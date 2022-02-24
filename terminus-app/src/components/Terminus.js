import React, { useContext } from "react";
import { Flex, Spinner } from "@chakra-ui/react";
import { TERMINUS_DIAMOND_ADDRESS } from "../AppDefintions";

import { targetChain } from "../core/providers/Web3Provider";

import useTerminus from "../core/hooks/useTerminus";
import PoolCard from "./PoolCard";
import TerminusControllerPanel from "./TerminusControllerPanel";
import Web3Context from "../core/providers/Web3Provider/context";
import TerminusOwnerPanel from "./TerminusOwnerPanel";

const Terminus = () => {
  const terminus = useTerminus({
    DiamondAddress: TERMINUS_DIAMOND_ADDRESS,
    targetChain: targetChain,
  });

  const web3Provider = useContext(Web3Context);
  if (!terminus.terminusFacetCache.data?.totalPools) return <Spinner />;

  console.log(
    "terminus.terminusFacetCache.data.ownedPoolIds",
    terminus.terminusFacetCache.data.ownedPoolIds
  );
  return (
    <Flex
      w="100%"
      minH="100vh"
      direction={"column"}
      maxW="1337px"
      alignSelf={"center"}
    >
      {terminus.terminusFacetCache.data.controller === web3Provider.account && (
        <TerminusControllerPanel
          borderRadius={"md"}
          my={2}
          bgColor="blue.600"
          py={4}
        />
      )}
      {terminus.terminusFacetCache.data.owner === web3Provider.account && (
        <TerminusOwnerPanel
          borderRadius={"md"}
          my={2}
          bgColor="blue.600"
          py={4}
        />
      )}
      <Flex w="100%" direction="column">
        {terminus.terminusFacetCache.data.ownedPoolIds.map((i) => (
          <PoolCard
            alignItems={"baseline"}
            // mx={["20px", "7%", null, "7%"]}
            maxW="1337px"
            key={`pool-${i}`}
            poolId={String(i)}
            bgColor="blue.500"
          />
        ))}
      </Flex>
    </Flex>
  );
};

export default Terminus;
