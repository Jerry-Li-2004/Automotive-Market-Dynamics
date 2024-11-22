from bokeh.models import HoverTool, Span, CustomJS
from data_extraction import get_all_sales_data


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

import numpy as np

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import figure, show



def year_slider():
    x = np.linspace(0, 10, 500)
    y = x
    source = ColumnDataSource(data=dict(x=x, y=y))
    plot = figure(y_range=(-10, 10),x_range=(0,10), width=400, height=400)
    plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
    

    time_slider = Slider(start=2001,end=2021,value=2001,step=5,title="Year")
    callback = CustomJS(args = dict(plot=plot,time_slider=time_slider),code = """
        const year = time_slider.value;
        const start = (year - 2001) / 20 * 10;  // Calculate start of x_range
        const end = start + 10;  // Calculate end of x_range
        plot.x_range.start = start;
        plot.x_range.end = end; 
                        """)

    time_slider.js_on_change('value',callback)
    show(row(plot, column(time_slider)))

year_slider()



# x = np.linspace(0, 10, 500)
# y = np.sin(x)

# source = ColumnDataSource(data=dict(x=x, y=y))

# plot = figure(y_range=(-10, 10), width=400, height=400)

# plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

# amp = Slider(start=0.1, end=10, value=1, step=.1, title="Amplitude")
# freq = Slider(start=0.1, end=10, value=1, step=.1, title="Frequency")
# phase = Slider(start=-6.4, end=6.4, value=0, step=.1, title="Phase")
# offset = Slider(start=-9, end=9, value=0, step=.1, title="Offset")

# callback = CustomJS(args=dict(source=source, amp=amp, freq=freq, phase=phase, offset=offset),
#                     code="""
#     const A = amp.value
#     const k = freq.value
#     const phi = phase.value
#     const B = offset.value

#     const x = source.data.x
#     const y = Array.from(x, (x) => B + A*Math.sin(k*x+phi))
#     source.data = { x, y }
# """)

# amp.js_on_change('value', callback)
# freq.js_on_change('value', callback)
# phase.js_on_change('value', callback)
# offset.js_on_change('value', callback)

# show(row(plot, column(amp, freq, phase, offset)))