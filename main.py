from bokeh.plotting import show, output_file
from bokeh.layouts import layout, column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Button, CustomJS, TapTool, Div

from data_extraction import main_page_setup, filter_line_page_setup, inner_page_setup
from main_interaction import vertical_line_with_cursor, info_with_cursor, year_slider, brand_filter


def main():
    main_page = main_page_setup()
    filter_line_page = filter_line_page_setup()
    inner_page = inner_page_setup()

    # main page interaction
    vertical_line_with_cursor(main_page)  # show vertical lines with cursor
    info_with_cursor(main_page)  # show information when hover

    # filter page interaction
    # show vertical lines with cursor
    vertical_line_with_cursor(filter_line_page)
    info_with_cursor(filter_line_page)  # show information when hover

    # inner page interaction
    # info_with_cursor(inner_layer_page)  # show information when hover

    # buttons for page switching
    main_but = Button(label="Main Layer", button_type="success",
                      width=100, height=30)
    inner_but = Button(label="Inner Layer", button_type="success",
                       width=100, height=30)
    filter_but = Button(label="filter Layer", button_type="success",
                        width=100, height=30)

    ferarri_logo_html = """
<a href="https://google.com" target="_blank">
    <img src="image/ferrari_logo.jpg" width="90" height="50">
</a>
"""

    audi_logo_html = """
<a href="https://google.com" target="_blank">
    <img src="image/audi_logo.jpg" width="90" height="65">
</a>
"""

    ferarri_logo = Div(text=ferarri_logo_html)
    audi_logo = Div(text=audi_logo_html)
    # page setup
    # 1. main page setup
    main_page = column(main_page,
                       row(year_slider(main_page), filter_but, inner_but, ferarri_logo, audi_logo), Spacer(height=20))

    # 2. filter layer setup
    filter_line_page = column(filter_line_page,
                              row(year_slider(filter_line_page), brand_filter(filter_line_page),  main_but, inner_but), Spacer(height=20))

    # 3. inner layer setup
    inner_page = column(inner_page,
                        row(main_but, filter_but))

    # main but_callback
    main_but_callback = CustomJS(args=dict(main_page=main_page, inner_page=inner_page, filter_page=filter_line_page, inner=inner_but, main=main_but, filter=filter_but), code="""
        main_page.visible = true;
        main.visible = false;
        inner_page.visible = false;
        inner.visible = true;
        filter_page.visible = false;
        filter.visible = true;
    """)
    # inner but_callback
    inner_but_callback = CustomJS(args=dict(main_page=main_page, inner_page=inner_page, filter_page=filter_line_page, inner=inner_but, main=main_but, filter=filter_but), code="""
        main_page.visible = false;
        main.visible = true;
        inner_page.visible = true;      
        inner.visible = false;
        filter_page.visible = false;
        filter.visible = true;
    """)
    # filter but_callback
    filter_but_callback = CustomJS(args=dict(main_page=main_page, inner_page=inner_page, filter_page=filter_line_page, inner=filter_but, main=main_but, filter=filter_but), code="""
        main_page.visible = false;
        main.visible = true;
        inner_page.visible = false;      
        inner.visible = true;
        filter_page.visible = true;
        filter.visible = false;
    """)

    main_but.js_on_click(main_but_callback)
    inner_but.js_on_click(inner_but_callback)
    filter_but.js_on_click(filter_but_callback)

    main_page.visible = True
    filter_line_page.visible = False
    inner_page.visible = False
    # show the plot
    final_layout = layout([[main_page, inner_page, filter_line_page]],
                          sizing_mode='stretch_both')
    curdoc().add_root(final_layout)

    output_file("automotive_market_dynamics.html")
    show(final_layout)


if __name__ == "__main__":
    main()
