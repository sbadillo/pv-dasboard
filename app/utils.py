import time
import requests

import pandas as pd
import plotly.graph_objects as go

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


def return_figures(data):
    """Creates plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the plotly visualizations
    """

    # hourly is a list of dicts : {'time': '20150101:0010', 'P': 0.0,
    # 'Gb(i)': 0.0, 'Gd(i)': 0.0, 'Gr(i)': 0.0, 'H_sun': 0.0, 'T2m': -1.15,
    # 'WS10m': 1.96, 'Int': 0.0}, ...

    # build a main dataframe
    df = pd.DataFrame.from_dict(data=data["outputs"]["hourly"])
    index = pd.to_datetime(df["time"], format="%Y%m%d:%H%M")
    df.index = index

    df["G(i)"] = df["Gb(i)"] + df["Gd(i)"] + df["Gr(i)"]

    # build secondary df, temporal selections and resampling
    summer = df["2015-06-30"]  # graph 1 typical day
    winter = df["2015-12-24"]  # graph 2 typical day
    monthly = df.resample("M").sum()  # for calendar monthly

    # todo : averaged day of summer
    # todo : averaged day of winter

    # Convert Dataframe Indexes to Hour:Minute format to make plotting easier
    summer.index = summer.index.strftime("%H")
    winter.index = winter.index.strftime("%H")
    monthly.index = monthly.index.strftime("%b")

    # construct first chart
    chart_summer = []
    chart_summer.append(
        go.Scatter(x=list(summer.index), y=list(summer["G(i)"].values), mode="lines")
    )

    layout_summer = dict(
        title="Summer day",
        xaxis=dict(title="Hour of day"),
        yaxis=dict(title="Global irradiance [W/m2]"),
    )

    # construct second chart
    chart_winter = []

    chart_winter.append(
        go.Scatter(x=list(winter.index), y=list(winter["G(i)"].values), mode="lines")
    )

    layout_winter = dict(
        title="Winter day",
        xaxis=dict(title="Hour of day"),
        yaxis=dict(title="Global irradiance [W/m2]"),
    )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=chart_summer, layout=layout_summer))
    figures.append(dict(data=chart_winter, layout=layout_winter))

    return figures