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
        print(r.text)
        return r.text

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


import pandas as pd
import plotly.graph_objs as go


def return_figures(data):
    """Creates plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations
    """

    print("data outputs len : ", len(data["outputs"]))

    # first chart plots arable land from 1990 to 2015 in top 10 economies
    # as a line chart

    graph_one = []
    graph_one.append(
        go.Scatter(x=[0, 1, 2, 3, 4, 5], y=[0, 2, 4, 6, 8, 10], mode="lines")
    )

    layout_one = dict(
        title="Chart One",
        xaxis=dict(title="x-axis label"),
        yaxis=dict(title="y-axis label"),
    )

    # second chart plots ararble land for 2015 as a bar chart
    graph_two = []

    graph_two.append(
        go.Bar(
            x=["a", "b", "c", "d", "e"],
            y=[12, 9, 7, 5, 1],
        )
    )

    layout_two = dict(
        title="Chart Two",
        xaxis=dict(
            title="x-axis label",
        ),
        yaxis=dict(title="y-axis label"),
    )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))

    return figures