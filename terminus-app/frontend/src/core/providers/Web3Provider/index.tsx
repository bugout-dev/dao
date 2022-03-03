import React from "react";
import Web3Context, { WALLET_STATES } from "./context";
import Web3 from "web3";

declare global {
  interface Window {
    ethereum: any;
    web3: Web3;
  }
}

export const chains = {
  local: {
    chainId: 1337,
    name: "local",
    rpcs: ["http://127.0.0.1:8545"],
  },
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

export const targetChain =
  process.env.NODE_ENV === "development" ? chains.local : chains.matic;

const Web3Provider = ({ children }: { children: JSX.Element }) => {
  const [web3] = React.useState<Web3>(new Web3(null));
  const [buttonText, setButtonText] = React.useState(WALLET_STATES.ONBOARD);
  const [account, setAccount] = React.useState<string>("");
  const [chainId, setChainId] = React.useState<number | void>();

  const setWeb3ProviderAsWindowEthereum = async () => {
    let wasSetupSuccess = false;
    await window.ethereum
      .request({ method: "eth_requestAccounts" })
      .then(() => {
        web3.setProvider(window.ethereum);
        wasSetupSuccess = true;
      });
    return wasSetupSuccess;
  };

  const onConnectWalletClick = () => {
    if (window.ethereum) {
      console.log("wallet provider detected -> connecting wallet");
      setWeb3ProviderAsWindowEthereum().then((result) => {
        if (result) console.log("wallet setup was successfull");
        else
          console.warn(
            "wallet setup failed, should go in fallback mode immediately"
          );
        setButtonText(result ? WALLET_STATES.CONNECTED : WALLET_STATES.CONNECT);
      });
    }
  };

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
            params: [{ chainId: `0x${targetChain.chainId.toString(16)}` }],
          })
          .then(() => web3?.eth.getChainId().then((id) => setChainId(id)));
      } catch (switchError: any) {
        // This error code indicates that the chain has not been added to MetaMask.
        if (switchError.code === 4902) {
          try {
            await window.ethereum.request({
              method: "wallet_addEthereumChain",
              params: [
                {
                  chainId: `${targetChain.chainId}`,
                  chainName: targetChain.name,
                  rpcUrls: targetChain.rpcs,
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
        targetChain.chainId
      );
      if (chainId) {
        if (chainId === targetChain.chainId) {
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
    if (chainId === targetChain.chainId && web3.currentProvider) {
      web3.eth.getAccounts().then((accounts) => setAccount(accounts[0]));
    }
  }, [chainId, web3.currentProvider, web3?.eth]);

  window?.ethereum?.on("chainChanged", () => window.location.reload());
  window?.ethereum?.on("accountsChanged", (_accounts: Array<string>) => {
    if (chainId === targetChain.chainId && web3.currentProvider) {
      setAccount(web3.utils.toChecksumAddress(_accounts[0]));
    }
  });

  React.useLayoutEffect(() => {
    if (web3.currentProvider && chainId) {
      if (chainId === targetChain.chainId) {
        setButtonText(WALLET_STATES.CONNECTED);
      } else {
        setButtonText(WALLET_STATES.WRONG_CHAIN);
      }
    } else {
      if (!window.ethereum) {
        setButtonText(WALLET_STATES.ONBOARD);
      } else {
        setButtonText(WALLET_STATES.CONNECT);
      }
    }
  }, [web3.currentProvider, chainId]);

  return (
    <Web3Context.Provider
      value={{
        web3: web3,
        onConnectWalletClick,
        buttonText,
        WALLET_STATES,
        account,
        chainId,
      }}
    >
      {children}
    </Web3Context.Provider>
  );
};

export default Web3Provider;
