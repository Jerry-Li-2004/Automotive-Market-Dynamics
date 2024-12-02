from bokeh.models import HoverTool, Span, CustomJS, Slider, TapTool, Button, CheckboxGroup
from bokeh.layouts import column, row, Spacer

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
    centered_slider = row(Spacer(width=90), time_slider,
                          Spacer(width=90))
    # main_page_layout = column(main_page, centered_slider, Spacer(height=20))
    return centered_slider


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

def model_selector(inner_page):
    from bokeh.models import ColumnDataSource, Select, CustomJS
    brands = [item.label['value'] for item in inner_page.legend.items]
    selector = Select(title="Car Model", value = "Toyota", options = list(brands.keys()))

    # select_callback = CustomJS(args=dict(source=source, data=data), code="""
    #     // Update the source data with the selected model
    #     const selected_model = cb_obj.value;
    #     source.data = data[selected_model];
    #     source.change.emit();
    # """)
    # selector.js_on_change('value', select_callback)



def test():
    from bokeh.models import ColumnDataSource, Select, CustomJS
    from bokeh.plotting import figure, show
    from bokeh.layouts import column

    # Sample data for multiple car models
    data = {
        'Toyota': {'x': [1, 2, 3, 4], 'y': [4, 7, 6, 5]},
        'Honda': {'x': [1, 2, 3, 4], 'y': [1, 3, 5, 7]},
        'BMW': {'x': [1, 2, 3, 4], 'y': [7, 6, 5, 4]},
    }

    # Create a ColumnDataSource and initialize with one model's data
    source = ColumnDataSource(data=data['Toyota'])

    # Create a plot
    p = figure(title="Car Models", width=600, height=400)
    line = p.line('x', 'y', source=source, line_width=2, color='blue')

    # Create a Select widget
    select = Select(title="Car Model:", value="Toyota", options=list(data.keys()))

    # Add a callback to update the plot when the selection changes
    select_callback = CustomJS(args=dict(source=source, data=data), code="""
        // Update the source data with the selected model
        const selected_model = cb_obj.value;
        source.data = data[selected_model];
        source.change.emit();
    """)
    select.js_on_change('value', select_callback)

    # Layout
    layout = column(select, p)
    show(layout)


# test() 