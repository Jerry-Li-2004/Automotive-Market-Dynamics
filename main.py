from bokeh.plotting import show, output_file
from bokeh.layouts import layout, column, row, Spacer
from bokeh.io import curdoc
from bokeh.models import Button, CustomJS, TapTool, Div

from data_extraction import main_page_setup, filter_line_page_setup
from main_interaction import vertical_line_with_cursor, info_with_cursor, year_slider, brand_filter


def main():
    main_page = main_page_setup()
    filter_line_page  = filter_line_page_setup()
    # main page interaction
    vertical_line_with_cursor(main_page)  # show vertical lines with cursor
    info_with_cursor(main_page)  # show information when hover

    # inner page interaction
    vertical_line_with_cursor(filter_line_page)  # show vertical lines with cursor
    info_with_cursor(filter_line_page)  # show information when hover


    # buttons for page switching
    button1 = Button(label="Inner Layer", button_type="success",
                     width=100, height=30)

    button2 = Button(label="Main Layer", button_type="success",
                     width=100, height=30)

    # page setup
    # 1. main page setup
    main_page = column(main_page,
                       row(year_slider(main_page),  button1), Spacer(height=20))

    # 2. inner layer setup
    filter_line_page = column(filter_line_page , 
                       row(year_slider(filter_line_page ), brand_filter(filter_line_page ),  button2), Spacer(height=20))

    # button1_callback
    button1_callback = CustomJS(args=dict(main_page=main_page, inner_page=filter_line_page, button1=button1, button2=button2), code="""
        main_page.visible = false;
        button1.visible = false;
        button2.visible = true;
        inner_page.visible = true;      
    """)

    # button1_callback
    button2_callback = CustomJS(args=dict(main_page=main_page, inner_page=filter_line_page, button1=button1, button2=button2), code="""
        main_page.visible = true;
        button1.visible = true;
        button2.visible = false;
        inner_page.visible = false;                  
    """)

    button1.js_on_click(button1_callback)
    button2.js_on_click(button2_callback)

    main_page.visible = True
    filter_line_page.visible = False
    # show the plot
    final_layout = layout([[main_page, filter_line_page]],
                          sizing_mode='stretch_both')
    curdoc().add_root(final_layout)

    output_file("automotive_market_dynamics.html")
    show(final_layout)


if __name__ == "__main__":
    main()
