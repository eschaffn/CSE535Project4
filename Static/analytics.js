function plotsCallback(response){
var R = JSON.parse(response);



var pie = R.piechart_data
var sunburst = R.sunburst_data
var words_per_topic_container = document.getElementById('words_per_topic_container')
var words_per_topic = R.words_per_topic_data
var bubblechart = R.bubblechart_data

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
    x: [203, 807, 92, 581, 232, 770],
    name: 'Pro',
    orientation: 'h',
    type: 'bar',
    marker: {
        color: 'rgba(72, 133, 237, 0.6)',
        line: {
            color: 'rgba(55, 53, 54, 1)',
            width: 3
        }
    }
}
var stackedbartrace3 = {
    y: ['US_POI', 'US_Public', 'Mex_POI', 'Mex_Public', 'India_POI', 'India_Public'],
    x: [41, 1070, 12, 691, 13, 295],
    name: 'Against',
    orientation: 'h',
    type: 'bar',
    marker: {
        color: 'rgba(219, 50, 54, 0.6)',
        line: {
            color: 'rgba(55, 53, 54, 1)',
            width: 3
        }
    }
}

var stackedbartrace2 = {
    y: ['US_POI', 'US_Public', 'Mex_POI', 'Mex_Public', 'India_POI', 'India_Public'],
    x: [134, 1001, 54, 627, 121, 616],
    name: 'Neutral',
    orientation: 'h',
    type: 'bar',
    marker: {
        color: 'rgba(60, 186, 84, 0.6)',
        line: {
            color: 'rgba(55, 53, 54, 1)',
            width: 3
        }
    }
}
var stackedbardata = [stackedbartrace1, stackedbartrace2, stackedbartrace3]
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
    0:'Corona_Masks_Government',
    1:'Immunity_Positive_South_Africa',
    2:'Hospital_Health',
    3:'Coronavirus',
    4:'India_Covid_Cases',
    5:'Omicron_Variant',
    6:'Symptoms_Lockdown',
    7:'Travel_Quarantine',
    8:'Social_Distance',
    9:'Covid_Vaccination',
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

var bubblechartlayout = {
    title: 'Stance Towards Vaccines Graphed Against Covid Cases per Day',
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(128, 128, 128, 0.3)',
    font: {
        color: 'white'
    }
}
Plotly.newPlot('pie_container', piedata, pielayout);
Plotly.newPlot('stacked_bar', stackedbardata, stackedbarlayout)
Plotly.newPlot('sunburst_container', sunburstdata, sunburstlayout)
Plotly.newPlot('bubblechart_container', bubblechart, bubblechartlayout)
}


function plots(){
    ajaxGetRequest("/analytics.html/plots", plotsCallback)
};





