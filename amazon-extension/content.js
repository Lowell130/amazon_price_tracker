console.log("content.js caricato sulla pagina:", window.location.href);

function extractAsinFromUrl(url) {
    const asinMatch = url.match(/\/([A-Z0-9]{10})(?:[/?]|$)/i);
    return asinMatch ? asinMatch[1].toUpperCase() : null;
}

function cleanPriceText(priceText) {
    if (!priceText) return null;
    let price = priceText.replace(/[^\d,\.]/g, "");
    if (price.includes(",") && price.includes(".")) {
        if (price.indexOf(",") > price.indexOf(".")) {
            price = price.replace(/\./g, "").replace(",", ".");
        } else {
            price = price.replace(/,/g, "");
        }
    } else if (price.includes(",")) {
        price = price.replace(",", ".");
    }
    return parseFloat(price) || null;
}

function extractPrice() {
    const selectors = [
        "#corePrice_feature_div .a-offscreen",
        "#corePriceDisplay_desktop_feature_div .a-offscreen",
        "#corePrice_desktop .a-offscreen",
        ".apexPriceToPay .a-offscreen",
        "#priceblock_ourprice",
        "#priceblock_dealprice"
    ];
    for (let selector of selectors) {
        const el = document.querySelector(selector);
        if (el) {
            const price = cleanPriceText(el.innerText);
            if (price) return price;
        }
    }
    return null;
}

function extractAvailability() {
    const outOfStockEl = document.querySelector("#outOfStock, #availability span.a-color-error");
    if (outOfStockEl && (outOfStockEl.innerText.includes("Non disponibile") || outOfStockEl.innerText.includes("Attualmente non disponibile"))) {
        return "Non disponibile";
    }
    return "Disponibile";
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "getProductUrl") {
        const url = window.location.href;
        const asin = extractAsinFromUrl(url);
        const price = extractPrice();
        const availability = extractAvailability();

        sendResponse({
            product_url: url,
            asin: asin,
            price: price,
            availability: availability
        });

        return true;
    }
});
