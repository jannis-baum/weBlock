const relevant_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7'];

function sendstring() {
   var dict = {};
   for (tag of relevant_tags) {
      elements = document.getElementsByTagName(tag);
      list = [];
      for (element of elements) {
         list.push(element.innerHTML);
      }
      dict[tag] = list;
   }
   return JSON.stringify(dict);
}

function edit_page(data) {
   for (let tag in data) {
      elements = document.getElementsByTagName(tag);
      for (let n = 0; n < elements.length; n++) {
         elements[n].innerHTML = data[tag][n];
      }
   }
}

document.documentElement.hidden = true;

const xhr = new XMLHttpRequest();
xhr.open("POST", 'http://saltleague.net:6969');
xhr.onreadystatechange = function () {
   if (xhr.readyState === 4) {
      data = JSON.parse(xhr.responseText);
      edit_page(data);
      document.documentElement.hidden = false;
   }
};

xhr.send(sendstring());

