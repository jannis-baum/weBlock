const TITLE_CENSOR = 'censor'
const TITLE_REPLACE = 'replace'

function initializePageAction(tab) {
    function protocolIsApplicable(url) {
        const protocol = (new URL(url)).protocol;
        return ["http:", "https:"].includes(protocol);
    }
    if (protocolIsApplicable(tab.url)) {
        browser.pageAction.setIcon({ tabId: tab.id, path: 'icons/icon.svg' });
        browser.pageAction.setTitle({ tabId: tab.id, title: TITLE_CENSOR });
        browser.pageAction.show(tab.id);
        browser.tabs.executeScript(tab.id, { file: 'censor.js'})
    }
}

browser.tabs.query({}).then((tabs) => {
    for (let tab of tabs) initializePageAction(tab);
});
browser.tabs.onUpdated.addListener((id, changeInfo, tab) => initializePageAction(tab));
browser.pageAction.onClicked.addListener((tab) => {
    browser.pageAction.getTitle({tabId: tab.id}).then((title) => {
        if (title == TITLE_CENSOR) {
            browser.pageAction.setTitle({tabId: tab.id, title: TITLE_REPLACE});
            browser.tabs.executeScript(tab.id, { code: 'censor_page();'})
        }
        else {
            browser.pageAction.setTitle({tabId: tab.id, title: TITLE_CENSOR});
            browser.tabs.executeScript(tab.id, { code: 'edit_page(original_page); censor_page(true);'})
        }
    })
});

