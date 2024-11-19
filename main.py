from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter, Span, CustomJS
from bokeh.layouts import layout
from bokeh.io import curdoc
from bokeh.palettes import Category10, Category20

import numpy as np
import pandas as pd

from data_extraction import get_sales_data, main_page_setup

#extract the data
total_volvo_sales, total_toyota_sales, total_nissan_sales, total_volkswagen_sales = get_sales_data()

main_page = main_page_setup()

#show vertical lines with cursor:
vline = Span(location=0, dimension = 'height',line_color='black', line_width =2 , line_dash = [10,5])
main_page.add_layout(vline)
main_page.js_on_event('mousemove', CustomJS(args=dict(vline=vline), code="""
    const x = cb_obj.x;
    vline.location = x;
"""))

#show information when hover
hover = HoverTool()
hover.tooltips = [("Year", "@Year"), ("Volvo",
                                      "@{VOLVO}{0,0}"), ('Toyota', "@{TOYOTA}{0,0}"), ("Nissan", "@{VOLVO}{0,0}"), ("Volkswagen", "@{VOLKSWAGEN}{0,0}")]
main_page.add_tools(hover)

final_layout = layout([[main_page]], sizing_mode='stretch_both')
curdoc().add_root(final_layout)

output_file("automotive_market_dynamics.html")
show(final_layout)
