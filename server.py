import bottle
import json
import App


@bottle.route("/")
def serve_html():
    return bottle.static_file("homepage.html", root = '')
    
@bottle.route("/Static/Homepage.js")
def serve_front_end():
    return bottle.static_file("Static/Homepage.js", root = '')

@bottle.route("/Static/ajax.js")
def serve_AJAX():
    return bottle.static_file("Static/ajax.js", root = '')

@bottle.route("/Static/analytics.js")
def serve_analyticsJS():
    return bottle.static_file('Static/analytics.js', root = '')

@bottle.route("/analytics.html/Static/ajax.js")
def serve_analyticsAJAX():
    return bottle.static_file('Static/ajax.js', root = '')

@bottle.route("/Images/wordCloud2.png")
def serve_wordCloud2():
    return bottle.static_file('Images/wordCloud2.png', root = '')

@bottle.route("/analytics.html/plots")
def serve_piechart():
    results = App.run_plots()
    return json.dumps(results)

@bottle.route("/Images/logo.png")
def serve_logo():
    return bottle.static_file("Images/logo.png", root = '')

@bottle.route("/Images/chalkboard.jpg")
def background():
    return bottle.static_file("Images/chalkboard.jpg", root = '')

@bottle.route("/analytics.html")
def serve_analytics():
    return bottle.static_file('analytics.html', root = '')

@bottle.route("/about.html")
def serve_about():
    return bottle.static_file('about.html', root = '')

@bottle.route("/lda_10Topics.html")
def serve_lda():
    return bottle.static_file('lda_10Topics.html', root = '')

@bottle.post("/search")
def serve_query_data():
    content = bottle.request.body.read().decode()
    content = json.loads(content)
    results = App.fetchResults(content)

    return json.dumps(results)

@bottle.post("/translate")
def serve_translate_data():
    content = bottle.request.body.read().decode()
    content = json.loads(content)
    results = App.returnTranslation(content)

    return json.dumps(results)
