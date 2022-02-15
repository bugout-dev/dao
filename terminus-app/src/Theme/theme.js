import { extendTheme } from "@chakra-ui/react";
import Button from "./Button";
import Tag from "./Tag";
import Menu from "./Menu";
import Input from "./Input";
// import Spinner from "./Spinner";
import NumberInput from "./NumberInput";
import Badge from "./Badge";
import Checkbox from "./Checkbox";
import Table from "./Table";
import Tooltip from "./Tooltip";
import Spinner from "./Spinner";
import Heading from "./Heading";
import { createBreakpoints } from "@chakra-ui/theme-tools";

const breakpointsCustom = createBreakpoints({
  sm: "24em", //Mobile phone
  md: "64em", //Tablet or rotated phone
  lg: "89.9em", //QHD
  xl: "160em", //4k monitor
  "2xl": "192em", // Mac Book 16" and above
});

const Accordion = {
  parts: ["container", "panel", "button"],
  baseStyle: {
    container: { borderColor: "white.300" },
    panel: { pb: 4 },
  },
};

const theme = extendTheme({
  breakpoints: breakpointsCustom,
  config: {
    initialColorMode: "light",
  },
  styles: {
    global: {
      body: {
        color: "gray.300",
      },
    },
  },

  components: {
    Button,
    Accordion,
    Menu,
    Input,
    Tag,
    NumberInput,
    Badge,
    Checkbox,
    Table,
    Spinner,
    Tooltip,
    Heading,
  },

  fonts: {
    heading: '"Virgil", sans-serif',
    body: '"Body Virgil", sans-serif',
    mono: '"Virgil", monospace',
  },
  fontSizes: {
    xs: "0.625rem", //10px
    sm: "0.875rem", //14px
    md: "1rem", //16px
    lg: "1.25rem", //20px
    xl: "1.375rem", //22
    "2xl": "1.5rem", //24px
    "3xl": "1.625rem", //26
    "4xl": "1.875rem", //30px
    "5xl": "2.625rem", //42px
    "6xl": "3.75rem", //60px
    "7xl": "4.5rem", //72px
  },

  colors: {
    blue: {
      0: "#FFFFFFFF",
      50: "#e7f1ff",
      100: "#cfe2ff",
      200: "#b6d4fe",
      300: "#9ec5fe",
      400: "#86b7fe",
      500: "#6ea8fe",
      600: "#569afe",
      700: "#3d8bfd",
      800: "#257dfd",
      900: "#0d6efd",
      1000: "#0d6efd",
      1100: "#0c63e4",
      1200: "#0c63e4",
      1300: "#0a58ca",
      1400: "#094db1",
      1500: "#084298",
      1600: "#07377f",
      1700: "#052c65",
      1800: "#04214c",
      1900: "#010b19",
      2000: "#000000",
    },

    purple: {
      0: "#FFFFFFFF",
      50: "##f1ecf9",
      100: "##e2d9f3",
      200: "##d4c6ec",
      300: "##c5b3e6",
      400: "##b7a1e0",
      500: "##a98eda",
      600: "#9a7bd4",
      700: "##8c68cd",
      800: "#7d55c7",
      900: "#6f42c1",
      1000: "#6f42c1",
      1100: "#643bae",
      1200: "#59359a",
      1300: "#4e2e87",
      1400: "#382161",
      1500: "#21143a",
      1600: "#160d27",
    },

    gray: {
      0: "#FFFFFFFF",
      50: "#f7f8fa",
      100: "#f8f9fa",
      200: "#e9ecef",
      300: "#dee2e6",
      400: "#ced4da",
      500: "#adb5bd",
      600: "#495057",
      700: "#343a40",
      800: "#343a40",
      900: "#212529",
      1000: "#9ca7b6",
      1100: "#8a94a2",
      1200: "#79828d",
      1300: "#686f79",
      1400: "#575d65",
      1500: "#454a51",
      1600: "#34373d",
    },
    white: {
      100: "#FFFFFF",
      200: "#F7F8FB",
      300: "#EAEBF7",
    },
    red: {
      0: "#FFFFFFFF",
      50: "#fcebec",
      100: "#f8d7da",
      200: "#f5c2c7",
      300: "#f1aeb5",
      400: "#ee9aa2",
      500: "#ea868f",
      600: "#e7727d",
      700: "#e35d6a",
      800: "#e04958",
      900: "#dc3545",
    },

    yellow: {
      0: "#FFFFFFFF",
      50: "#fff9e6",
      100: "#fff3cd",
      200: "#ffecb5",
      300: "#ffe69c",
      400: "#ffe083",
      500: "#ffda6a",
      600: "#ffd451",
      700: "#ffcd39",
      800: "#ffc720",
      900: "#ffc107",
    },
    orange: {
      0: "#FFFFFFFF",
      50: "#fff2e8",
      100: "#ffe5d0",
      200: "#fed8b9",
      300: "#fecba1",
      400: "#febf8a",
      500: "#feb272",
      600: "#fea55b",
      700: "#fd9843",
      800: "#fd8b2c",
      900: "#fd7e14",
    },

    green: {
      0: "#FFFFFFFF",
      50: "#e8f3ee",
      100: "#d1e7dd",
      200: "#badbcc",
      300: "#a3cfbb",
      400: "#8cc3aa",
      500: "#75b798",
      600: "#5eab87",
      700: "#479f76",
      800: "#309365",
      900: "#198754",
      1000: "#198754",
      1100: "#177a4c",
      1200: "#146c43",
      1300: "#125f3b",
      1400: "#0f5132",
      1500: "#0d442a",
      1600: "#0a3622",
    },

    black: {
      100: "#333399",
      200: "#111442",
    },
  },
});

export default theme;
