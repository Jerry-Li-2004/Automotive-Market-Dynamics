from bokeh.models import HoverTool, Span, CustomJS, Slider, CheckboxGroup
from bokeh.layouts import row, Spacer


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
    time_slider = Slider(start=2001, end=2020,
                         value=2001, step=1, title="Year")
    callback = CustomJS(args=dict(main_page=main_page, time_slider=time_slider), code="""
        const year = time_slider.value;
        const start = year;                 // Calculate start of x_range
        const end = start + 5;              // Calculate end of x_range
        main_page.x_range.start = start;
        main_page.x_range.end = end; 
                        """)

    time_slider.js_on_change('value', callback)
    return time_slider


def main_page_year_slider(main_page):
    time_slider = Slider(start=2001, end=2020,
                         value=2001, step=1, title="Year")
    callback = CustomJS(args=dict(main_page=main_page, time_slider=time_slider), code="""
        const year = time_slider.value;
        const start = year;                 // Calculate start of x_range
        const end = start + 5;              // Calculate end of x_range
        main_page.x_range.start = start;
        main_page.x_range.end = end; 
                        """)

    time_slider.js_on_change('value', callback)
    return time_slider


def brand_filter(main_page, filter_lines):
    # Create a CheckboxGroup for brand selection
    brands = [item.label['value'] for item in main_page.legend.items]
    checkbox_group = CheckboxGroup(
        labels=brands, active=[], sizing_mode='stretch_width', inline=True)

    # CustomJS to update visibility based on checkbox selection
    checkbox_callback = CustomJS(args=dict(lines=filter_lines, checkbox_group=checkbox_group), code="""
        for (let i = 0; i < lines.length; i++) {
            if (cb_obj.active.includes(i)) {
                lines[i].visible = true; // Unmute line when corresponding checkbox is checked
            } else {
                lines[i].visible = false;  // Mute line when corresponding checkbox is unchecked
            }
        }
    """)

    checkbox_group.js_on_change('active', checkbox_callback)

    # Add the checkbox group to the layout
    return checkbox_group
