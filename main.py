from bokeh.plotting import show, output_file
from bokeh.layouts import layout
from bokeh.io import curdoc

from data_extraction import get_sales_data, main_page_setup
from main_interaction import vertical_line_with_cursor, info_with_cursor

#extract the data
total_volvo_sales, total_toyota_sales, total_nissan_sales, total_volkswagen_sales = get_sales_data()

main_page = main_page_setup()

#interaction
vertical_line_with_cursor(main_page)        #show vertical lines with cursor
info_with_cursor(main_page)                 #show information when hover

#show the plot
final_layout = layout([[main_page]], sizing_mode='stretch_both')
curdoc().add_root(final_layout)

output_file("automotive_market_dynamics.html")
show(final_layout)
