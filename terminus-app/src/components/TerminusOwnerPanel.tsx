import React, { FC } from "react";
import { Flex, Button, chakra, Stack, Input, Fade } from "@chakra-ui/react";
import { TERMINUS_DIAMOND_ADDRESS } from "../AppDefintions";
import { targetChain } from "../core/providers/Web3Provider";
import { FlexProps } from "@chakra-ui/react";
import useTerminus from "../core/hooks/useTerminus";

const STATES = {
  buttons: 0,
  transferOwnershipArgs: 1,
};
const TerminusOwnerPanel: FC<FlexProps> = (props) => {
  const terminus = useTerminus({
    DiamondAddress: TERMINUS_DIAMOND_ADDRESS,
    targetChain: targetChain,
  });

  const [state, setState] = React.useState(STATES.buttons);
  const [newOwner, setNewOwnerField] = React.useState("");
  const handleNewOwnerFieldChange = (event: any) =>
    setNewOwnerField(event.target.value);

  return (
    <Flex {...props}>
      <Stack direction={"column"} w="100%">
        <Flex justifyContent={"center"} fontWeight="600" textColor={"blue.50"}>
          Pool owner panel
        </Flex>
        {state === STATES.buttons && (
          <Fade in={state === STATES.buttons ? true : false}>
            <Flex w="100%" justifyContent="space-evenly">
              <Button
                variant={"solid"}
                colorScheme={"orange"}
                onClick={() => setState(STATES.transferOwnershipArgs)}
              >
                Transfer ownership
              </Button>
            </Flex>
          </Fade>
        )}
        {state === STATES.transferOwnershipArgs && (
          <Fade in={state === STATES.transferOwnershipArgs ? true : false}>
            <Flex
              w="100%"
              justifyContent="center"
              px={20}
              alignItems="baseline"
            >
              <Input
                value={newOwner}
                onChange={handleNewOwnerFieldChange}
                placeholder="New terminus owner address"
                size="md"
                maxW="420px"
                fontSize={"sm"}
              />
              <Button
                variant={"solid"}
                colorScheme={"orange"}
                onClick={() =>
                  terminus.transferTerminusOwnershipMutation.mutate({
                    newOwner: newOwner,
                  })
                }
                isLoading={terminus.transferTerminusOwnershipMutation.isLoading}
              >
                Submit
              </Button>
              <Button
                variant={"solid"}
                colorScheme={"orange"}
                onClick={() => setState(STATES.buttons)}
              >
                Cancel
              </Button>
            </Flex>
          </Fade>
        )}
      </Stack>
    </Flex>
  );
};
export default chakra(TerminusOwnerPanel, {
  baseStyle: {
    w: "100%",
    direction: "row",
    bgColor: "red.100",
    boxShadow: "revert",
  },
});
