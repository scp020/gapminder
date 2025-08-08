'''
鼠标悬浮可以查看每个国家的具体数据
多个点重叠的情况可以同时显示多个国家的信息
'''

import os
import pandas as pd
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import (
    Button,
    CategoricalColorMapper,
    ColumnDataSource,
    HoverTool,
    Label,
    SingleIntervalTicker,
    Slider,
    Legend,
)
from bokeh.palettes import Spectral6
from bokeh.plotting import figure

current_dir = os.path.dirname(os.path.abspath(__file__))

pop_path = os.path.join(current_dir, 'pop_data.csv')
reg_path = os.path.join(current_dir, 'reg.csv')
income_path = os.path.join(current_dir, 'income_data.csv')
life_path = os.path.join(current_dir, 'life_data.csv')


def process_data():
    years = [int(year) for year in range(1800, 2019)]
    population = pd.read_csv(pop_path, index_col=0)
    regions = pd.read_csv(reg_path, index_col=0)
    income_df = pd.read_csv(income_path, index_col=0)
    life_df = pd.read_csv(life_path, index_col=0)

    columns = list(life_df.columns)
    rename_dict = dict(zip(columns, years))

    income_df = income_df.rename(columns=rename_dict)
    life_df = life_df.rename(columns=rename_dict)
    population = population.rename(columns=rename_dict)
    regions = regions.rename(columns=rename_dict)

    regions_list = list(regions.Group.unique())

    # Turn population into bubble sizes. Use min_size and factor to tweak.

    scale_factor = 200
    population_size = np.sqrt(population / np.pi) / scale_factor
    min_size = 3
    population_size = population_size.where(population_size >= min_size).fillna(min_size)

    return income_df, life_df, population_size, regions, years, regions_list


income_df, life_df, population_df_size, regions_df, years, regions_list = process_data()

df = pd.concat({'income': income_df, 'life': life_df, 'population': population_df_size}, axis=1)

data = {}

regions_df.rename({'Group': 'region'}, axis='columns', inplace=True)
regions_df['region'] = regions_df['region'].str.strip().str.title().fillna('Unknown')

for year in years:
    df_year = df.iloc[:, df.columns.get_level_values(1) == year]
    df_year.to_csv('df_year.csv')
    df_year.columns = df_year.columns.droplevel(1)

    merged = df_year.reset_index().merge(regions_df.reset_index()[['Country', 'region']], on='Country', how='left')
    merged['region'] = merged['region'].fillna('Unknown')
    data[year] = merged.to_dict('list')

source = ColumnDataSource(data=data[years[0]])

regions_list = sorted(merged['region'].unique())

plot = figure(x_axis_type="log", x_range=(200, 128000), y_range=(20, 100), title='Gapminder Data', height=300)
plot.xaxis.ticker = SingleIntervalTicker(interval=1000)
plot.xaxis.axis_label = "income per person (d)"
plot.yaxis.ticker = SingleIntervalTicker(interval=20)
plot.yaxis.axis_label = "Life expectancy at birth (years)"

label = Label(x=500, y=40, text=str(years[0]), text_font_size='200px', text_color='#eeeeee')
plot.xaxis.ticker = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072]
plot.xaxis.major_label_overrides = {
    1: '1',
    2: '2',
    4: '4',
    8: '8',
    16: '16',
    32: '32',
    64: '64',
    128: '128',
    256: '256',
    512: '512',
    1024: '1k',
    2048: '2k',
    4096: '4k',
    8192: '8k',
    16384: '16k',
    32768: '32k',
    65536: '64k',
    131072: '128k',
}
plot.add_layout(label)

color_mapper = CategoricalColorMapper(palette=Spectral6, factors=regions_list)

color_mapper = CategoricalColorMapper(palette=Spectral6, factors=regions_list)
scatter = plot.scatter(
    x='income',
    y='life',
    size='population',
    source=source,
    fill_color={'field': 'region', 'transform': color_mapper},
    fill_alpha=0.8,
    line_color="#20201d",
    line_width=1.0,
    line_alpha=0.5,
    legend_group='region',
)

hover = HoverTool(
    tooltips=[("国家", "@Country"), ("收入", "@income{0,0}"), ("预期寿命", "@life{0}"), ("地区", "@region")],
    renderers=[scatter],
)
plot.add_tools(hover)

legend_items = []
for i, region in enumerate(regions_list):
    renderer = plot.scatter(
        x=[None],
        y=[None],  # 不可见的点
        fill_color=Spectral6[i % len(Spectral6)],
        size=0,
        alpha=0,  # 完全透明
        legend_label=region,
    )
    legend_items.append((region, [renderer]))

plot.legend[0] = Legend(items=legend_items)
# plot.add_tools(HoverTool(tooltips="@Country", show_arrow=False, point_policy='follow_mouse'))


def animate_update():
    year = slider.value + 1
    if year > years[-1]:
        year = years[0]
    slider.value = year


def slider_update(attrname, old, new):
    year = slider.value
    label.text = str(year)
    source.data = data[year]


slider = Slider(start=years[0], end=years[-1], value=years[0], step=1, title="Year")
slider.on_change('value', slider_update)

callback_id = None


def animate():
    global callback_id
    if button.label == '► Play':
        button.label = '❚❚ Pause'
        callback_id = curdoc().add_periodic_callback(animate_update, 200)
    else:
        button.label = '► Play'
        curdoc().remove_periodic_callback(callback_id)


button = Button(label='► Play', width=60)
button.on_event('button_click', animate)

layout = layout(
    [
        [plot],
        [slider, button],
    ],
    sizing_mode='scale_width',
)

curdoc().add_root(layout)
curdoc().title = "Gapminder"


# print("第一年数据:", data[years[0]])
