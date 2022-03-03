import React from "react";
import { getLayout, getLayoutProps } from "../src/layouts/InfoPageLayout";

const _PageWithBackground_template = () => {
  return <></>;
};

_PageWithBackground_template.getLayout = getLayout;

export async function getStaticProps() {
  const metaTags = {
    title: "TITLE HERE",
    description: "DESCRIPTION HERE",
    keywords: "word1, word2, word3",
    url: "URL HERE",
  };
  const layoutProps = getLayoutProps();
  //if you want to use default metatags, then just dont pass metaTags object in to layoutProps.props.metaTags
  layoutProps.props.metaTags = { ...layoutProps.props.metaTags, ...metaTags };
  return { ...layoutProps };
}
export default _PageWithBackground_template;
