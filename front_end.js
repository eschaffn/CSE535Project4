let mystring = '[{"Response": "JESUS EU QUERO MORDER A STEFHANY"}, {"Response": "Fl\u00fcchtling m\u00fcsste man sein keine Probleme,die kriegen alles in den A...geblasen"}, {"Response": "@SPIEGELONLINE Blo\u00df weil jemand von A nach B will, ist er noch lange nicht automatisch \"#Fl\u00fcchtling\". Aber die dt. #Goebbels-#Medien eben..."}, {"Response": "#Kultura: \"Lotsagarria, zentzurik gabekoa, sinestezina\": Imanol Uribek \"Lejos del Mar\" filma a... http://t.co/PTIcb2DtxS via @naiz_info."}]'
function sendQueryCallback(response){
    let j = JSON.parse(response)
    var mainContainer = document.getElementById("results");
    mainContainer.innerHTML = ''
    var n = 1
    for (var i = 0; i < j.length; i++) {
        var div = document.createElement("div")
        div.classList.add("results")
        div.innerHTML = 'Response ' + n + ': \n' + j[i].Response
        mainContainer.appendChild(div);
        n +=1
      }
};


function sendQuery(){
    let query = document.getElementById("searchbar").value;

    document.getElementById("searchbar").value = "";

    let data = {"query": query};
    data = JSON.stringify(data);
    ajaxPostRequest("/search", data, sendQueryCallback);
};
