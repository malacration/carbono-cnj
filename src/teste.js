function getElementByXpath(path) {
    console.log(document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue);
}

getElementByXpath("//*[contains(text(), 'Latência média na origem para')]"
    +"//ancestor::div[contains(@class, 'sn-kpi-data')][1]"
);


getElementByXpath("//span[contains(text(), 'Latência média na origem para o TJRO')]//ancestor::div[contains(@class, 'sn-kpi-data')]//span[last()]");

getElementByXpath("//span[contains(text(), 'Latência média na origem para o TJRO')]//ancestor::div[contains(@class, 'sn-kpi-data')]//span[contains(text(), '00:00:42.38')]");

getElementByXpath("//span[contains(text(), 'Latência média na origem')]//ancestor::div[contains(@class, 'sn-kpi ')]//div[contains(@class, 'sn-kpi-value')]//span[last()]");
