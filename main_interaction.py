from bokeh.models import HoverTool, Span, CustomJS, Slider
from bokeh.layouts import column, row, Spacer


def vertical_line_with_cursor(main_page):  # show vertical lines with cursor:
    vline = Span(location=0, dimension='height',
                 line_color='black', line_width=2, line_dash=[10, 5])
    main_page.add_layout(vline)
    main_page.js_on_event('mousemove', CustomJS(args=dict(vline=vline), code="""
        const x = cb_obj.x;
        vline.location = x;
    """))
    return


def info_with_cursor(main_page):  # show information when hover
    # sales_data = get_all_sales_data()
    hover = HoverTool()
    hover.tooltips = [("Year", "@Year"), ("Ford",
                                          "@{FORD}{0,0}"), ('Vauxhall', "@{VAUXHALL}{0,0}"), ("Volkswagen", "@{VOLKSWAGEN}{0,0}")]
    main_page.add_tools(hover)
    return


def year_slider(main_page):
    time_slider = Slider(start=2001, end=2015,
                         value=2001, step=1, title="Year")
    callback = CustomJS(args=dict(main_page=main_page, time_slider=time_slider), code="""
        const year = time_slider.value;
        const start = year;                 // Calculate start of x_range
        const end = start + 5;              // Calculate end of x_range
        main_page.x_range.start = start;
        main_page.x_range.end = end; 
                        """)

    time_slider.js_on_change('value', callback)
    centered_slider = row(Spacer(width=90), time_slider, Spacer(width=90))
    main_page_layout = column(main_page, centered_slider, Spacer(height=20))
    return main_page_layout
