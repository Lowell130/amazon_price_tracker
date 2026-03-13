console.log("content.js caricato sulla pagina:", window.location.href);

function extractAsinFromUrl(url) {
    // Pattern base per /dp/ASIN/, /gp/product/ASIN, ecc.
    const asinMatch = url.match(/\/([A-Z0-9]{10})(?:[/?]|$)/i);
    return asinMatch ? asinMatch[1].toUpperCase() : null;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "getProductUrl") {
        const url = window.location.href;
        const asin = extractAsinFromUrl(url);

        sendResponse({
            product_url: url,
            asin: asin,
        });

        return true;
    }
});
