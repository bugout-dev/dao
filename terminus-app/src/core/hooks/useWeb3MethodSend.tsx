import React from "react";
import { Contract } from "web3-eth-contract";
import Web3Context, { txStatus } from "../providers/Web3Provider/context";
import { useContext } from "react";

export interface UseWeb3MethodSend {
  name: string;
  contract: Contract;
  targetChain: any;
  onSuccess?: (receipt?: any) => void;
  onError?: (error?: any) => void;
}

const useWeb3MethodSend = ({
  name,
  contract,
  targetChain,
  onSuccess,
  onError,
}: UseWeb3MethodSend): { status: txStatus; send: (...args: any[]) => void } => {
  const [status, setStatus] = React.useState<txStatus>(txStatus.READY);
  const web3Provider = useContext(Web3Context);

  const send = (...args: any) => {
    if (
      web3Provider.web3?.utils.isAddress(web3Provider.account) &&
      web3Provider.chainId === targetChain.chainId
    ) {
      if (args.length === 0) {
        throw new Error("Error: Transaction submitted incorrectly");
      }
      let methodArgs = args.slice(0, args.length - 1);
      let transactionConfig = args[args.length - 1];
      if (!transactionConfig.from) {
        transactionConfig.from = web3Provider.account;
      }
      setStatus(txStatus.LOADING);
      contract.methods[`${name}`](...methodArgs)
        .send(transactionConfig)
        .once("receipt", (receipt: any) => {
          if (receipt.status) {
            setStatus(txStatus.SUCCESS);
            onSuccess && onSuccess(receipt);
          } else {
            console.error("transaction failed");
            setStatus(txStatus.ERROR);
            onError && onError(receipt);
          }
        })
        .once("error", (error: any) => {
          setStatus(txStatus.ERROR);
          console.error("Seems that EVM reverted transaction");
          onError && onError(error);
        });
    }
  };

  return { status, send };
};

export default useWeb3MethodSend;
