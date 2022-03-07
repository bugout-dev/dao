import React, { useContext } from "react";
import Web3Context from "../providers/Web3Provider/context";
import DataContext from "../providers/DataProvider/context";
import { useMutation, useQuery } from "react-query";
import {
  getTerminusFacetPoolState,
  mintNewAccessToken,
  setTerminusPoolController,
  setTerminusPoolURI,
} from "../contracts/terminus.contracts";
import useTerminus from "./useTerminus";
import * as abi from "../../../abi/TerminusFacet.json";
import { TerminusFacet } from "../../../types/contracts/TerminusFacet";

export interface useTerminusPoolArgumentsType {
  DiamondAddress: string;
  poolId: string;
  targetChain: any;
}

const useTerminusPool = ({
  DiamondAddress,
  poolId,
  targetChain,
}: useTerminusPoolArgumentsType) => {
  const { contracts, dispatchContracts } = useContext(DataContext);
  const web3Provider = useContext(Web3Context);

  const terminus = useTerminus({
    diamondAddress: DiamondAddress,
    targetChain: targetChain,
  });

  React.useEffect(() => {
    if (!contracts["terminusFacet"]) {
      dispatchContracts({
        key: "terminusFacet",
        abi: abi, //Facet abi
        address: DiamondAddress, // Diamond address
      });
    }
  }, [contracts, DiamondAddress, targetChain, dispatchContracts]);

  const terminusPoolCache = useQuery(
    ["terminusPoolState", poolId, DiamondAddress, targetChain.chainId],
    getTerminusFacetPoolState(contracts["terminusFacet"], poolId),
    {
      onSuccess: () => {
        console.debug("succ");
      },
      refetchInterval: 1000000,
      staleTime: Infinity,
      enabled:
        !!terminus.terminusFacetCache.data?.paymentToken &&
        !!contracts["terminusFacet"] &&
        web3Provider.web3?.utils.isAddress(web3Provider.account) &&
        web3Provider.chainId === targetChain.chainId,
    }
  );

  const mintPoolNFTMutation = useMutation(
    (args: any) =>
      mintNewAccessToken(contracts["terminusFacet"], {
        from: web3Provider.account,
      })({ poolId, ...args }),
    {
      onSettled: () => {
        terminus.terminusFacetCache.refetch();
        terminusPoolCache.refetch();
      },
    }
  );

  const setPoolController = useMutation(
    setTerminusPoolController(contracts["terminusFacet"], poolId, {
      from: web3Provider.account,
    }),
    {
      onSettled: () => {
        terminus.terminusFacetCache.refetch();
        terminusPoolCache.refetch();
      },
    }
  );

  const setPoolURI = useMutation(
    (args: any) =>
      setTerminusPoolURI(contracts["terminusFacet"], {
        from: web3Provider.account,
      })({ poolId, ...args }),
    {
      onSuccess: (resp) => {
        console.log("setPoolURI success:", resp);
      },
      onSettled: () => {
        terminus.terminusFacetCache.refetch();
        terminusPoolCache.refetch();
      },
    }
  );

  const getMethodsABI = React.useCallback(
    <T extends keyof TerminusFacet["methods"]>(name: T): typeof abi[number] => {
      const index = abi.findIndex(
        (item) => item.name === name && item.type == "function"
      );
      if (index !== -1) {
        const item = abi[index];
        return item;
      } else throw "accesing wrong abi element";
    },
    []
  );

  return {
    terminusPoolCache,
    mintPoolNFTMutation,
    setPoolController,
    setPoolURI,
    abi,
    getMethodsABI,
  };
};

export default useTerminusPool;
