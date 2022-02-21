import React, { useContext } from "react";
import Web3Context from "../providers/Web3Provider/context";
import { useToast } from "./";
import { web3MethodCall } from "../providers/Web3Provider/context";
import useWeb3MethodCall from "./useWeb3MethodCall";
import DataContext from "../providers/DataProvider/context";
import BN from "bn.js";
import {
  useMutation,
  useQuery,
  useQueryClient,
  UseQueryResult,
} from "react-query";
import { queryCacheProps } from "./hookCommon";
// import { }
// import { bottler } from ...
import { Diamond } from "../../../contracts/Diamond";
import { DiamondLoupeFacet } from "../../../contracts/DiamondLoupeFacet";
import { DiamondCutFacet } from "../../../contracts/DiamondCutFacet";
import { OwnershipFacet } from "../../../contracts/OwnershipFacet";
import { TerminusFacet } from "../../../contracts/TerminusFacet";
import {
  getTerminusFacetState,
  createSimplePool,
} from "../contracts/terminus.contracts";
import { getTokenState, setAllowance } from "../contracts/ERC20.contracts";

export interface BottleType {
  name: string;
  imageUrl: string;
  emptyImageURL: string;
  // TODO(zomglings): Rename to poolIndex. It is too easy to confuse poolId as referring to the Terminus
  // pool ID.
  poolId: number;
  terminusPoolId: number;
}
export interface BottleTypes {
  small: BottleType;
  medium: BottleType;
  large: BottleType;
}

export const BOTTLE_TYPES: BottleTypes = {
  small: {
    name: "small",
    emptyImageURL:
      "https://s3.amazonaws.com/static.simiotics.com/unicorn_bazaar/small_empty_bottle.png",
    imageUrl:
      "https://s3.amazonaws.com/static.simiotics.com/unicorn_bazaar/small_um.png",
    poolId: 0,
    terminusPoolId: 5,
  },
  medium: {
    name: "medium",
    emptyImageURL:
      "https://s3.amazonaws.com/static.simiotics.com/unicorn_bazaar/medium_empty_bottle.png",
    imageUrl:
      "https://s3.amazonaws.com/static.simiotics.com/unicorn_bazaar/medium_um.png",
    poolId: 1,
    terminusPoolId: 6,
  },
  large: {
    name: "large",
    emptyImageURL:
      "https://s3.amazonaws.com/static.simiotics.com/unicorn_bazaar/large_empty_bottle.png",
    imageUrl:
      "https://s3.amazonaws.com/static.simiotics.com/unicorn_bazaar/large_um.png",
    poolId: 2,
    terminusPoolId: 7,
  },
};

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

export interface useBottlerArgumentsType {
  DiamondAddress: string;
  targetChain: any;
}
const diamondJSON = require("../../../../build/contracts/Diamond.json");
const terminusFacetJSON = require("../../../../build/contracts/TerminusFacet.json");
const moonstreamTokenFaucetJSON = require("../../../../build/contracts/MoonstreamTokenFaucet.json");
const useTerminus = ({
  DiamondAddress,
  targetChain,
}: useBottlerArgumentsType) => {
  const { contracts, dispatchContracts } = useContext(DataContext);
  const web3Provider = useContext(Web3Context);

  React.useEffect(() => {
    if (!contracts["terminusFacet"]) {
      console.log("terminusFacetJSON.abi", terminusFacetJSON.abi);
      dispatchContracts({
        key: "terminusFacet",
        abi: terminusFacetJSON.abi, //Facet abi
        address: DiamondAddress, // Diamond address
      });
    }
  }, [contracts, DiamondAddress, targetChain, dispatchContracts]);

  const _poolBasePrice = async () => {
    const terminusDiamond = contracts["terminusFacet"] as TerminusFacet;
    // console.debug("start _tcall", terminusDiamond.methods.);
    const response = await terminusDiamond.methods.poolBasePrice().call();
    return response;
  };

  const terminusFacetCache = useQuery(
    ["terminusFacet", DiamondAddress],
    getTerminusFacetState(contracts["terminusFacet"], web3Provider.account),
    {
      onSuccess: () => {},
      enabled:
        web3Provider.web3?.utils.isAddress(web3Provider.account) &&
        web3Provider.chainId === targetChain.chainId,
    }
  );

  const terminusPaymentTokenCache = useQuery(
    ["terminus", "terminusPaymentToken", terminusFacetCache.data?.paymentToken],
    (query) =>
      getTokenState({
        provider: web3Provider,
        spender: DiamondAddress,
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
          DiamondAddress
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

  const [awaitingAllowance, setAwaitingAllowance] = React.useState(false);
  const [awaitingCapcity, setAwaitingCapacity] = React.useState<string>("");
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

  React.useEffect(() => {
    if (
      awaitingAllowance &&
      !terminusPaymentTokenCache.isLoading &&
      !approveTerminusMutation.isLoading
    ) {
      if (
        terminusPaymentTokenCache.data?.allowance &&
        terminusFacetCache.data?.poolBasePrice
      ) {
        if (
          terminusPaymentTokenCache.data.allowance >=
          terminusFacetCache.data.poolBasePrice
        ) {
          // createPoolMutation.mutate({ capacity: awaitingCapcity });
          createSimplePool(contracts["terminusFacet"], {
            from: web3Provider.account,
          });
        }
      }
    }
  }, [
    awaitingAllowance,
    terminusPaymentTokenCache.isLoading,
    terminusPaymentTokenCache.data,
    approveTerminusMutation.isLoading,
  ]);

  const createPoolMutation = useMutation(handleCreateNewPool, {
    onSuccess: (resp) => {
      console.log("createSimplePool success:", resp);
    },
    onSettled: () => {
      terminusFacetCache.refetch();
      terminusPaymentTokenCache.refetch();
    },
  });

  return {
    terminusFacetCache,
    createPoolMutation,
    approveTerminusMutation,
    terminusPaymentTokenCache,
    handleCreateNewPool,
  };
};

export default useTerminus;
