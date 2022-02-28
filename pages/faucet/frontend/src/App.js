import './App.css';
import { useContext } from "react";
import faucetContract from './contracts/MoonstreamTokenFaucet.json';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import React, { useEffect, useState } from 'react';
import { ethers } from 'ethers';
import Web3 from "web3";

const CONTRACT_ADDRESS = "0x008dB85178d557a5612941131FDF75028422Df33";
const abi = faucetContract.abi;

export const chains = {
  matic_mumbai: {
    chainId: 80001,
    name: "Matic mumbai",
    rpcs: [
      "https://rpc-mumbai.matic.today",
      "https://matic-mumbai.chainstacklabs.com",
      "https://rpc-mumbai.maticvigil.com",
      "https://matic-testnet-archive-rpc.bwarelabs.com",
    ],
  },
  matic: {
    chainId: 137,
    name: "Matic mainnet",
    rpcs: [
      "https://rpc-mainnet.matic.network",
      "https://matic-mainnet.chainstacklabs.com",
      "https://rpc-mainnet.maticvigil.com",
      "https://rpc-mainnet.matic.quiknode.pro",
      "https://matic-mainnet-full-rpc.bwarelabs.com",
    ],
  },
};

function App() {

  const web3 = new Web3(Web3.givenProvider || "ws://localhost:8545");
  const [currentAccount, setCurrentAccount] = useState(null);
  const [chainId, setChainId] = React.useState(null);

  // export const targetChain =
  // process.env.NODE_ENV === "development" ? chains.mumbai : chains.matic;

  const checkWalletIsConnected = () => {
    const { ethereum } = window;

    if (!ethereum) {
      console.log("Metamask must be installed!");
    } else {
      console.log("Metamask detected");
    }
  }

  const setWeb3ProviderAsWindowEthereum = async () => {
    let wasSetupSuccess = false;
    await window.ethereum
      .request({ method: "eth_requestAccounts" })
      .then(() => {
        web3.setProvider(window.ethereum);
        wasSetupSuccess = true;
      });
    return wasSetupSuccess;
  }

  const onConnectWalletClick = async () => {
    if (window.ethereum) {
      console.log("wallet provider detected -> connecting wallet");
      setWeb3ProviderAsWindowEthereum().then((result) => {
        if (result) {
          console.log("wallet setup was successfull");
          web3.eth.getAccounts().then((accounts) => setCurrentAccount(accounts[0]));

          toast.success('Wallet connected!', {
            position: "top-right",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            });
          }
        else
          console.warn(
            "wallet setup failed, should go in fallback mode immediately"
          );
      });
    }
  }

  React.useLayoutEffect(() => {
    if (web3.currentProvider) {
      console.log("web3 is getting chain id");
      web3?.eth.getChainId().then((id) => setChainId(id));
    }
  }, [web3.currentProvider, web3?.eth]);

  React.useLayoutEffect(() => {
    const changeChain = async () => {
      try {
        await window.ethereum
          .request({
            method: "wallet_switchEthereumChain",
            params: [{ chainId: `0x${chains.matic_mumbai.chainId.toString(16)}` }],
          })
          .then(() => web3?.eth.getChainId().then((id) => setChainId(id)));
      } catch (switchError) {
        // This error code indicates that the chain has not been added to MetaMask.
        if (switchError.code === 4902) {
          try {
            await window.ethereum.request({
              method: "wallet_addEthereumChain",
              params: [
                {
                  chainId: `${chains.matic_mumbai.chainId}`,
                  chainName: chains.matic_mumbai.name,
                  rpcUrls: chains.matic_mumbai.rpcs,
                },
              ],
            });
          } catch (addError) {
            // handle "add" error
          }
        }
        // handle other "switch" errors
      }
    };

    if (web3.currentProvider && chainId) {
      console.log(
        "Checking that",
        chainId,
        "corresponds to selected target chain id:",
        chains.matic_mumbai.chainId
      );
      if (chainId) {
        if (chainId === chains.matic_mumbai.chainId) {
          //we are on matic
          console.log("chain id is correct");
        } else {
          //we are not on matic
          console.log("requesting to change chain Id", chainId);
          changeChain();
        }
      }
    }
  }, [chainId, web3.currentProvider, web3?.eth]);

  React.useLayoutEffect(() => {
    if (chainId === chains.matic_mumbai.chainId && web3.currentProvider) {
      web3.eth.getAccounts().then((accounts) => setCurrentAccount(accounts[0]));
    }
  }, [chainId, web3.currentProvider, web3?.eth]);

  window?.ethereum?.on("chainChanged", () => window.location.reload());

  const claimHandler = async () => {
    try {
      console.log(currentAccount);
      const { ethereum } = window;

      if (ethereum) {
        const provider = new ethers.providers.Web3Provider(ethereum);
        const signer = provider.getSigner();
        const nftContract = new ethers.Contract(CONTRACT_ADDRESS, abi, signer);

        let claimTxn = await nftContract.claim();
        await claimTxn.wait();
        console.log(`Funds confirmed, see transaction: https://mumbai.polygonscan.com/tx/${claimTxn.hash}`);
      }

    } catch (err) {
      console.log(err);
    }
  }

  const connectWalletButton = () => {
    return (
      <button onClick={onConnectWalletClick} className="main-button connect-wallet-button">
        Connect Wallet
      </button>
    )
  }

  const claimButton = () => {
    return (
      <button onClick={claimHandler} className="main-button claim-button">
        Claim MNSTR
      </button>
    )
  }

  useEffect(() => {
    console.log(currentAccount);
    checkWalletIsConnected();
  }, [])

  return (
    <div className="main-app">
      <h1>Moonstream Faucet</h1>
      <div>
        {currentAccount ? claimButton() : connectWalletButton()}
      </div>
      <ToastContainer />
    </div>
  )
}

export default App;