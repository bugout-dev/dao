import { TerminusFacet } from "../../../contracts/TerminusFacet";
import { BaseContract } from "../../../contracts/types";
import { setAllowance } from "./ERC20.contracts";
import BN from "bn.js";
import Web3 from "web3";
import { ERC20WithCommonStorage } from "../../../contracts/ERC20WithCommonStorage";
import { MoonstreamTokenFaucet } from "../../../contracts/MoonstreamTokenFaucet";
const erc20abi = require("../../../abi/erc20.json");

export const getTerminusFacetState =
  (contract: BaseContract, owner?: string) => async () => {
    console.log("getTerminusFacetState");
    const terminusFacet = contract as TerminusFacet;
    // const controller = await terminusFacet.methods.terminusController().call();
    const poolBasePrice = await terminusFacet.methods.poolBasePrice().call();
    console.log("poolBasePrice", poolBasePrice);
    const paymentToken = await terminusFacet.methods.paymentToken().call();
    const contractURI = await terminusFacet.methods.contractURI().call();
    const totalPools = await terminusFacet.methods.totalPools().call();
    let numberOfOwnedPools = "0";
    let ownedPoolIds = [];
    if (owner) {
      numberOfOwnedPools = await terminusFacet.methods
        .totalPoolsByOwner(owner)
        .call();

      if (numberOfOwnedPools !== "0") {
        const n = new Number(numberOfOwnedPools);
        for (let i = 0; i < n; i++) {
          const poolId = await terminusFacet.methods
            .poolOfOwnerByIndex(owner, i)
            .call();
          ownedPoolIds.push(poolId);
        }
      }
    }

    return {
      poolBasePrice,
      paymentToken,
      contractURI,
      totalPools,
      numberOfOwnedPools,
      ownedPoolIds,
    };
  };

export const getTerminusFacetPoolState =
  (contract: BaseContract, poolId: string) => async () => {
    const terminusFacet = contract as TerminusFacet;
    const controller = await terminusFacet.methods
      .terminusPoolController(poolId)
      .call();
    const supply = await terminusFacet.methods
      .terminusPoolSupply(poolId)
      .call();
    const uri = await terminusFacet.methods.uri(poolId).call();
    const capacity = await terminusFacet.methods
      .terminusPoolCapacity(poolId)
      .call();

    return { controller, supply, uri, capacity };
  };

export const getNumberOfPoolsByOwner =
  (contract: BaseContract, owner: string) => async () => {
    const terminusFacet = contract as TerminusFacet;

    return number;
  };

export const createSimplePool =
  (contract: BaseContract, defaultTxConfig: any) =>
  async ({
    capacity,
    transactionConfig,
  }: {
    capacity: string;
    transactionConfig?: any;
  }) => {
    const terminusFacet = contract as TerminusFacet;
    const txConfig = { ...defaultTxConfig, ...transactionConfig };
    console.debug("txConfig", txConfig);
    const response = await terminusFacet.methods
      .createSimplePool(capacity)
      .send(txConfig);
    return response;
  };
