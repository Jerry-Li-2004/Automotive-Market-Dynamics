from bokeh.models import HoverTool, Span, CustomJS


def vertical_line_with_cursor(main_page):               #show vertical lines with cursor:
    vline = Span(location=0, dimension = 'height',line_color='black', line_width =2 , line_dash = [10,5])
    main_page.add_layout(vline)
    main_page.js_on_event('mousemove', CustomJS(args=dict(vline=vline), code="""
        const x = cb_obj.x;
        vline.location = x;
    """))
    return

def info_with_cursor(main_page):                        #show information when hover
    hover = HoverTool()
    hover.tooltips = [("Year", "@Year"), ("Volvo",
                                        "@{VOLVO}{0,0}"), ('Toyota', "@{TOYOTA}{0,0}"), ("Nissan", "@{VOLVO}{0,0}"), ("Volkswagen", "@{VOLKSWAGEN}{0,0}")]
    main_page.add_tools(hover)
    return


