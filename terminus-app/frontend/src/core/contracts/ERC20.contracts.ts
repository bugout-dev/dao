import { ERC20Facet } from "../../../types/contracts/ERC20Facet";
import BN from "bn.js";
import { Web3ProviderInterface } from "../providers/Web3Provider/context";
import { AbiItem } from "web3-utils"
const erc20abi: AbiItem = require("../../../abi/ERC20Facet.json");

export const setAllowance =
  (
    provider: Web3ProviderInterface,
    address: string,
    defaultTxConfig: any,
    defaultSpender?: string
  ) =>
  async ({
    amount,
    spender,
    transactionConfig,
  }: {
    amount: string | BN;
    spender?: string;
    transactionConfig?: any;
  }) => {
    const erc20contract = new provider.web3.eth.Contract(
      erc20abi
    ) as any as ERC20Facet;
    erc20contract.options.address = address;
    const txConfig = { ...defaultTxConfig, ...transactionConfig };
    if (!spender && !defaultSpender) {
      throw "spender must be defined";
    }
    const _spender = (spender ?? defaultSpender) as string;
    const response = await erc20contract.methods
      .approve(_spender, amount)
      .send(txConfig);
    return response;
  };

export const getTokenState =
  ({
    provider,
    account,
    spender,
  }: {
    provider: Web3ProviderInterface;
    account?: string;
    spender?: string;
  }) =>
  async (address: string) => {
    const erc20contract = new provider.web3.eth.Contract(
      erc20abi
    ) as any as ERC20Facet;
    erc20contract.options.address = address;
    const balance = account
      ? await erc20contract.methods.balanceOf(account).call()
      : null;
    const spenderBalance = spender
      ? await erc20contract.methods.balanceOf(spender).call()
      : null;
    const allowance =
      spender && account
        ? await erc20contract.methods.allowance(account, spender).call()
        : null;
    const totalSupply = await erc20contract.methods.totalSupply().call();
    const symbol = await erc20contract.methods.symbol().call();
    const decimals = await erc20contract.methods.decimals().call();
    const name = await erc20contract.methods.name().call();
    return {
      totalSupply,
      symbol,
      decimals,
      name,
      balance,
      allowance,
      spenderBalance,
    };
  };
