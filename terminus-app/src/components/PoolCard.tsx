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
import { TERMINUS_DIAMOND_ADDRESS } from "../AppDefintions";
import { targetChain } from "../core/providers/Web3Provider";
import UIContext from "../core/providers/UIProvider/context";
import useTerminusPool from "../core/hooks/useTerminusPool";
import Web3Context from "../core/providers/Web3Provider/context";

const PoolCard = ({ poolId }: { poolId: string }) => {
  const ui = useContext(UIContext);

  const terminusPool = useTerminusPool({
    DiamondAddress: TERMINUS_DIAMOND_ADDRESS,
    targetChain,
    poolId: poolId,
  });

  if (terminusPool.terminusFacetCache.isLoading) return <Spinner />;
  return (
    <Center>
      <Flex
        w="100%"
        h="3rem"
        bgColor="purple.900"
        borderRadius={"lg"}
        mt={2}
        maxW="1337px"
        placeContent={"center"}
      >
        <Text>{terminusPool.terminusFacetCache.data?.capacity}</Text>
        <Text>{terminusPool.terminusFacetCache.data?.supply}</Text>
        <Text>{terminusPool.terminusFacetCache.data?.uri}</Text>
      </Flex>
    </Center>
  );
};

export default PoolCard;
