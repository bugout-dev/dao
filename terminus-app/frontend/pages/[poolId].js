import React, { useContext } from "react";
import { Flex, Spinner, Td, Tr, Table, Thead } from "@chakra-ui/react";
import { TERMINUS_DIAMOND_ADDRESS } from "../src/AppDefintions";
import { targetChain } from "../src/core/providers/Web3Provider";
import { useRouter } from "../src/core/hooks";
import useTerminusPool from "../src/core/hooks/useTerminusPool";
import Web3Context from "../src/core/providers/Web3Provider/context";
import PoolCard from "../src/components/PoolCard";

const TerminusPoolControlPage = () => {
  const router = useRouter();

  const { poolId } = router.params;

  const terminusPool = useTerminusPool({
    DiamondAddress: TERMINUS_DIAMOND_ADDRESS,
    targetChain,
    poolId: poolId,
  });

  const web3provider = useContext(Web3Context);

  // const handleClick = () => {
  //   terminusPool.mintPoolNFTMutation.mutate({
  //     address: `0xb4231b174a09d3510d75197C6de391ad97702116`,
  //     amount: 1,
  //     poolId: poolId,
  //   });
  // };

  if (terminusPool.terminusFacetCache.isLoading) return <Spinner />;

  return (
    <Flex
      w="100%"
      // px={2}
      // maxW="1337px"
      minH="100vh"
      direction="column"
      placeSelf={"center"}
      px="20px"
    >
      {web3provider.account ===
        terminusPool.terminusFacetCache.data?.controller && (
        <PoolCard
          poolId={poolId}
          hideOpen
          w="100%"
          maxW="unset"
          borderTopRadius={0}
          mt={0}
          bgColor="blue.400"
        />
      )}
      <Table>
        <Thead>
          <Tr>
            <Td>Id</Td>
            <Td>Address</Td>
            <Td>Notes</Td>
            <Td>Actions</Td>
          </Tr>
        </Thead>
      </Table>
    </Flex>
  );
};

export default TerminusPoolControlPage;
