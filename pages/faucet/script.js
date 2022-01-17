
const faucetAbi = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_MOONSTREAM_TOKEN_ADDRESS",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_FAUCET_AMOUNT",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_FAUCET_BLOCK_INTERVAL",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "address",
                "name": "previousOwner",
                "type": "address"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "OwnershipTransferred",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "claim",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getFaucetAmount",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getFaucetBlockInterval",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_address",
                "type": "address"
            }
        ],
        "name": "getLastClaimedBlock",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getMoonstreamTokenAddress",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_address",
                "type": "address"
            }
        ],
        "name": "getMoonstreamTokenBalance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },

]

const moonstreamTokenAbi = [{
    "inputs": [
        {
            "internalType": "address",
            "name": "account",
            "type": "address"
        }
    ],
    "name": "balanceOf",
    "outputs": [
        {
            "internalType": "uint256",
            "name": "",
            "type": "uint256"
        }
    ],
    "stateMutability": "view",
    "type": "function"
}]


const faucetContractAddress = "0x008dB85178d557a5612941131FDF75028422Df33"


function isMetamaskInstalled() {
    return typeof window.ethereum !== 'undefined' && ethereum.isMetaMask
}
function isMetamaskConnectedToMumbai() {
    return window.ethereum.networkVersion === "80001"
}

async function connectToMetamask() {
    if (!isMetamaskInstalled()) {
        alert("Please install MetaMask to use this faucet.")
        return false
    }
    if (!isMetamaskConnectedToMumbai()) {
        alert("Please connect MetaMask to Mumbai testnet to use this faucet.")
        return false
    }
    //window.ethereum.enable() // deprrecated
    await ethereum.request({ method: 'eth_requestAccounts' });
    return true
}


async function claim() {
    isConnected = await connectToMetamask()
    if (!isConnected) {
        return
    }
    let web3 = new Web3(window.ethereum)
    let faucetContract = new web3.eth.Contract(faucetAbi, faucetContractAddress)

    let lastClaimedBlock = await faucetContract.methods.getLastClaimedBlock(window.ethereum.selectedAddress).call()
    let currentBlock = await web3.eth.getBlockNumber()
    let blockInterval = await faucetContract.methods.getFaucetBlockInterval().call()

    if (currentBlock - lastClaimedBlock < blockInterval) {
        alert("You can claim again in " + (blockInterval - (currentBlock - lastClaimedBlock)) + " blocks.")
        return
    }

    let faucetAmount = await faucetContract.methods.getFaucetAmount().call()
    let faucetMoonstreamTokenBalance = await faucetContract.methods.getMoonstreamTokenBalance(faucetContractAddress).call()

    if (faucetMoonstreamTokenBalance < faucetAmount) {
        alert("Faucet is empty. Please try again later.")
        return
    }

    faucetContract.methods.claim().send({ from: window.ethereum.selectedAddress })
        .on('transactionHash', function (hash) {
            console.log("Transaction hash: " + hash)
        }
        ).on('receipt', function (receipt) {
            console.log("Transaction receipt: " + receipt)
            setBalance()
        }
        ).on('confirmation', function (confirmationNumber, receipt) {
            console.log("Transaction confirmation: " + confirmationNumber)
        }
        ).on('error', function (error) {
            console.log("Transaction error: " + error)
        }
        )

}


async function setBalance() {
    isConnected = await connectToMetamask()
    if (!isConnected) {
        return
    }

    let web3 = new Web3(window.ethereum)
    let faucetContract = new web3.eth.Contract(faucetAbi, faucetContractAddress)
    let moonstreamTokenAddress = await faucetContract.methods.getMoonstreamTokenAddress().call()
    let moonstreamTokenContract = new web3.eth.Contract(moonstreamTokenAbi, moonstreamTokenAddress)
    let balance = await moonstreamTokenContract.methods.balanceOf(window.ethereum.selectedAddress).call()
    balance = web3.utils.fromWei(balance, 'ether')
    document.getElementById("moonstreamTokenBalance").innerHTML = balance
    // make button with id connect not clickable
    document.getElementById("connect").disabled = true
}

async function addTokenToMetamask() {

    isConnected = await connectToMetamask()
    if (!isConnected) {
        return
    }
    let web3 = new Web3(window.ethereum)
    let faucetContract = new web3.eth.Contract(faucetAbi, faucetContractAddress)
    let moonstreamTokenAddress = await faucetContract.methods.getMoonstreamTokenAddress().call()
    try {
        // wasAdded is a boolean. Like any RPC method, an error may be thrown.
        const wasAdded = await ethereum.request({
            method: 'wallet_watchAsset',
            params: {
                type: 'ERC20', // Initially only supports ERC20, but eventually more!
                options: {
                    address: moonstreamTokenAddress, // The address that the token is at.
                    symbol: "MNSTR", // A ticker symbol or shorthand, up to 5 chars.
                    decimals: "18", // The number of decimals in the token
                    // image: tokenImage, // A string url of the token logo
                },
            },
        });

        if (wasAdded) {
            alert("Token added to your wallet!")
            console.log('Thanks for your interest!');
            // make add-token button not clickable
            document.getElementById("addToken").disabled = true
        } else {
            console.log('Your loss!');
        }
    }
    catch (error) {
        console.log(error);
    }
}



