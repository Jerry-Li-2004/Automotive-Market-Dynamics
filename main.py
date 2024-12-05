from bokeh.plotting import show, output_file
from bokeh.layouts import layout, column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Button, CustomJS, Tap, Div, BuiltinIcon, SVGIcon, InlineStyleSheet
from bokeh import events


from data_extraction import main_page_setup, filter_line_page_setup, brand_sales_graph_setup
from main_interaction import vertical_line_with_cursor, info_with_cursor, year_slider, brand_filter
from inner_interaction import model_selector, transition_page_set_up, power_shield_setup, specification_power_values


def main():
    main_page = main_page_setup()
    filter_line_page = filter_line_page_setup()
    transition_page = transition_page_set_up()

    # inner layer
    selected_brand = 'Volkswagen'
    #
    inner_layer_sales_graph = brand_sales_graph_setup(selected_brand)

    # power shield setup
    best_model, best_performance, average_performance = specification_power_values(
        selected_brand)
    visualization_title = selected_brand + " " + best_model
    best_power_shield = power_shield_setup(
        best_performance, visualization_title)
    average_power_shield = power_shield_setup(average_performance)

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
    transition_but = Button(label="Transition Layer", button_type="success",
                        width=100, height=30)
    inner_but = Button(label="Inner Layer", button_type="success",
                       width=100, height=30)
    filter_but = Button(label="filter Layer", button_type="success",
                        width=100, height=30)

    # audi testing button (currently the background image is ferrari logo)
    audi_button = Button(label="Audi",
                         width=100, height=30, styles={"background-image": "url('image/ferrari_logo.jpg')", "background-color": "transparent",
                                                       "background-size": "cover"})

    volks_golf_html = """
    <div id="audi_logo" style="text-align: right;">
        <img src="car_image/volkswagen_golf.jpg" alt="Logo" width="500" height="400" style="cursor: pointer;">
    </div>
    """
    volks_golf = Div(text=volks_golf_html)

    # stylesheet = InlineStyleSheet(
    #     css=".bk-btn { background-color: lightgray; background-image: url('your-image-url.jpg'); background-size: cover;border: none;color: white;font-size: 16px;cursor: pointer;}")

    # button = Button(label="Foo", stylesheets=[stylesheet])

    # page setup
    # 1. main page setup
    main_page = row(
        # Ensure the main page stretches
        column(main_page,
               row(year_slider(main_page), filter_but, inner_but, transition_but),
               Spacer(height=20), sizing_mode='stretch_both'),
        # Fix the width of the logo column
        column(Spacer(height=20), audi_button, width=200)
    )

    # 2. filter layer setup
    filter_line_page = column(filter_line_page,
                              row(year_slider(filter_line_page), brand_filter(filter_line_page),  main_but, inner_but), Spacer(height=20))

    transition_page_title = Div(text="<h1 style='font-size: 80px; text-align: center;'>Select Brand</h1>", height = 200)

    transition_page = column(row(Spacer(width = 400),transition_page_title, Spacer(width= 200),column(Spacer(height = 50),main_but, filter_but)),
                             transition_page)

    # 3. inner layer setup
    inner_page = column(row(volks_golf, best_power_shield, average_power_shield), inner_layer_sales_graph,
                        row(main_but, filter_but, model_selector(inner_layer_sales_graph)), sizing_mode="stretch_both")

    # main but_callback
    main_but_callback = CustomJS(args=dict(main_page=main_page, inner_page=inner_page, filter_page=filter_line_page, inner=inner_but, main=main_but, filter=filter_but, transition_page = transition_page, transition_but = transition_but), code="""
        main_page.visible = true;
        main.visible = false;
        inner_page.visible = false;
        inner.visible = true;
        transition_page.visible = false;
        transition_but.visible = true;
        filter_page.visible = false;
        filter.visible = true;
    """)
    # inner but_callback
    inner_but_callback = CustomJS(args=dict(main_page=main_page, inner_page=inner_page, filter_page=filter_line_page, inner=inner_but, main=main_but, filter=filter_but, transition_page = transition_page, transition_but = transition_but), code="""
        main_page.visible = false;
        main.visible = true;
        inner_page.visible = true;
        inner.visible = false;
        transition_page.visible = false;
        transition_but.visible = true;
        filter_page.visible = false;
        filter.visible = true;
    """)
    transition_but_callback = CustomJS(args=dict(main_page=main_page, inner_page=inner_page, filter_page=filter_line_page, inner=inner_but, main=main_but, filter=filter_but, transition_page = transition_page, transition_but = transition_but), code="""
        main_page.visible = false;
        main.visible = true;
        inner_page.visible = false;
        inner.visible = false;
        transition_page.visible = true;
        transition_but.visible = false;
        filter_page.visible = false;
        filter.visible = true;
    """)
    # filter but_callback
    filter_but_callback = CustomJS(args=dict(main_page=main_page, inner_page=inner_page, filter_page=filter_line_page, inner=filter_but, main=main_but, filter=filter_but, transition_page = transition_page, transition_but = transition_but), code="""
        main_page.visible = false;
        main.visible = true;
        inner_page.visible = false;
        inner.visible = true;
        transition_page.visible = false;
        transition_but.visible = true;
        filter_page.visible = true;
        filter.visible = false;
    """)

    main_but.js_on_click(main_but_callback)
    inner_but.js_on_click(inner_but_callback)
    transition_but.js_on_click(transition_but_callback)
    filter_but.js_on_click(filter_but_callback)

    # inner layer for specific car brand
    audi_button.js_on_event(events.ButtonClick, inner_but_callback)

    main_page.visible = True
    filter_line_page.visible = False
    inner_page.visible = False
    transition_page.visible = False
    # show the plot
    final_layout = layout([main_page, inner_page, filter_line_page, transition_page],
                          sizing_mode='stretch_both')
    curdoc().add_root(final_layout)

    output_file("automotive_market_dynamics.html")
    show(final_layout)


if __name__ == "__main__":
    main()
