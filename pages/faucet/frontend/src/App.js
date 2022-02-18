import './App.css';
import faucetContract from './contracts/MoonstreamTokenFaucet.json';
import { useEffect } from 'react';
import { useState } from 'react';
import { ethers } from 'ethers';

const CONTRACT_ADDRESS = "0x008dB85178d557a5612941131FDF75028422Df33";
const abi = faucetContract.abi;

function App() {

  const [currentAccount, setCurrentAccount] = useState(null);

  const checkWalletIsConnected = () => {
    const { ethereum } = window;

    if (!ethereum) {
      console.log("Metamask must be installed!");
    } else {
      console.log("Metamask detected");
    }
  }

  const connectWalletHandler = async () => {
    const { ethereum } = window;

    if (!ethereum) {
      alert("Metamask must be installed!")
    } else {
      const chainId = await ethereum.request({ method: 'eth_chainId' });

      if (chainId !== "0x13881") {
        alert("Make sure you're connected to Polygon Testnet (Mumbai)");
        return;
      }
    }

    try {
      console.log(ethereum.selectedAddress, "is connected");
      setCurrentAccount(ethereum.selectedAddress);
    } catch (err) {
      console.log(err);
    }
  }

  const claimHandler = async () => {
    try {
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
      <button onClick={connectWalletHandler} className='main-button connect-wallet-button'>
        Connect Wallet
      </button>
    )
  }

  const claimButton = () => {
    return (
      <button onClick={claimHandler} className='main-button claim-button'>
        Claim MNSTR
      </button>
    )
  }

  useEffect(() => {
    checkWalletIsConnected();
  }, [])

  return (
    <div className='main-app'>
      <h1>Moonstream Faucet</h1>
      <div>
        {currentAccount ? claimButton() : connectWalletButton()}
      </div>
    </div>
  )
}

export default App;