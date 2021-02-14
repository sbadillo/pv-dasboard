from app import app
from .utils import get_hourly_rad, return_figures
import json

import plotly
from flask import render_template, request

# from wrangling_scripts.wrangle_data import return_figures

# We're going to be accepting POST requests on this route
#   so we need to pass another argument to @app.route


@app.route("/", methods=["GET", "POST"])
@app.route("/index")
def index():

    # handle the POST request
    if request.method == "POST":
        print(request.form)
        req = request.form

        json_rad = get_hourly_rad(
            lat=req["latitude"],
            lon=req["longitude"],
            peakpower=req["nameplate"],
            angle=req["slope"],
            azimuth=req["azimuth"],
        )

        figures = return_figures(json_rad)

        ids = ["figure-{}".format(i) for i, _ in enumerate(figures)]

        # Convert the plotly figures to JSON for javascript in html template
        figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

        # return """
        #       <p>{}</p>
        #       """.format(
        #     json_rad
        # )

        return render_template("graphs.html", ids=ids, figuresJSON=figuresJSON)

    # figures = return_figures()

    # plot ids for the html id tag
    # # ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    return render_template(
        "index.html",
        #    ids=ids,
        #    figuresJSON=figuresJSON
    )
