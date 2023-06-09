# -*- coding: utf-8 -*-
"""FinalVisdat_1301190354_1301180205

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vKJWabjaPLboiBStyINAeWvor3co85JY

### **TUGAS BESAR AKHIR VISUALISASI DATA DENGAN VISUALISASI INTERAKTIF**
Dataset yang digunakan merupakan Data dari IMDb Movie yang berisi nama-nama film dan genre yang tersedia dengan score yang diberikan juga voting dari user, dari dataset ini kami menampilkan grafik dengan nama-nama genre yang ada dan terbanyak filmnya dan juga menampilkan grafik nilai score dan juga voter tertinggi.

**Nama Kelompok :**


Muhammad Haidir Ali (1301180205)
Fanji Aburizal (1301190354)
"""

# Data handling
import pandas as pd
import numpy as np
import jinja2

# Bokeh libraries
from markupsafe import Markup
from bokeh.io import curdoc, show, output_file, output_notebook
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, WheelZoomTool
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral5
from bokeh.layouts import column, row, gridplot
from bokeh.models import Slider, Select
from bokeh.models import Panel, Tabs

df = pd.read_csv ('movies.csv')

"""dataset: https://www.kaggle.com/datasets/danielgrijalvas/movies"""

df = df.dropna()
df.year = df.year.astype(int)
df = df.sort_values('year', ascending=True)
print(df.info())

is_null = df.isnull().sum()
print(is_null)

df.head(2)

df.tail(2)

data = df.set_index("year")
x = data.loc[1980].votes
y = data.loc[1980].score

# Count the number of movies per genre
genre_counts = data.groupby('genre').size().reset_index(name='count')

# Create a new figure for the genre count plot
genre_plot = figure(x_range=genre_counts['genre'], plot_height=400, title='Number of Movies per Genre')
genre_plot.vbar(x='genre', top='count', width=0.9, source=ColumnDataSource(genre_counts))

# Add labels and formatting to the genre plot
genre_plot.xaxis.axis_label = 'Genre'
genre_plot.yaxis.axis_label = 'Count'
genre_plot.xaxis.major_label_orientation = 45

# # Add the layouts to the current document
# curdoc().add_root(genre_layout)

# # Show the plots separately
# show(genre_layout)

show(genre_plot)

# initial source
vs_cds = ColumnDataSource(data={
    "x": data.loc[1980].votes,
    "y": data.loc[1980].score,
    "Title": data.loc[1980].name,
    "Genre" : data.loc[1980].genre,
    "Company" : data.loc[1980].company,
    "Country" : data.loc[1980].country,
})
# color map
genre_list = data.genre.unique().tolist()
color_mapper = CategoricalColorMapper(factors=genre_list, palette=Spectral5)

# hover tool
hover = HoverTool(tooltips = [("Title","@Title"), 
                              ("Genre","@Genre"),
                              ("Company","@Company"),
                              ("Country","@Country")])

# plotting
plot=figure(title ="Rates Movie in IMDB",
            x_axis_label="number of user votes", y_axis_label="IMDb user rating",
            tools=[hover, WheelZoomTool(), "crosshair","pan","box_zoom", "reset"],
            width=650, height=450)
plot.circle("x","y", source=vs_cds, fill_alpha=2,size=12,
            color=dict(field="Genre", transform=color_mapper), 
            legend_field="Genre", hover_color ="red")

# In this method x and y axis are updated from drop dawn value and year is updated from slider value.
def update(attr, old, new):
     # set the `yr` name to `slider.value` and `source.data = new_data`
    yr = slider.value
    x = x_select.value
    y = y_select.value
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    new_data = {
        "x"       : data.loc[yr][x],
        "y"       : data.loc[yr][y],
        "Title" : data.loc[yr].name,
        "Genre" : data.loc[yr].genre,
        "Company" : data.loc[yr].company,
        "Country" : data.loc[yr].country,
    }
    source.data = new_data

    # Add title to figure: plot.title.text
    plot.title.text = 'Rates Movie in IMDB - Year {}'.format(yr)

# Make a slider object: slider
slider = Slider(start=1980, end=2020, step=1, value=1980, title='Year')
slider.on_change('value', update)

# # Make dropdown menu for x and y axis
# Create a dropdown Select widget for the x data: x_select
x_select = Select(
    options=["votes", "score", "budget", "gross"],
    value="votes",
    title='x-axis data'
)
# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', update)

# Create a dropdown Select widget for the y data: y_select
y_select = Select(
    options=['votes', 'score', 'budget', 'gross'],
    value='score',
    title='y-axis data'
)

# Attach the update_plot callback to the 'value' property of y_select
y_select.on_change('value', update)

# Create layout and add to current document
layout = row(column(slider, x_select, y_select), plot, sizing_mode='scale_width')
curdoc().add_root(layout)

show(layout)

tab1 = Panel(child=genre_plot, title="Genre")
tab2 = Panel(child=layout, title="Rate")
show(Tabs(tabs=[tab1, tab2]))