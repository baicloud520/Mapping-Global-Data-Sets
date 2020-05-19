import os
import csv
import json
import matplotlib.pyplot as plt
from datetime import datetime

# Import Scattergeo chart type and Layout class.
from plotly.graph_objs import Scattergeo, Layout
# Import offline module to render map.
from plotly import offline


#------------- OPEN SOURCE FILE AND EXPORT DATA TO A NEW JSON FILE ------------#

filename = os.path.join("data", "covid19_data.csv")
with open(filename) as f:
    # Call csv.reader() object:
    reader = csv.reader(f)
    # Return the next line in the file (header):
    header_row = next(reader)
    # Print header and its corresponding index:
    for index, header in enumerate(header_row):
        print(f"{index}, {header}")

        # Read and store searched indexes:
        date_index = header_row.index("Date")
        country_index = header_row.index("Country/Region")
        state_index = header_row.index("Province/State")
        long_index = header_row.index("Long")
        lat_index = header_row.index("Lat")
        confirmed_index = header_row.index("Confirmed")
        recovered_index = header_row.index("Recovered")
        deaths_index = header_row.index("Deaths")

    # Check data length and initialize nested list.
    countries, dates, lists, sizes = [], [], [], []

    info_source = "Center for Systems Science and Engineering (CSSE) at Johns Hopkins University"
    info_url = "https://datahub.io/core/covid-19"
    info_updated = "12-05-2020"
    info_covid19 = "Coronavirus disease (COVID-19) is caused by the Severe acute respiratory syndrome Coronavirus 2 (SARS-CoV-2)"
    info_title = "Worldwide COVID19 confirmed cases, deaths, and recovered cases around the world since 2020-01-22"
    info_zones = "Number of analyzed geographical zones: 266"
    info = {
        "metadata": {
            "source": info_source,
            "url": info_url, "updated": info_updated,
            "title": info_title, "covid19": info_covid19,
            "territories": info_zones
        },
        "database": lists,
    }

    for index, row in enumerate(reader):

        identifier = f"{row[country_index]}:{row[state_index]}"
        print(row[country_index])
        print(identifier)
        # Check number of countries (no repetition):
        if identifier not in countries:
            countries.append(identifier)

        # Get current date:
        date = datetime.strptime(row[date_index], "%Y-%m-%d")
        country = row[country_index]
        state = row[state_index]
        # Small trick to add.
        if state == "":
            state = "none"

        try:
            lon = float(row[long_index])
            lat = float(row[lat_index])
            confirmed = int(row[confirmed_index])
            recovered = int(row[recovered_index])
            deaths = int(row[deaths_index])

            size = 0
            plot_color = ""
            if confirmed < 200:
                size = 6
                plot_color = "red"
            elif confirmed < 800:
                size = 8
                plot_color = "red"
            elif confirmed < 1_600:
                size = 12
                plot_color = "red"
            elif confirmed < 3_200:
                size = 16
                plot_color = "red"
            elif confirmed < 24_000:
                size = 20
                plot_color = "red"
            elif confirmed < 72_000:
                size = 24
                plot_color = "red"
            elif confirmed < 150_000:
                size = 28
                plot_color = "red"
            elif confirmed < 500_000:
                size = 32
                plot_color = "red"
            else:
                size = 36
                plot_color = "red"
 except ValueError:
            print(f"Missing float for {date}")
        else:
            # key = f"{identifier}." + str(row[date_index])
            inf = {
                "territory": {"country": country, "state/province": state},
                "coordinates": {"lon": lon, "lat": lat},
                "spreading": {"date": row[date_index], "confirmed": confirmed,
                              "recovered": recovered, "deaths": deaths},
                "plot_params": {"size": size, "color": plot_color}
            }

        lists.append(inf)
        # print(info[row[country_index]])

    # Save to readable file.
    filename = os.path.join("data", "clean_covid19_data.json")
    with open(filename, "w") as f:
        json.dump(info, f, indent=4)

# Check.
# print(row[country_index])
# print(info)


#----------------------------- EXTRACT INFORMATIOM ---------------------------#

# Recover data associated with key "features".
# It is a list of dictionaries.
# Store it in "all_eq_dicts".
data_info, all_dicts = info["metadata"], info["database"]
# Verify that we've captured all data.
print(len(data_info))
print(len(all_dicts))

# Extract title name.
title = data_info["title"]

# Select date for plot.
time_to_analyze = "2020-05-12"

# Extract confirmed from each territory.
# Empty list to store magnitudes, longitudes, lattitudes, and titles.
dates, confs, longs, lats, hover_texts, sizs, colors = [], [], [], [], [], [], []
# Recover last update.
for dictionary in all_dicts:
    if dictionary["spreading"]["date"] == time_to_analyze:
        label = (f"<br>Country: {dictionary['territory']['country']}<br>"
                 f"State: {dictionary['territory']['state/province']}<br>"
                 f"Confirmed: {dictionary['spreading']['confirmed']}<br>"
                 f"Recovered: {dictionary['spreading']['recovered']}<br>"
                 f"Deaths: {dictionary['spreading']['deaths']}")
        hover_texts.append(label)
        confs.append(dictionary["spreading"]["confirmed"])
        longs.append(dictionary["coordinates"]["lon"])
        lats.append(dictionary["coordinates"]["lat"])
        sizs.append(dictionary["plot_params"]["size"])
        colors.append(dictionary["plot_params"]["color"])


# # Check.
# print(hover_texts[0:266])
# print(confs[0:266])
# print(longs[0:266])
# print(lats[0:266])


#----------------------------- BUILDING A WORLDMAP ---------------------------#

# Define a list to store Scattergeo object.
# Remember, you can plot more than one data set
# on any visualization.

# Store information about data structure in key-value pairs.
# To show severity, adapt size of markers (inside list comprehension.
# Customize each markers color to provide classification to the severity
# of each earthquake.
data = [{
    "type": "scattergeo",
    "visible": True,
    "lon": longs,
    "lat": lats,
    "hovertext": hover_texts,
    "marker": {
        "symbol": "circle-dot",
        "size": sizs,
        "color": colors,
        "opacity": 0.7,
    },
}]

print(hover_texts)
msg = f"Covid-19 World Map ({time_to_analyze})"
my_layout = Layout(title={"text": msg, "xref": "container", "yref": "container",
                          "x": 0.5, "y": 0.92, "xanchor": "center", "yanchor": "middle",
                          "font": {"family": "Arial", "size": 35}},
                   showlegend=False, paper_bgcolor="white", plot_bgcolor="red",
                   geo={"showland": True, "landcolor": "#F0DC82", "showocean": True,
                        "oceancolor": "#80DEEA", "showlakes": True, "lakecolor": "#80DEEA",
                        "showrivers": True, "rivercolor": "#80DEEA", "showcountries": True,
                        "showsubunits": True},
                   hovermode="closest",
                   )

# Create a dictionary that contains data and layout.
fig = {"data": data, "layout": my_layout}
# Pass "fig" to plot with a descriptive filename.
offline.plot(fig, filename="global_covid19.html")
