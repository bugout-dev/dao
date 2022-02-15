import React, { useContext } from "react";
import DataContext, { ContractsHolder } from "./context";
import { Contract } from "web3-eth-contract";
import Web3Context from "../Web3Provider/context";
import BN from "bn.js";
const erc20abi = require("../../../../abi/erc20.json");
const bottlerAbi = require("../../../../abi/bottlerAbi.json");
const terminusDiamondAbi = require("../../../../../build/contracts/Diamond.json");


type Reducer<S, A> = (prevState: S, action: A) => S;

const DataProvider = ({ children }: { children: JSX.Element }) => {
  const { web3 } = useContext(Web3Context);

  const setContracts = (state: ContractsHolder, action: any): ContractsHolder =>
  {
    const newContract = new web3.eth.Contract(action.abi) as any;
    const newState = {... state}
    newState[action.key] = newContract;
    newContract.options.address = action.address
    return {...newState}
  }
  const [contracts, dispatchContracts] = React.useReducer(setContracts,{})


  return (
    <DataContext.Provider
      value={{
        contracts,
        dispatchContracts,
      }}
    >
      {children}
    </DataContext.Provider>
  );
};

export default DataProvider;
