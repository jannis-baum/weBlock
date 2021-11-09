const xhr = new XMLHttpRequest();
xhr.open("GET", 'http://saltleague.net:6969');

xhr.onreadystatechange = function () {
   if (xhr.readyState === 4) {
      console.log(xhr.status);
      console.log(xhr.responseText);
   }};

xhr.send();

