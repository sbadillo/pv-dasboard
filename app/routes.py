from app import app
import json

# import plotly
from flask import render_template, request, redirect

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
        # latitude = request.form.get("latitude")
        # longitude = request.form.get("longitude")

        json_rad = get_hourly_rad(
            lat=req["latitude"],
            lon=req["longitude"],
            peakpower=req["nameplate"],
            angle=req["slope"],
            azimuth=req["azimuth"],
        )

        return """
              <p>{}</p>
              """.format(
            json_rad
        )

    # figures = return_figures()

    # plot ids for the html id tag
    # # ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # # Convert the plotly figures to JSON for javascript in html template
    # figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        "index.html",
        #    ids=ids,
        #    figuresJSON=figuresJSON
    )


# TODO : put this function in a file of its own, but where ?

# import pandas as pd
import time
import requests

from requests.exceptions import HTTPError


def get_hourly_rad(
    lat,
    lon,
    peakpower,
    angle,
    azimuth,
    startyear=2015,
    endyear=2016,
):
    """Build query and executes requests to pvgis' photovololtaic
    series hourly radiation endpoint.

    Args:
        lat ([float]): [description]
        lon ([float]): [description]
        peakpower ([float]): [description]
        angle ([float]): [description]
        azimuth ([float]): [description]
        startyear (int, optional): [description]. Defaults to 2015.
        endyear (int, optional): [description]. Defaults to 2016.

    Returns:
        [type]: [description]
    """

    url = "https://re.jrc.ec.europa.eu/api/seriescalc?"

    params = {
        "lat": lat,
        "lon": lon,
        "startyear": startyear,
        "endyear": endyear,
        "pvcalculation": 1,
        "peakpower": peakpower,
        "loss": 14,
        "angle": angle,
        "aspect": azimuth,
        "components": 1,  # If "1" outputs E_beam, E_diffuse and E_ground components.
        "outputformat": "json",  # csv, json, epw
    }

    start = time.time()
    try:
        r = requests.get(url, params=params)

        # If the respons was successful, no Exception will be raised
        r.raise_for_status()

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(r.message)

    except Exception as err:
        print(f"Other error occurred: {err}")

    else:
        print("get_hourly_rad: done in {:.2f} seconds.".format(time.time() - start))

        result = r.json()

        # df_r = pd.DataFrame.from_dict(data=tmy_json["outputs"]["tmy_hourly"])
        # df_tmy = df_r[["time(UTC)", "G(h)", "Gb(n)", "Gd(h)"]].copy()
        # df_tmy.set_index(self.times, inlace=True)
        # df_tmy.columns = ["time_pvgis", "GHI", "DNI", "DHI"]

        # return df_tmy

        return result