import { createContext } from "react";
import Web3 from "web3";

export interface WalletStatesInterface {
  ONBOARD: string;
  CONNECT: string;
  CONNECTED: string;
  WRONG_CHAIN: string;
}

export enum txStatus {
  READY = 0,
  SUCCESS,
  ERROR,
  LOADING,
}

export interface Web3ProviderInterface {
  web3: Web3;
  onConnectWalletClick: () => void;
  buttonText: string;
  WALLET_STATES: WalletStatesInterface;
  account: string;
  chainId: number | void;
}

export interface web3MethodCall {
  status: txStatus;
  send: (...args: Array<any>) => void;
  data: any;
}

export const WALLET_STATES: WalletStatesInterface = {
  ONBOARD: "Install MetaMask!",
  CONNECT: "Connect with Metamask",
  CONNECTED: "Connected",
  WRONG_CHAIN: "Please select polygon chain in metamask",
};

const Web3Context = createContext<Web3ProviderInterface>({
  web3: new Web3(null),
  onConnectWalletClick: () => console.error("not intied"),
  buttonText: "",
  WALLET_STATES: WALLET_STATES,
  account: "",
  chainId: undefined,
});

export default Web3Context;
