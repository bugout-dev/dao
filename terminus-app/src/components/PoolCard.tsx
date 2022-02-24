import React, { FC, useContext } from "react";
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
  chakra,
  Fade,
  Input,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
} from "@chakra-ui/react";
import { TERMINUS_DIAMOND_ADDRESS } from "../AppDefintions";
import Web3Provider, { targetChain } from "../core/providers/Web3Provider";
import { FlexProps } from "@chakra-ui/react";
import RouteButton from "../components/RouteButton";
import useTerminus from "../core/hooks/useTerminus";
import useTerminusPool from "../core/hooks/useTerminusPool";
import Web3Context from "../core/providers/Web3Provider/context";

// intersecting
interface PoolCardProps extends FlexProps {
  poolId: string;
  hideOpen: boolean;
}

const STATES = {
  default: 0,
  URIArgs: 1,
  mintArgs: 2,
  poolControllerArgs: 3,
};
const PoolCard: FC<PoolCardProps> = ({ poolId, hideOpen, ...props }) => {
  const web3Provider = useContext(Web3Context);
  const [state, setState] = React.useState(STATES.default);
  const [argument, setArgument] = React.useState<any>("");
  const terminus = useTerminus({
    DiamondAddress: TERMINUS_DIAMOND_ADDRESS,
    targetChain: targetChain,
  });
  const handleArgumentChange = (event: any) => setArgument(event.target.value);
  const handleArgumentAddressChange = (event: any) =>
    setArgument((current: any) => {
      return { ...current, address: event.target.value };
    });
  const handleArgumentAmountChange = (value: any) =>
    setArgument((current: any) => {
      return { ...current, amount: value };
    });

  const terminusPool = useTerminusPool({
    DiamondAddress: TERMINUS_DIAMOND_ADDRESS,
    poolId,
    targetChain,
  });

  return (
    <Flex {...props} px={[2, "20px", "40px"]}>
      <Badge variant="subtle" colorScheme={"blue"}>
        Pool ID: #{poolId}
      </Badge>
      <Spacer />
      {state === STATES.URIArgs && (
        <Fade
          in={state === STATES.URIArgs ? true : false}
          style={{ width: "100%" }}
        >
          <Flex w="100%" justifyContent="center" px={20} alignItems="baseline">
            <Input
              value={argument}
              onChange={handleArgumentChange}
              placeholder="New terminus pool uri"
              size="md"
              fontSize={"sm"}
              w="100%"
              variant={"outline"}
              minW="420px"
            />
            <Button
              variant={"solid"}
              colorScheme={"orange"}
              onClick={() =>
                terminus.setPoolURI
                  .mutateAsync({
                    poolId: poolId,
                    newURI: argument,
                  })
                  .then(() => {
                    setState(STATES.default);
                    setArgument("");
                  })
              }
              isLoading={terminus.setPoolURI.isLoading}
            >
              Submit
            </Button>
            <Button
              variant={"solid"}
              colorScheme={"orange"}
              onClick={() => setState(STATES.default)}
            >
              Cancel
            </Button>
          </Flex>
        </Fade>
      )}
      {state === STATES.poolControllerArgs && (
        <Fade
          in={state === STATES.poolControllerArgs ? true : false}
          style={{ width: "100%" }}
        >
          <Flex w="100%" justifyContent="center" px={20} alignItems="baseline">
            <Input
              value={argument}
              onChange={handleArgumentChange}
              placeholder="New terminus pool controller address"
              size="md"
              fontSize={"sm"}
              w="100%"
              variant={"outline"}
              minW="420px"
            />
            <Button
              variant={"solid"}
              colorScheme={"orange"}
              onClick={() =>
                terminusPool.setPoolController
                  .mutateAsync({
                    newController:
                      web3Provider.web3.utils.toChecksumAddress(argument),
                  })
                  .then(() => {
                    setState(STATES.default);
                    setArgument("");
                  })
              }
              isLoading={terminusPool.setPoolController.isLoading}
            >
              Submit
            </Button>
            <Button
              variant={"solid"}
              colorScheme={"orange"}
              onClick={() => setState(STATES.default)}
            >
              Cancel
            </Button>
          </Flex>
        </Fade>
      )}
      {state === STATES.default && (
        <>
          <Badge
            colorScheme={"orange"}
            variant="outline"
            fontSize={"16px"}
            size="md"
          >
            Issued tokens: {terminusPool.terminusFacetCache.data?.supply} /{" "}
            {terminusPool.terminusFacetCache.data?.capacity}
          </Badge>
          <Spacer />
          <Button
            colorScheme={"blue"}
            variant="solid"
            size="sm"
            onClick={() => setState(STATES.URIArgs)}
          >
            Set URI
          </Button>
          <Button
            colorScheme={"blue"}
            variant="solid"
            size="sm"
            onClick={() => setState(STATES.mintArgs)}
          >
            Mint new
          </Button>
          <Button
            colorScheme={"blue"}
            variant="solid"
            size="sm"
            onClick={() => setState(STATES.poolControllerArgs)}
          >
            Transfer controller
          </Button>
          {!hideOpen && (
            <RouteButton
              variant="outline"
              colorScheme="green"
              size="sm"
              href={`/${poolId}`}
            >
              Open
            </RouteButton>
          )}
        </>
      )}
      {state === STATES.mintArgs && (
        <Fade
          in={state === STATES.mintArgs ? true : false}
          style={{ width: "100%" }}
        >
          <Flex w="100%" alignItems="center" px={20}>
            <Input
              value={argument.address}
              onChange={handleArgumentAddressChange}
              placeholder="Addres to mint for"
              size="md"
              fontSize={"sm"}
              w="100%"
              variant={"outline"}
              minW="420px"
            />
            <NumberInput
              defaultValue={0}
              onChange={handleArgumentAmountChange}
              value={argument.amount}
              size="md"
              mx={2}
              isDisabled={terminus.withrawPayments.isLoading}
            >
              <NumberInputField />
              <NumberInputStepper>
                <NumberIncrementStepper />
                <NumberDecrementStepper />
              </NumberInputStepper>
            </NumberInput>
            <Button
              variant={"solid"}
              colorScheme={"orange"}
              onClick={() =>
                terminusPool.mintPoolNFTMutation
                  .mutateAsync({
                    poolId: poolId,
                    address: web3Provider.web3.utils.toChecksumAddress(
                      argument.address
                    ),
                    amount: argument.amount,
                  })
                  .then(() => {
                    setState(STATES.default);
                    setArgument("");
                  })
              }
              isLoading={terminusPool.mintPoolNFTMutation.isLoading}
            >
              Submit
            </Button>
            <Button
              variant={"solid"}
              colorScheme={"orange"}
              onClick={() => setState(STATES.default)}
            >
              Cancel
            </Button>
          </Flex>
        </Fade>
      )}
    </Flex>
  );
};
export default chakra(PoolCard, {
  baseStyle: {
    w: "100%",
    h: "auto",
    bgColor: "purple.900",
    borderRadius: "lg",
    my: 2,
    maxW: "1337px",
    placeContent: "center",
    py: 2,
  },
});
