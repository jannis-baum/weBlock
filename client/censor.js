var serverURL;
// ad-block
function guardian_block_ads() {
    for (ad of document.querySelectorAll("div[class*='ad-'], div[class*='ads-'], div[class='GoogleActiveViewElement'],  div[class*='-ad']")) {
        ad.parentNode.removeChild(ad);
    }
}

// censoring
function edit_page(data) {
    for (let tag in data) {
        elements = document.getElementsByTagName(tag);
        for (let n = 0; n < elements.length; n++) {
            elements[n].innerHTML = data[tag][n];
        }
    }
}

async function censor_page(replace_text = false) {
    guardian_block_ads();
    const relevant_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7'];

    function sendstring() {
        var page = {};
        for (tag of relevant_tags) {
            elements = document.getElementsByTagName(tag);
            list = [];
            for (element of elements) {
                list.push(element.innerHTML);
            }
            page[tag] = list;
        }
        return JSON.stringify({replace_text: replace_text, page: page});
    }

    document.documentElement.hidden = true;

    let getting = await browser.storage.local.get("serverUrl");
    const xhr = new XMLHttpRequest();
    let host = getting.serverUrl || "localhost"
    xhr.open("POST", "http://" + host + ":6969");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            data = JSON.parse(xhr.responseText);
            edit_page(data);
            document.documentElement.hidden = false;
        }
    };

    const s = sendstring();
    xhr.send(s);
    //
    return JSON.parse(s).page;
}

//
const original_page = censor_page();

