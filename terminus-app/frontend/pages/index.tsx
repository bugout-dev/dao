import React, { useContext } from "react";
import { Flex, Button, Image, Center } from "@chakra-ui/react";
import { DEFAULT_METATAGS } from "../src/core/constants";
import Web3Context from "../src/core/providers/Web3Provider/context";
import Terminus from "../src/components/Terminus";
const assets: any = {
  onboarding:
    "https://s3.amazonaws.com/static.simiotics.com/unicorn_bazaar/unim-onboarding.png",
};

const Homepage = () => {
  const web3Provider = useContext(Web3Context);

  return (
    <Flex w="100%" minH="100vh" bgColor={"blue.1200"} direction={"column"}>
      {web3Provider.account && <Terminus />}
      {!web3Provider.account &&
        web3Provider.buttonText !== web3Provider.WALLET_STATES.CONNECTED && (
          <Center>
            <Button
              mt={20}
              colorScheme={
                web3Provider.buttonText === web3Provider.WALLET_STATES.CONNECTED
                  ? "orange"
                  : "orange"
              }
              onClick={web3Provider.onConnectWalletClick}
            >
              {web3Provider.buttonText}
              {"  "}
              <Image
                pl={2}
                h="24px"
                src="https://raw.githubusercontent.com/MetaMask/brand-resources/master/SVG/metamask-fox.svg"
              />
            </Button>
          </Center>
        )}
    </Flex>
  );
};

interface Preconnect {
  rel: string;
  href: string;
  as?: string;
}

export async function getStaticProps() {
  const assetPreload: Array<Preconnect> = assets
    ? Object.keys(assets).map((key) => {
        return {
          rel: "preload",
          href: assets[key],
          as: "image",
        };
      })
    : [];
  const preconnects: Array<Preconnect> = [
    { rel: "preconnect", href: "https://s3.amazonaws.com" },
  ];

  const preloads = assetPreload.concat(preconnects);

  return {
    props: { metaTags: DEFAULT_METATAGS, preloads },
  };
}

export default Homepage;
