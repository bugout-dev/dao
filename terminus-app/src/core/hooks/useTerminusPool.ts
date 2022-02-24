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
  getTerminusFacetPoolState,
  mintNewAccessToken,
  setTerminusPoolController,
} from "../contracts/terminus.contracts";
import useTerminus from "./useTerminus";
import { string } from "yargs";
import { terminus } from "../services";

export interface useTerminusPoolArgumentsType {
  DiamondAddress: string;
  poolId: string;
  targetChain: any;
}
const diamondJSON = require("../../../../build/contracts/Diamond.json");
const terminusFacetJSON = require("../../../../build/contracts/TerminusFacet.json");
const useTerminusPool = ({
  DiamondAddress,
  poolId,
  targetChain,
}: useTerminusPoolArgumentsType) => {
  const { contracts, dispatchContracts } = useContext(DataContext);
  const web3Provider = useContext(Web3Context);

  const terminus = useTerminus({
    DiamondAddress: DiamondAddress,
    targetChain: targetChain,
  });

  React.useEffect(() => {
    if (!contracts["terminusFacet"]) {
      dispatchContracts({
        key: "terminusFacet",
        abi: terminusFacetJSON.abi, //Facet abi
        address: "0x040Cf7Ee9752936d8d280062a447eB53808EBc08", // Diamond address
      });
    }
  }, [contracts, DiamondAddress, targetChain, dispatchContracts]);

  const terminusFacetCache = useQuery(
    ["terminusPoolState", poolId, DiamondAddress],
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
    mintNewAccessToken(contracts["terminusFacet"], {
      from: web3Provider.account,
    }),
    {
      onSettled: () => {
        terminus.terminusFacetCache.refetch();
        terminusFacetCache.refetch();
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
        terminusFacetCache.refetch();
      },
    }
  );

  return { terminusFacetCache, mintPoolNFTMutation, setPoolController };
};

export default useTerminusPool;
