import React, { createContext } from "react";
import { Contract } from "web3-eth-contract";
import { BaseContract } from "../../../../contracts/types";

export interface ContractsHolder {
  [key: string]: BaseContract;
}

export interface DataContext {
  dispatchContracts: React.Dispatch<any>;
  contracts: ContractsHolder;

}
const DataContext = createContext<DataContext>({
  dispatchContracts: () => null,
  contracts: {},
});

export default DataContext;
