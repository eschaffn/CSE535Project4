function plotsCallback(response){
var R = JSON.parse(response);



var pie = R.piechart_data
var sunburst = R.sunburst_data
var words_per_topic_container = document.getElementById('words_per_topic_container')
var words_per_topic = R.words_per_topic_data

var piedata = [{
    values: pie.values,
    labels: pie.labels,
    type: 'pie'
  }];

var pielayout = {
    title: 'Distribution of Emotions',
    height: 400,
    width: 500,
    paper_bgcolor: 'rgba(0, 0, 0, 0)',
    plot_bgcolor: 'rgba(0, 0, 0, 0)',
    font: {
        color: "white"
    }
}

var sunburstdata = sunburst
var sunburstlayout = {
    margin: {l: 0, r: 0, b: 0, t: 15},
    automargin: true,
    width: 500,
    height: 500,
    paper_bgcolor: 'rgba(0, 0, 0, 0)',
    plot_bgcolor: 'rgba(0, 0, 0, 0)',
    font: {
        color: "white"
    }
   }
var stackedbartrace1 = {
    y: ['US_POI', 'US_Public', 'Mex_POI', 'Mex_Public', 'India_POI', 'India_Public'],
    x: [1031, 4140, 1400, 3555, 735, 1275],
    name: 'Pro',
    orientation: 'h',
    type: 'bar',
    marker: {
        color: 'rgba(246, 78, 139, 0.6)',
        line: {
            color: 'rgba(246, 78, 139, 1.0)',
            width: 3
        }
    }
}
var stackedbartrace2 = {
    y: ['US_POI', 'US_Public', 'Mex_POI', 'Mex_Public', 'India_POI', 'India_Public'],
    x: [781, 15000, 701, 4407, 451, 522],
    name: 'Against',
    orientation: 'h',
    type: 'bar',
    marker: {
        color: 'rgba(58, 71, 80, 0.6)',
        line: {
            color: 'rgba(258, 71, 80, 1.0)',
            width: 3
        }
    }
}
var stackedbardata = [stackedbartrace1, stackedbartrace2]
var stackedbarlayout = {
    barmode: 'stack',
    paper_bgcolor: 'rgba(0, 0, 0, 0)',
    plot_bgcolor: 'rgba(0, 0, 0, 0)',
    font: {
        family: 'Trebuchet MS, sans-serif',
        color: 'white',
    },
    title: 'Distribution of Detected Stances Towards Vaccines'
}

const words_per_topic_titles = {
    0: 'Covid',
    1: 'Covid cases and omicron',
    2: 'India fight corona',
    3: 'Hospital and medications',
    4: 'Tests and travel',
    5: 'Social distancing and masks',
    6: 'Covid and economy'
}

var k = '1'
for (var i = 0; i < words_per_topic.length; i++) {
    var words_per_topic_layout = {
        title: words_per_topic_titles[i],
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        margin: {l: 60, r: 15, b: 15, t: 50},
        height: 300,
        width: 300,
        font: {
            color: "white"
        }
    }
    var words_per_topic_plot = document.createElement("div")
    words_per_topic_plot.id = k; words_per_topic_plot.classList.add('words_per_topic_plots');
    words_per_topic_container.appendChild(words_per_topic_plot)
    Plotly.newPlot(k, words_per_topic[i], words_per_topic_layout)
    k += 1
};

Plotly.newPlot('pie_container', piedata, pielayout);
Plotly.newPlot('stacked_bar', stackedbardata, stackedbarlayout)
Plotly.newPlot('sunburst_container', sunburstdata, sunburstlayout)
}


function plots(){
    ajaxGetRequest("/analytics.html/plots", plotsCallback)
};





