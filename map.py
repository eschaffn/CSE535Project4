import json
import plotly.graph_objects as go


topic_colors = {
    -1: "rgb(0, 0, 0)",
    0: "rgb(255, 255, 0)",
    1: "rgb(21, 247, 21)",
    2: "rgb(21, 247, 240)",
    3: "rgb(247, 21, 51)",
    4: "rgb(247, 21, 225)",
    5: "rgb(247, 179, 21)",
    6: "rgb(247, 21, 134)",
    7: "rgb(149, 247, 21)",
    8: "rgb(247, 142, 21)",
    9: "rgb(21, 247, 81)",
    10: "rgb(255, 255, 255)"
}
topic_names = {
    -1: "Not COVID related",
    0: "Vaccines",
    1: "Conspiracy",
    2: "Government/Politics",
    3: "Social Distancing",
    4: "Lockdown",
    5: "School",
    6: "Travel",
    7: "COVID Curve",
    8: "News",
    9: "Long-Term Health Effects",
    10: "Symptoms"
}
line_len = 120


def format_text(user, body, topic):
    out = "@" + user + ": <br><br>\'\'\'"
    start = 0
    end = line_len
    stop = False

    while not stop:
        while end < len(body) and not text[end].isspace():
            end += 1

        stop = end >= len(body)
        out += body[start:end].strip()

        if stop:
            out += "\'\'\'"
        else:
            start = end
            end += line_len

        out += "<br>"

    return out + "<br>TOPIC: " + topic


if __name__ == '__main__':
    with open('results.json') as f:
        data = json.load(f)

    lon = []
    lat = []
    text = []
    color = []

    for d in data:
        if not d['geolocation'] == "":
            lon.append(d['geolocation'][0])
            lat.append(d['geolocation'][1])
            text.append(format_text(d['username'], d['tweet_text'], topic_names[d['topic']]))
            color.append(topic_colors[d['topic']])

    sg = go.Scattergeo(lon=lon, lat=lat, text=text, mode='markers', marker_color=color, hoverinfo='text')
    fig = go.Figure(data=sg)
    fig.update_layout(title="Search Results:", geo_scope='world')
    fig.update_geos(showcountries=True, countrycolor='black')
    fig.show()
