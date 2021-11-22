function edit_page(data) {
   const key_tag = 'tag';
   const key_edits = 'edits';
   const key_index = 'index';
   const key_innerHTML = 'innerHTML';

   for (let dict of data) {
      elements = document.getElementsByTagName(dict[key_tag]);
      for (edit of dict[key_edits]) {
         elements[edit[key_index]].innerHTML = edit[key_innerHTML];
      }
   }
}

document.documentElement.hidden = true;

const xhr = new XMLHttpRequest();
xhr.open("POST", 'http://saltleague.net:6969');
xhr.onreadystatechange = function () {
   if (xhr.readyState === 4) {
      console.log('status: ' + xhr.status);
      console.log('response: ' + xhr.responseText);
      data = JSON.parse(xhr.responseText);
      edit_page(data);
      document.documentElement.hidden = false;
   }
};
xhr.send(document.documentElement.innerHTML);

