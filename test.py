# bokeh dashboard switch page testing
# from bokeh.io import show
# from bokeh.layouts import column
# from bokeh.models import Button, CustomJS, Div

# # Define your different visualizations or pages
# page1 = Div(text="<h1>Page 1: Visualization 1</h1>")
# page2 = Div(text="<h1>Page 2: Visualization 2</h1>")

# # Create a button
# button1 = Button(label="Switch Page", button_type="success",
#                  width=100, height=30)

# # JavaScript callback to toggle between pages and hide the button on Page 2
# button1_callback = CustomJS(args=dict(page1=page1, page2=page2, button1=button1), code="""
#     if (page1.visible) {
#         page1.visible = false;
#         page2.visible = true;
#         button1.visible = false;
#     } else {
#         page1.visible = true;
#         page2.visible = false;
#         button1.visible = true;
#     }
# """)

# button1.js_on_click(button1_callback)

# # Initially, only page1 is visible
# page1.visible = True
# page2.visible = False

# # Layout with button and the pages
# layout = column(button1, page1, page2)

# # Show the layout
# show(layout)

import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource

# Define the data
categories = ['Price', 'Oil Price', 'Gas_emission',
              'MPG', 'Engine_power', 'Top_speed']

# oil cost: petrol, diesel, electric different costs
# all categorical data are normalized

# Average_mpg fuel econonmy
values = [4, 3, 2, 5, 4, 3]

# Number of variables
num_vars = len(categories)

# Compute angle for each axis
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # Complete the loop

# Repeat the first value to close the circular plot
values += values[:1]

# Convert to polar coordinates
x = [v * np.cos(a) for v, a in zip(values, angles)]
y = [v * np.sin(a) for v, a in zip(values, angles)]

# Create a Bokeh figure
p = figure(title="Circular Parallel Axis Plot", match_aspect=True,
           tools="", x_axis_type=None, y_axis_type=None, width=500, height=300)
p.grid.grid_line_color = None

# Add the circular plot
p.line(x, y, line_width=5)
p.circle(x, y, size=8)

# Add category labels
for i, category in enumerate(categories):
    angle = angles[i]
    x_label = 6 * np.cos(angle)
    y_label = 6 * np.sin(angle)
    p.text(x=[x_label], y=[y_label], text=[category],
           text_align="center", text_baseline="middle")

# Add parallel axes
for angle in angles[:-1]:  # Exclude the last angle to avoid duplicate axis
    p.line([0, 5 * np.cos(angle)], [0, 5 * np.sin(angle)],
           line_dash="dotted", line_color="gray")

# Show the plot
output_file("circular_parallel_axis_plot.html")
show(p)
