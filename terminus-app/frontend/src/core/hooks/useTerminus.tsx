import React, { useContext } from "react";
import Web3Context from "../providers/Web3Provider/context";
import { web3MethodCall } from "../providers/Web3Provider/context";
import DataContext from "../providers/DataProvider/context";
import BN from "bn.js";
import { useMutation, useQuery, UseQueryResult } from "react-query";
import {
  getTerminusFacetState,
  createSimplePool,
  transferTerminusOwnership,
  withrawTerminusFunds,
  setController,
  setTerminusPoolBasePrice,
  setTerminusURI,
  setTerminusPaymentToken,
} from "../contracts/terminus.contracts";
import { getTokenState, setAllowance } from "../contracts/ERC20.contracts";
import {
  getTerminus,
  getweb3Auth,
  postweb3Auth,
} from "../services/terminus.service";
export interface useBottlerReturns {
  balanceCache: UseQueryResult<number, any>;
  allowanceCache: UseQueryResult<string, any>;
  fillBottles: web3MethodCall;
  fillEmptyBottles: web3MethodCall;
  approveSpendMilk: web3MethodCall;
  fullBottlesCache: UseQueryResult<Array<number>, any>;
  pourFullBottles: web3MethodCall;
  bottleVolumesCache: UseQueryResult<Array<{ matic: number; bn: BN }>, any>;
  bottlesLeftCache: UseQueryResult<Array<number>, any>;
  emptyBottlesCache: UseQueryResult<Array<number>, any>;
  fullBottlesPricesCache: UseQueryResult<Array<{ matic: number; bn: BN }>, any>;
}
import queryCacheProps from "./hookCommon";

export interface useBottlerArgumentsType {
  diamondAddress: string;
  targetChain: any;
}
// const diamondJSON = require("../../../../build/contracts/Diamond.json");
const terminusFacetJSON = require("../../../abi/TerminusFacet.json");
const ownershipFacetJSON = require("../../../abi/OwnershipFacet.json");
// const moonstreamTokenFaucetJSON = require("../../../../build/contracts/MoonstreamTokenFaucet.json");
const useTerminus = ({
  diamondAddress,
  targetChain,
}: useBottlerArgumentsType) => {
  const { contracts, dispatchContracts } = useContext(DataContext);
  const web3Provider = useContext(Web3Context);

  React.useEffect(() => {
    if (!contracts["terminusFacet"]) {
      dispatchContracts({
        key: "terminusFacet",
        abi: terminusFacetJSON, //Facet abi
        address: diamondAddress, // Diamond address
      });
    }
    if (!contracts["ownershipFacet"]) {
      dispatchContracts({
        key: "ownershipFacet",
        abi: ownershipFacetJSON, //Facet abi
        address: diamondAddress, // Diamond address
      });
    }
  }, [contracts, diamondAddress, targetChain, dispatchContracts]);

  const terminusFacetCacheW2 = useQuery(
    ["terminusFacetW2", diamondAddress, targetChain.chainId],
    () => getTerminus(diamondAddress, targetChain.chainId),
    {
      onSuccess: () => {},
      ...queryCacheProps,
      enabled:
        web3Provider.web3?.utils.isAddress(web3Provider.account) &&
        web3Provider.chainId === targetChain.chainId,
    }
  );



  const terminusFacetCache = useQuery(
    ["terminusFacet", diamondAddress, targetChain.chainId],
    getTerminusFacetState(
      {
        terminusFacet: contracts["terminusFacet"],
        ownershipFacet: contracts["ownershipFacet"],
      },
      web3Provider.account
    ),
    {
      onSuccess: () => {},
      enabled:
        !!contracts["ownershipFacet"] &&
        !!contracts["terminusFacet"] &&
        web3Provider.web3?.utils.isAddress(web3Provider.account) &&
        web3Provider.chainId === targetChain.chainId,
    }
  );

  const terminusPaymentTokenCache = useQuery(
    ["terminus", "terminusPaymentToken", terminusFacetCache.data?.paymentToken],
    (query) =>
      getTokenState({
        provider: web3Provider,
        spender: diamondAddress,
        account: web3Provider.account,
      })(query.queryKey[2] ?? ""),
    {
      onSuccess: () => {},
      enabled:
        !!terminusFacetCache.data?.paymentToken &&
        web3Provider.web3?.utils.isAddress(web3Provider.account) &&
        web3Provider.chainId === targetChain.chainId,
    }
  );

  const approveTerminusMutation = useMutation(
    async ({
      amount,
      spender,
      transactionConfig,
    }: {
      amount: string | BN;
      spender?: string;
      transactionConfig?: any;
    }) => {
      if (terminusFacetCache.data?.paymentToken) {
        return setAllowance(
          web3Provider,
          terminusFacetCache.data?.paymentToken,
          { from: web3Provider.account },
          diamondAddress
        )({ amount, spender, transactionConfig });
      } else {
        throw "payment token not provided";
      }
    },
    {
      onSuccess: () => {
        console.log("success approve terminus");
      },
      onSettled: () => {
        terminusFacetCache.refetch();
        terminusPaymentTokenCache.refetch();
      },
    }
  );

  const handleCreateNewPool = async (capacity: string) => {
    if (
      terminusPaymentTokenCache.data?.allowance &&
      terminusFacetCache.data?.poolBasePrice
    ) {
      if (
        terminusPaymentTokenCache.data?.allowance <
        terminusFacetCache.data?.poolBasePrice
      ) {
        const result = approveTerminusMutation
          .mutateAsync({
            amount: terminusFacetCache.data?.poolBasePrice,
          })
          .then(() =>
            createSimplePool(contracts["terminusFacet"], {
              from: web3Provider.account,
            })({ capacity: capacity })
          );
        return result;
        // setAwaitingAllowance(true);
        // setAwaitingCapacity(capacity);
      } else {
        // createPoolMutation.mutate({ capacity });
        return createSimplePool(contracts["terminusFacet"], {
          from: web3Provider.account,
        })({ capacity: capacity });
      }
    }
  };

  const createPoolMutation = useMutation(handleCreateNewPool, {
    onSuccess: (resp) => {
      console.log("createPoolMutation success:", resp);
    },
    onSettled: () => {
      terminusFacetCache.refetch();
      terminusPaymentTokenCache.refetch();
    },
  });

  const transferTerminusOwnershipMutation = useMutation(
    transferTerminusOwnership(contracts["ownershipFacet"], {
      from: web3Provider.account,
    }),
    {
      onSuccess: (resp) => {
        console.log("transferTerminusOwnershipMutation success:", resp);
      },
      onSettled: () => {
        terminusFacetCache.refetch();
        terminusPaymentTokenCache.refetch();
      },
    }
  );

  const setTerminusController = useMutation(
    setController(contracts["terminusFacet"], {
      from: web3Provider.account,
    }),
    {
      onSuccess: (resp) => {
        console.log("setTerminusController success:", resp);
      },
      onSettled: () => {
        terminusFacetCache.refetch();
        terminusPaymentTokenCache.refetch();
      },
    }
  );

  const withrawPayments = useMutation(
    withrawTerminusFunds(contracts["terminusFacet"], {
      from: web3Provider.account,
    }),
    {
      onSuccess: (resp) => {
        console.log("withrawPayments success:", resp);
      },
      onSettled: () => {
        terminusFacetCache.refetch();
        terminusPaymentTokenCache.refetch();
      },
    }
  );

  const setPoolBasePrice = useMutation(
    setTerminusPoolBasePrice(contracts["terminusFacet"], {
      from: web3Provider.account,
    }),
    {
      onSuccess: (resp) => {
        console.log("setPoolBasePrice success:", resp);
      },
      onSettled: () => {
        terminusFacetCache.refetch();
        terminusPaymentTokenCache.refetch();
      },
    }
  );

  const setURI = useMutation(
    setTerminusURI(contracts["terminusFacet"], {
      from: web3Provider.account,
    }),
    {
      onSuccess: (resp) => {
        console.log("setURI success:", resp);
      },
      onSettled: () => {
        terminusFacetCache.refetch();
        terminusPaymentTokenCache.refetch();
      },
    }
  );

  const setPaymentToken = useMutation(
    setTerminusPaymentToken(contracts["terminusFacet"], {
      from: web3Provider.account,
    }),
    {
      onSuccess: (resp) => {
        console.log("setPaymentToken success:", resp);
      },
      onSettled: () => {
        terminusFacetCache.refetch();
        terminusPaymentTokenCache.refetch();
      },
    }
  );

  return {
    terminusFacetCache,
    createPoolMutation,
    approveTerminusMutation,
    terminusPaymentTokenCache,
    handleCreateNewPool,
    transferTerminusOwnershipMutation,
    withrawPayments,
    setTerminusController,
    setPoolBasePrice,
    setURI,
    setPaymentToken,
  };
};

export default useTerminus;
