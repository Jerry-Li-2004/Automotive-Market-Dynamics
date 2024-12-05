from bokeh.plotting import show, output_file
from bokeh.layouts import layout, column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Button, CustomJS, Tap, Div, BuiltinIcon, SVGIcon, InlineStyleSheet
from bokeh import events


from data_extraction import main_page_setup, filter_line_page_setup, brand_sales_graph_setup
from main_interaction import vertical_line_with_cursor, info_with_cursor, year_slider, brand_filter
from inner_interaction import model_selector, transition_page_set_up, power_shield_setup, specification_power_values, brand_page_setup


def main():
    # --------------------buttons setup----------------------#
    transition_but = Button(label="Transition Layer", button_type="success",
                            width=100, height=30)
    filter_but = Button(label="filter Layer", button_type="success",
                        width=100, height=30)

    # audi testing button (currently the background image is ferrari logo)
    audi1_button = Button(label="Audi",
                          width=100, height=30, styles={"background-image": "url('image/ferrari_logo.jpg')", "background-color": "transparent",
                                                        "background-size": "cover"})

    audi_but = Button(label="AUDI Layer", button_type="success",
                      width=100, height=30)
    bmw_but = Button(label="BWM Layer", button_type="success",
                     width=100, height=30)
    ford_inner_but = Button(label="FORD Layer", button_type="success",
                            width=100, height=30)

    # -----------------------1. main_page setup---------------------------#
    main_page = main_page_setup()
    # main page interaction
    vertical_line_with_cursor(main_page)  # show vertical lines with cursor
    info_with_cursor(main_page)  # show information when hover

    main_but = Button(label="Main Layer", button_type="success",
                      width=100, height=30)

    # main page setup
    main_page = row(
        # Ensure the main page stretches
        column(main_page, row(year_slider(main_page), filter_but, transition_but),
               Spacer(height=20), sizing_mode='stretch_both'),
        # Fix the width of the logo column
        column(Spacer(height=20), audi1_button, width=200)
    )

    # ------------------------2. filter layer-------------------------------#
    filter_line_graph, filter_line = filter_line_page_setup()
    # filter page interaction
    # show vertical lines with cursor
    vertical_line_with_cursor(filter_line_graph)
    info_with_cursor(filter_line_graph)  # show information when hover

    filter_line_page = column(filter_line_graph,
                              row(year_slider(filter_line_graph), brand_filter(filter_line_graph, filter_line),  main_but), Spacer(height=20))
    # ------------------------3. transition layer---------------------------#
    top_row, bottom_row = transition_page_set_up()

    transition_page_title = Div(
        text="<h1 style='font-size: 80px; text-align: center;'>Select Brand</h1>", height=200)

    transition_page = column(row(Spacer(width=400), transition_page_title, Spacer(width=200), column(Spacer(height=50), main_but, filter_but)),
                             top_row,
                             row(audi_but, bmw_but),
                             bottom_row)

    # ------------------------4. Brand layer---------------------------#

    audi_inner_page = row(brand_page_setup('Audi'), transition_but)
    bmw_inner_page = row(brand_page_setup('Bmw'), transition_but)
    ford_inner_page = row(brand_page_setup('Ford'), transition_but)
    # ----------------------page buttons callback----------------------#
    # main but_callback
    main_but_callback = CustomJS(args=dict(main_page=main_page, filter_page=filter_line_page, main=main_but, filter=filter_but, transition_page=transition_page, transition_but=transition_but), code="""
        main_page.visible = true;
        main.visible = false;
        transition_page.visible = false;
        transition_but.visible = true;
        filter_page.visible = false;
        filter.visible = true;
    """)
    # filter but_callback
    filter_but_callback = CustomJS(args=dict(main_page=main_page, ford_inner_page=ford_inner_page, filter_page=filter_line_page, main=main_but, filter=filter_but, transition_page=transition_page, transition_but=transition_but), code="""
        main_page.visible = false;
        main.visible = true;
        filter_page.visible = false;
        filter.visible = true;
        transition_page.visible = false;
        transition_but.visible = true;
        filter_page.visible = true;
        filter.visible = false;
    """)
    # inner but_callback
    transition_but_callback = CustomJS(args=dict(main_page=main_page, ford_inner_page=ford_inner_page, filter_page=filter_line_page, ford_inner=ford_inner_but, main=main_but, filter=filter_but, transition_page=transition_page, transition_but=transition_but, audi_inner_page=audi_inner_page, audi_but=audi_but, bmw_but=bmw_but, bmw_inner_page=bmw_inner_page), code="""
        main_page.visible = false;
        main.visible = true;
        transition_page.visible = true;
        transition_but.visible = false;
        filter_page.visible = false;
        filter.visible = true;
        ford_inner_page.visible = false;
        ford_inner.visible = true;
        audi_inner_page.visible = false;
        audi_but.visible = true;
        bmw_inner_page.visible = false;
        bmw_but.visible = true;
    """)

# ----------------------brand layer buttons callback----------------------#
    audi_but_callback = CustomJS(args=dict(main_page=main_page,  filter_page=filter_line_page, transition_page=transition_page, transition_but=transition_but, audi_inner_page=audi_inner_page, bmw_inner_page=bmw_inner_page, ford_inner_page=ford_inner_page, audi_but=audi_but), code="""
        main_page.visible = false;
        filter_page.visible = false;
        transition_page.visible = false;
        bmw_inner_page.visible = false;
        ford_inner_page.visible = false;
        audi_inner_page.visible = true;
        transition_but.visible = true;
        audi_but.visible = false;
    """)
    bmw_but_callback = CustomJS(args=dict(main_page=main_page,  filter_page=filter_line_page, transition_page=transition_page, transition_but=transition_but, audi_inner_page=audi_inner_page, bmw_inner_page=bmw_inner_page, ford_inner_page=ford_inner_page, bmw_but=bmw_but), code="""
        main_page.visible = false;
        filter_page.visible = false;
        transition_page.visible = false;
        audi_inner_page.visible = false;
        ford_inner_page.visible = false;
        transition_but.visible = true;
        bmw_inner_page.visible = true;
        bmw_but.visible = false;
    """)
    ford_inner_but_callback = CustomJS(args=dict(main_page=main_page, ford_inner_page=ford_inner_page, filter_page=filter_line_page, main=main_but, filter=filter_but, transition_page=transition_page, transition_but=transition_but), code="""
        main_page.visible = false;
        main.visible = true;
        ford_inner_page.visible = true;
        ford_inner.visible = false;
        transition_page.visible = false;
        transition_but.visible = true;
        filter_page.visible = false;
        filter.visible = true;
    """)

    # ----------------------page buttons interaction----------------------#
    main_but.js_on_click(main_but_callback)
    ford_inner_but.js_on_click(ford_inner_but_callback)
    transition_but.js_on_click(transition_but_callback)
    filter_but.js_on_click(filter_but_callback)
    bmw_but.js_on_click(bmw_but_callback)
    audi_but.js_on_click(audi_but_callback)

    # ------------------------5. show the plot---------------------------#
    # inner layer for specific car brand
    audi1_button.js_on_event(events.ButtonClick, ford_inner_but_callback)

    main_page.visible = True
    filter_line_page.visible = False
    ford_inner_page.visible = False
    transition_page.visible = False
    audi_inner_page.visible = False
    bmw_inner_page.visible = False
    # show the plot
    final_layout = layout([main_page, ford_inner_page, filter_line_page, transition_page, audi_inner_page, bmw_inner_page],
                          sizing_mode='stretch_both')
    curdoc().add_root(final_layout)

    output_file("automotive_market_dynamics.html")
    show(final_layout)


if __name__ == "__main__":
    main()
