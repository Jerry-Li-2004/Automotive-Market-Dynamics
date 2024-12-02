from bokeh.plotting import show, output_file
from bokeh.layouts import layout, column, row, Spacer
from bokeh.io import curdoc

from data_extraction import main_page_setup
from main_interaction import vertical_line_with_cursor, info_with_cursor, year_slider


def main():
    main_page = main_page_setup()

    # interaction
    vertical_line_with_cursor(main_page)  # show vertical lines with cursor
    info_with_cursor(main_page)  # show information when hover
    main_page = year_slider(main_page)

    # show the plot
    final_layout = layout([[main_page]], sizing_mode='stretch_both')
    curdoc().add_root(final_layout)

    output_file("automotive_market_dynamics.html")
    show(final_layout)


main()
