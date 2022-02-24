import React, { Fragment, useContext } from "react";
import RouterLink from "next/link";
import {
  Button,
  Image,
  ButtonGroup,
  Spacer,
  Link,
  IconButton,
  Flex,
  Badge,
  Text,
  Spinner,
} from "@chakra-ui/react";
import { HamburgerIcon } from "@chakra-ui/icons";
import useModals from "../core/hooks/useModals";
import UIContext from "../core/providers/UIProvider/context";
import ChakraAccountIconButton from "./AccountIconButton";
import RouteButton from "./RouteButton";
import {
  ALL_NAV_PATHES,
  APP_ENTRY_POINT,
  IS_AUTHENTICATION_REQUIRED,
  WHITE_LOGO_W_TEXT_URL,
} from "../core/constants";
import router from "next/router";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";
import Web3Context from "../core/providers/Web3Provider/context";
import { TERMINUS_DIAMOND_ADDRESS } from "../AppDefintions";
import { targetChain } from "../core/providers/Web3Provider";
import useTerminus from "../core/hooks/useTerminus";

const LandingNavbar = () => {
  const ui = useContext(UIContext);
  const { toggleModal } = useModals();
  const web3Provider = useContext(Web3Context);
  const terminus = useTerminus({
    DiamondAddress: TERMINUS_DIAMOND_ADDRESS,
    targetChain: targetChain,
  });
  return (
    <>
      {ui.isMobileView && (
        <>
          <IconButton
            alignSelf="flex-start"
            colorScheme="blue"
            variant="solid"
            onClick={() => ui.setSidebarToggled(!ui.sidebarToggled)}
            icon={<HamburgerIcon />}
          />
        </>
      )}
      <Flex
        pl={ui.isMobileView ? 2 : 8}
        justifySelf="flex-start"
        h="100%"
        py={1}
        flexBasis="200px"
        flexGrow={1}
        id="Logo Container"
      >
        <RouterLink href="/" passHref>
          <Link
            as={Image}
            w="auto"
            h="full"
            justifyContent="left"
            src={WHITE_LOGO_W_TEXT_URL}
            alt="Logo"
          />
        </RouterLink>
      </Flex>

      {!ui.isMobileView && (
        <>
          <Spacer />
          <ButtonGroup variant="solid" spacing={4} pr={16}>
            {web3Provider.buttonText !==
              web3Provider.WALLET_STATES.CONNECTED && (
              <Button
                colorScheme={
                  web3Provider.buttonText ===
                  web3Provider.WALLET_STATES.CONNECTED
                    ? "green"
                    : "green"
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
            )}
            {web3Provider.buttonText ===
              web3Provider.WALLET_STATES.CONNECTED && (
              <Flex>
                <Badge
                  colorScheme={"pink"}
                  variant={"solid"}
                  fontSize={"md"}
                  borderRadius={"md"}
                  mr={2}
                >
                  <Flex>
                    <Image
                      ml={2}
                      h="22px"
                      src="https://darkforest.cryptounicorns.fun/static/media/icon_milk.6fc3d44e.png"
                    />
                    {terminus.terminusPaymentTokenCache?.data?.balance ? (
                      <Text mx={2} display={"inline-block"}>
                        Your balance:{" "}
                        {web3Provider.web3.utils.fromWei(
                          terminus.terminusPaymentTokenCache.data.balance,
                          "ether"
                        )}
                      </Text>
                    ) : (
                      <Spinner m={0} size="xs" />
                    )}
                  </Flex>
                </Badge>
                {web3Provider.account ===
                  terminus.terminusFacetCache.data?.controller && (
                  <Badge
                    colorScheme={"pink"}
                    variant={"solid"}
                    fontSize={"md"}
                    borderRadius={"md"}
                    mr={2}
                  >
                    <Flex>
                      <Image
                        ml={2}
                        h="22px"
                        src="https://darkforest.cryptounicorns.fun/static/media/icon_milk.6fc3d44e.png"
                      />
                      {terminus.terminusPaymentTokenCache?.data
                        ?.spenderBalance ? (
                        <Text mx={2} display={"inline-block"}>
                          Terminus contract balance:{" "}
                          {web3Provider.web3.utils.fromWei(
                            terminus.terminusPaymentTokenCache.data
                              .spenderBalance,
                            "ether"
                          )}
                        </Text>
                      ) : (
                        <Spinner m={0} size="xs" />
                      )}
                    </Flex>
                  </Badge>
                )}
                <Badge
                  colorScheme={"green"}
                  variant={"solid"}
                  fontSize={"md"}
                  borderRadius={"md"}
                >
                  {web3Provider.account ? (
                    `Connected: ${web3Provider.account}`
                  ) : (
                    <Spinner m={0} size={"xs"} />
                  )}
                </Badge>
              </Flex>
            )}
          </ButtonGroup>
          <ButtonGroup variant="link" colorScheme="orange" spacing={4} pr={16}>
            {ALL_NAV_PATHES.map((item, idx) => (
              <RouteButton
                key={`${idx}-${item.title}-landing-all-links`}
                variant="link"
                href={item.path}
                color="white"
                isActive={!!(router.pathname === item.path)}
              >
                {item.title}
              </RouteButton>
            ))}

            {ui.isLoggedIn ||
              (!IS_AUTHENTICATION_REQUIRED && APP_ENTRY_POINT && (
                <RouterLink href={APP_ENTRY_POINT} passHref>
                  <Button
                    as={Link}
                    colorScheme="orange"
                    variant="outline"
                    size="sm"
                    fontWeight="400"
                    borderRadius="2xl"
                  >
                    App
                  </Button>
                </RouterLink>
              ))}
            {!ui.isLoggedIn && IS_AUTHENTICATION_REQUIRED && (
              <Button
                colorScheme="orange"
                variant="solid"
                onClick={() => toggleModal({ type: MODAL_TYPES.SIGNUP })}
                size="sm"
                fontWeight="400"
                borderRadius="2xl"
              >
                Sign Up
              </Button>
            )}
            {!ui.isLoggedIn && IS_AUTHENTICATION_REQUIRED && (
              <Button
                color="white"
                onClick={() => toggleModal({ type: MODAL_TYPES.LOGIN })}
                fontWeight="400"
              >
                Log in
              </Button>
            )}
            {ui.isLoggedIn && IS_AUTHENTICATION_REQUIRED && (
              <ChakraAccountIconButton variant="link" colorScheme="orange" />
            )}
          </ButtonGroup>
        </>
      )}
      {ui.isLoggedIn && IS_AUTHENTICATION_REQUIRED && ui.isMobileView && (
        <>
          <Spacer />
          <ChakraAccountIconButton variant="link" colorScheme="orange" />
        </>
      )}
    </>
  );
};

export default LandingNavbar;
