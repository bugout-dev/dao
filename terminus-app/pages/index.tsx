import React, { useContext } from "react";
import {
  Stack,
  Heading,
  Center,
  Flex,
  Badge,
  Image,
  Text,
  Spacer,
  Spinner,
  Button,
} from "@chakra-ui/react";
import { DEFAULT_METATAGS } from "../src/core/constants";
import { TERMINUS_DIAMOND_ADDRESS } from "../src/AppDefintions";

import { targetChain } from "../src/core/providers/Web3Provider";

import UIContext from "../src/core/providers/UIProvider/context";
import useTerminus from "../src/core/hooks/useTerminus";
import useTerminusPool from "../src/core/hooks/useTerminusPool";
import PoolCard from "../src/components/PoolCard";

const assets = {
  onboarding:
    "https://s3.amazonaws.com/static.simiotics.com/unicorn_bazaar/unim-onboarding.png",
};

const Homepage = () => {
  const ui = useContext(UIContext);
  const terminus = useTerminus({
    DiamondAddress: TERMINUS_DIAMOND_ADDRESS,
    targetChain: targetChain,
  });

  // const terminusPool1 = useTerminusPool({
  //   DiamondAddress: TERMINUS_DIAMOND_ADDRESS,
  //   targetChain,
  //   poolId: "74",
  // });

  if (!terminus.terminusFacetCache.data?.totalPools) return "";
  return (
    <>
      <Center w="100%" bgColor="blue.1200">
        <Button
          variant={"solid"}
          colorScheme={"yellow"}
          onClick={() => terminus.createPoolMutation.mutate("100")}
          isLoading={terminus.createPoolMutation.isLoading}
        >
          New Pool
        </Button>
      </Center>
      {terminus.terminusFacetCache.data?.ownedPoolIds.map((ownedPoolId) => (
        <PoolCard
          key={`ownedpool-${ownedPoolId}`}
          poolId={String(ownedPoolId)}
        />
      ))}
      <Stack />
    </>
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
