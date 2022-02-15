import React from "react";
import { getLayout } from "../src/layouts/RootLayout";
import { DEFAULT_METATAGS } from "../src/core/constants";
import RedocComponent from "../src/components/RedocComponent";

const Docs = () => {
  return <RedocComponent specUrl={`https://api.moonstream.to/openapi.json`} />;
};

export async function getStaticProps() {
  const metaTags = {
    title: "Moonstream: API Documentation",
    description: "API Documentation to use moonstream.to",
    keywords: "API, docs",
    url: "https://www.moonstream.to/docs",
  };
  return { props: { metaTags: { ...DEFAULT_METATAGS, ...metaTags } } };
}

Docs.getLayout = getLayout;
export default Docs;
