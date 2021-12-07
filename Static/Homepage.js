function sendQueryCallback(response){
    let j = JSON.parse(response)
    var mainContainer = document.getElementById("results");
    var analysisContainer = document.getElementById("analytics");
    var map_container = document.getElementById("map_container");
    var bar_container = document.getElementById("bar_container");

    mainContainer.innerHTML = '';
    analysisContainer.innerHTML = '';

    var n = 1;
    var usernames = [];
    var topics = [];
    var texts = [];
    var lonList = [];
    var latList = [];
    var colorList = [];





    for (var i = 0; i < j.length - 1; i++) {
        
        var result_container = document.createElement("div"); 
        result_container.classList.add("results_container2");

        var SET_container = document.createElement("div"); SET_container.classList.add("SET_container")

        // var translateButton = document.createElement("div"); translateButton.classList.add("translateButton");
        var responseCounter = document.createElement("div"); responseCounter.classList.add("responseCounter");
        var username = document.createElement("div"); username.classList.add("username");
        var tweet_url = document.createElement("div"); tweet_url.classList.add("tweet_url");
        var tweet_text = document.createElement("div"); tweet_text.classList.add("tweet_text");
        var num_likes_retweets = document.createElement("div"); num_likes_retweets.classList.add("num_likes_retweets");
        var resultTopics = document.createElement("div"); resultTopics.classList.add("resultTopics");
        var resultEmotions = document.createElement("div"); resultEmotions.classList.add("resultTopics");
        var resultSentiment = document.createElement("div"); 


        // translateButton.innerHTML = '<button onclick="translateTweet();" id="translateButton" class="translateButton">Show Original Language</a>'; result_container.appendChild(translateButton)

        var R = j[i].Response;
        usernames.push(R.username); texts.push(R.map_text);topics.push(R.topics); latList.push(R.lat);lonList.push(R.lon);colorList.push(R.colors);


        responseCounter.innerHTML = 'Response ' + n + '<br>'; responseCounter.id = 'responseCounter'; result_container.appendChild(responseCounter);
        username.innerHTML = '@' + R.username + '<br>'; result_container.appendChild(username);
        tweet_url.innerHTML = '<a target = "_blank" href =' + R.tweet_url + '>' + R.tweet_url + '</a>'; result_container.appendChild(tweet_url);
        if(R.original_text == R.text){
            tweet_text.innerHTML = R.text;
            result_container.appendChild(tweet_text);
        }

        else{
            var original_text = document.createElement("div")
            original_text.classList.add("original_text")
            tweet_text.innerHTML = 'Translated Text:    ' + R.text
            result_container.appendChild(tweet_text)
            original_text.innerHTML = 'Original Text:    ' + R.original_text 
            result_container.appendChild(original_text)
        

        };
        if(R.sentiment == 'Negative') {resultSentiment.classList.add('negative_sentiment')}
        else if(R.sentiment == 'Positive') {resultSentiment.classList.add('positive_sentiment')}
        else {resultSentiment.classList.add('neutral_sentiment')};

        resultSentiment.innerHTML = 'Detected Sentiment:    ' + R.sentiment; SET_container.appendChild(resultSentiment);

        resultTopics.innerHTML = 'Tweet Topics:   ' + R.topics; SET_container.appendChild(resultTopics);
        resultEmotions.innerHTML = 'Detected Emotions:    ' + R.emotion; SET_container.appendChild(resultEmotions)
        result_container.appendChild(SET_container)
        num_likes_retweets.innerHTML = '❤️: ' + R.num_likes + '   '+'    🔁:  ' + R.num_retweets; result_container.appendChild(num_likes_retweets);


        mainContainer.appendChild(result_container);
        analysisContainer.appendChild(map_container);
        analysisContainer.appendChild(bar_container);
    
        
        n +=1
      }
      var bardata = j[j.length - 1].topic_bar_data;
      var barlayout = {
          paper_bgcolor: 'rgba(0,0,0,0)',
          plot_bgcolor: 'rgba(0,0,0,0)',
          title: 'Distribution of Topics in Results',
          font: {
            family: 'Trebuchet MS, sans-serif',
            size: 10, 
            color: 'white'
          },
          titlefont: {
            family: 'Trebuchet MS, sans-serif',
            size: 16, 
            color: 'white'
          }
      }
      var mapdata = [{
          type: 'scattergeo',
          mode: 'markers',
          text: texts,
          lon: lonList,
          lat: latList,
          marker: {
              size: 7,
              color: colorList
          },

      }]
      var maplayout = { 
          title: 'Geographic Distribution of Tweets',
          paper_bgcolor: 'rgba(0,0,0,0)',
          font: {
            family: 'Trebuchet MS, sans-serif',
            size: 6
            },
            titlefont: {
                family: 'Trebuchet MS, sans-serif',
                size: 16,
                color: 'white'
            },
            geo: {
                scope: 'world',
                showcountries: true,
                countrycolor: '#000000',
                bgcolor: 'rgba(0,0,0,0)',
                showland: true,
                landcolor: 'rgb(97, 171, 75)',
                showocean: true,
                oceancolor: 'rgb(71, 115, 191)',
                showlakes: true,
                lakecolor: 'rgb(71, 115, 191)',
                showrivers: true,
                rivercolor: 'rgb(71, 115, 191)'
                            
            }
    
      }


      Plotly.newPlot('map_container', mapdata, maplayout)
      Plotly.newPlot('bar_container', bardata, barlayout)

};


function sendQuery(){
    let query = document.getElementById("searchbar").value;
    let RTfilterparams = document.getElementById("retweetFilter").value;
    let langfilterparams = document.getElementById("LangFilter").value;

    document.getElementById("searchbar").value = "";

    let data = {
        "query": query, 
        "RTfilterparams": RTfilterparams, 
        "langfilterparams": langfilterparams
};

    data = JSON.stringify(data);
    ajaxPostRequest("/search", data, sendQueryCallback);
};

// function translateTweetCallback(){



// };

// function translateTweet(){
//     let responseN = document.getElementById("responseCounter");

//     let data = {
//         "responseN": responseN
//     }
//     data = JSON.stringify(data)
//     ajaxPostRequest("/translate", data, translateTweetCallback);
// };



// function loadResults(){
//     var source = document.getElementById('homepage')
//     var dest = document.getElementById("results2")
//     var h = source.contentWindow.document.getElementById('results')
//     var x = document.adoptNode(h)
//     dest.appendChild(x)
    
// };