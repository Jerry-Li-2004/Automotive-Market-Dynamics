from bokeh.models import HoverTool, Span, CustomJS, Slider, CheckboxGroup
from bokeh.layouts import column
from data_extraction import global_lines

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
    time_slider = Slider(start=2001,end=2015,value=2001,step=1,title="Year")
    callback = CustomJS(args = dict(main_page=main_page,time_slider=time_slider),code = """
        const year = time_slider.value;
        const start = year;                 // Calculate start of x_range
        const end = start + 5;              // Calculate end of x_range
        main_page.x_range.start = start;
        main_page.x_range.end = end; 
                        """)

    time_slider.js_on_change('value', callback)
    return time_slider

def brand_filter(main_page):
    # Create a CheckboxGroup for brand selection
    brands = [item.label['value'] for item in main_page.legend.items]
    checkbox_group = CheckboxGroup(labels=brands, active=[])

    # CustomJS to update visibility based on checkbox selection
    checkbox_callback = CustomJS(args=dict(lines=global_lines, checkbox_group=checkbox_group), code="""
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


def test():
    from bokeh.models import CheckboxGroup, CustomJS
    from bokeh.plotting import figure, show, ColumnDataSource
    from bokeh.layouts import column

    # Create sample data
    data = {
        'x': [1, 2, 3, 4, 5],
        'y1': [6, 7, 2, 4, 5],
        'y2': [1, 4, 9, 16, 25],
        'y3': [25, 16, 9, 4, 1]
    }
    source = ColumnDataSource(data=data)

    # Create a Bokeh figure
    p = figure(title="Multiple Lines with Checkboxes", width=400, height=300)

    # Add multiple lines to the plot
    line1 = p.line('x', 'y1', source=source, line_width=2, color="blue", muted_alpha=0.2, legend_label="Line 1")
    line2 = p.line('x', 'y2', source=source, line_width=2, color="green", muted_alpha=0.2, legend_label="Line 2")
    line3 = p.line('x', 'y3', source=source, line_width=2, color="red", muted_alpha=0.2, legend_label="Line 3")

    # Add interactive legend
    # p.legend.visible = False  # Hide the legend for clarity

    # Create a CheckboxGroup widget for multiple lines
    checkbox = CheckboxGroup(labels=["Line 1", "Line 2", "Line 3"], active=[0, 1, 2])  # All lines shown by default

    # Define a CustomJS callback for multiple lines
    callback = CustomJS(args=dict(lines=[line1, line2, line3]), code="""
        for (let i = 0; i < lines.length; i++) {
            if (cb_obj.active.includes(i)) {
                lines[i].muted = false; // Unmute line when corresponding checkbox is checked
            } else {
                lines[i].muted = true;  // Mute line when corresponding checkbox is unchecked
            }
        }
    """)
    checkbox.js_on_change('active', callback)

    # Layout the plot and widget
    layout = column(p, checkbox)

    # Show the result
    show(layout)

test()