from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter
from bokeh.layouts import layout
from bokeh.io import curdoc
from bokeh.palettes import Category10, Category20

import numpy as np
import pandas as pd

sales_df = pd.read_csv("dataset/Sales_table.csv")

volvo_sales = sales_df.loc[sales_df['Maker'] ==
                           'VOLVO', ["2016", "2017", "2018", "2019", "2020"]]

toyota_sales = sales_df.loc[sales_df['Maker'] ==
                            'TOYOTA', ["2016", "2017", "2018", "2019", "2020"]]

nissan_sales = sales_df.loc[sales_df['Maker'] ==
                            'NISSAN', ["2016", "2017", "2018", "2019", "2020"]]

volkswagen_sales = sales_df.loc[sales_df['Maker'] ==
                                'VOLKSWAGEN', ["2016", "2017", "2018", "2019", "2020"]]

total_volvo_sales = volvo_sales.sum(axis=0).values
total_toyota_sales = toyota_sales.sum(axis=0).values
total_nissan_sales = nissan_sales.sum(axis=0).values
total_volkswagen_sales = nissan_sales.sum(axis=0).values

years = np.arange(2016, 2021)

data = pd.DataFrame({'Year': years, 'VOLVO': total_volvo_sales,
                    'TOYOTA': total_toyota_sales, 'NISSAN': total_nissan_sales, 'VOLKSWAGEN': total_volkswagen_sales})
print(data.head())

source = ColumnDataSource(data)

p = figure(title="Automotive Market Dynamics Visualization", x_axis_label='Year',
           y_axis_label='Sales', sizing_mode='stretch_both', width=800, height=400)

colors = Category20[4]
colors_label = ['Volvo', 'Toyota', 'Nissan', 'Volkswagen']
p.varea_stack(stackers=['VOLVO', 'TOYOTA', 'NISSAN', 'VOLKSWAGEN'],
              x='Year', color=colors, source=source, legend_label=colors_label)

hover = HoverTool()
hover.tooltips = [("Year", "@Year"), ("Volvo",
                                      "@{VOLVO}{0,0}"), ('Toyota', "@{TOYOTA}{0,0}"), ("Nissan", "@{VOLVO}{0,0}"), ("Volkswagen", "@{VOLKSWAGEN}{0,0}")]
p.add_tools(hover)

p.yaxis.formatter = NumeralTickFormatter(format="0,0")
p.title.text_font_size = '20pt'
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

l = layout([[p]], sizing_mode='stretch_both')
curdoc().add_root(l)

output_file("automotive_market_dynamics.html")
show(l)
