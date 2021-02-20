from app import app
from .utils import get_hourly_rad, return_figures
import json

import plotly

from flask import render_template, request, jsonify
import pandas as pd


# We're going to be accepting POST requests on this route
#   so we need to pass another argument to @app.route


@app.route("/", methods=["GET", "POST"])
@app.route("/index")
def index():

    # handle the POST request
    if request.method == "POST":
        print("flask : got you")
        req = request.form

        data = {}
        data["success"] = False

        # validations
        data["errors"] = {}

        if not req["latitude"].isnumeric():
            data["errors"]["latitude"] = "latitude must be numeric"

        if not req["longitude"].isnumeric():
            data["errors"]["longitude"] = "longitude must be numeric"

        if not req["peakpower"].isnumeric():
            data["errors"]["peakpower"] = "peak power must be numeric"

        if not req["angle"].isnumeric():
            data["errors"]["angle"] = "angle must be numeric"

        if not req["azimuth"].isnumeric():
            data["errors"]["azimuth"] = "azimuth must be numeric"

        if len(data["errors"]) != 0:
            return data

        # if all input is fine, run get_hourly_rad
        json_rad = get_hourly_rad(
            lat=req["latitude"],
            lon=req["longitude"],
            peakpower=req["peakpower"],
            angle=req["angle"],
            azimuth=req["azimuth"],
        )

        figures = return_figures(json_rad)

        # plot ids for the html id tag
        ids = ["figure-{}".format(i) for i, _ in enumerate(figures)]

        # Convert the plotly figures to JSON for javascript in html template
        figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

        data["success"] = True
        data["ids"] = ids
        data["figuresJSON"] = figuresJSON

        # return render_template("graphs.html", ids=ids, figuresJSON=figuresJSON)

        return data

    return render_template(
        "index.html",
        #    ids=ids,
        #    figuresJSON=figuresJSON
    )
