function saveOptions(e) {
  e.preventDefault();
  browser.storage.local.set({
    serverUrl: document.querySelector("#serverUrl").value
  });
}

function restoreOptions() {

  function setCurrentChoice(result) {
    document.querySelector("#serverUrl").value = result.serverUrl || "localhost";
  }

  function onError(error) {
    console.log(`Error: ${error}`);
  }

  let getting = browser.storage.local.get("serverUrl");
  getting.then(setCurrentChoice, onError);
}

document.addEventListener("DOMContentLoaded", restoreOptions);
document.querySelector("form").addEventListener("submit", saveOptions);