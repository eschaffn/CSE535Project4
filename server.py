import bottle
import json
import App


@bottle.route("/")
def serve_html():
    return bottle.static_file("homepage.html", root = '')
@bottle.route("/front_end.js")
def serve_front_end():
    return bottle.static_file("front_end.js", root = '')

@bottle.route("/ajax.js")
def serve_AJAX():
    return bottle.static_file("ajax.js", root = '')

@bottle.route("/Images/logo.png")
def serve_logo():
    return bottle.static_file("Images/logo.png", root = '')

@bottle.route("/Images/chalkboard.jpg")
def background():
    return bottle.static_file("Images/chalkboard.jpg", root = '')

@bottle.post("/search")
def serve_query_data():
    content = bottle.request.body.read().decode()
    content = json.loads(content)
    results = App.fetchResults(content)
    print(json.dumps(results))
    print(type(json.dumps(results)))
    return json.dumps(results)