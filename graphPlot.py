import config as cfg
import numpy as np
import folium
from folium import plugins
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

data = cfg.data_set
folium_map = folium.Map([37.7783, -119.4179], zoom_start = 7)
# folium_map = folium.Map([37.805, -122.2711], zoom_start = 12)
colors = [
    'red',
    'blue',
    # 'gray',
    'darkred',
    'lightred',
    'orange',
    'beige',
    'green',
    'darkgreen',
    'lightgreen',
    'darkblue',
    'lightblue',
    'purple',
    'darkpurple',
    'pink',
    'cadetblue',
    'lightgray',
    'black'
]

def graph(battery_locations, energy_mapping):
    nf = getNormalizeFactor(cfg.month_index) # maximize size of possible ring radius
    for zipcode, values in data.items():
        if np.isnan(values[cfg.LATITUDE]) or np.isnan(values[cfg.LONGITUDE]): continue
        popup_text = """Zipcode: {}<br>
                        2017 Supply (KW): {}<br>
                        2017 Demand (KWh): {}"""
        popup_text = popup_text.format(str(zipcode), values[cfg.SUPPLY_KW], values[cfg.month_index])
        folium.CircleMarker([values[cfg.LATITUDE], values[cfg.LONGITUDE]], radius = 100 * (values[cfg.month_index] / nf), popup = popup_text).add_to(folium_map)

    for location in battery_locations.keys():
        folium.Marker([location[0], location[1]]).add_to(folium_map)

    for location, energy in energy_mapping.items():
        if energy == 0: continue
        folium.CircleMarker([location[0], location[1]], radius = 100 * (energy / nf), color = 'crimson').add_to(folium_map)

    folium_map.save("test_map.html")

def graph_scikit(battery_locations, zip_coords, battery_supplied_zipcodes, energy_supplied_zipcodes, zip_weights):
    nf = getNormalizeFactor(cfg.month_index) # maximize size of possible ring radius

    for index, val in enumerate(energy_supplied_zipcodes):
        if val == 0:
            folium.CircleMarker(zip_coords[index], radius = 100 * (zip_weights[index] / nf), color = 'gray').add_to(folium_map)

    for i, location in enumerate(battery_locations):
        folium.Marker(location, icon = folium.Icon(color = colors[i % len(colors)])).add_to(folium_map)
        for index in battery_supplied_zipcodes[i].keys():
            # if np.isnan(values[cfg.LATITUDE]) or np.isnan(values[cfg.LONGITUDE]): continue
            # popup_text = """Zipcode: {}<br>
            #                 2017 Supply (KW): {}<br>
            #                 2017 Demand (KWh): {}"""
            # popup_text = popup_text.format(str(zipcode), values[cfg.SUPPLY_KW], values[cfg.month_index])
            # folium.CircleMarker([values[cfg.LATITUDE], values[cfg.LONGITUDE]], radius = 100 * (values[cfg.month_index] / nf), popup = popup_text).add_to(folium_map)
            folium.CircleMarker(zip_coords[index], radius = 100 * (zip_weights[index] / nf), color = colors[i % len(colors)]).add_to(folium_map)

    folium_map.save("/Users/jkhunt/github/batteries-california/scikit_map.html")

def graph_comparison(battery_locations_start, battery_locations_end):
    nf = getNormalizeFactor(cfg.month_index) # maximize size of possible ring radius
    for zipcode, values in data.items():
        if np.isnan(values[cfg.LATITUDE]) or np.isnan(values[cfg.LONGITUDE]): continue
        popup_text = """Zipcode: {}<br>
                        2017 Supply (KW): {}<br>
                        2017 Demand (KWh): {}"""
        popup_text = popup_text.format(str(zipcode), values[cfg.SUPPLY_KW], values[cfg.month_index])
        folium.CircleMarker([values[cfg.LATITUDE], values[cfg.LONGITUDE]], radius = 100 * (values[cfg.month_index] / nf), popup = popup_text).add_to(folium_map)

    for location in battery_locations_start.values():
        folium.Marker([location[0][0], location[0][1]], icon = folium.Icon(color = 'blue')).add_to(folium_map)

    for location in battery_locations_end.values():
        folium.Marker([location[0][0], location[0][1]], icon = folium.Icon(color = 'red')).add_to(folium_map)

    folium_map.save("comparison_map.html")

def getNormalizeFactor(index):
    return max([x[index] for x in cfg.data_set.values()])

if __name__ == '__main__':
	graph()
