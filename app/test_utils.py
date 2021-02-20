# from app.utils import get_hourly_rad, return_figures
from utils import get_hourly_rad, return_figures

json_rad = get_hourly_rad(lat=44, lon=3, peakpower=3, angle=35, azimuth=0)

print(return_figures(json_rad))
