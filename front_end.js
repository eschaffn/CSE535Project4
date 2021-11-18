
function sendQueryCallback(response){
    let j = JSON.parse(response)
    var mainContainer = document.getElementById("results");
    n = 1
    for (var i = 0; i < j.length; i++) {
        // append each person to our page
        // var div = document.createElement("div");
        mainContainer = 'Response ' + n + ': \n' + j[i].Response
        // mainContainer.appendChild(div);
        n+=1
      }
};


function sendQuery(){
    let query = document.getElementById("searchbar").value;

    document.getElementById("searchbar").value = "";

    let data = {"query": query};
    data = JSON.stringify(data);
    ajaxPostRequest("/search", data, sendQueryCallback);
};
