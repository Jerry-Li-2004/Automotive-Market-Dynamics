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

from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.plotting import figure
from bokeh.layouts import gridplot
from bokeh.io import show, output_file
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource

# Define the data
categories = ['sales', 'price', 'MPG', 'engine_power', 'Top_speed']

# oil cost: petrol, diesel, electric different costs
# all categorical data are normalized

# Average_mpg fuel econonmy
values = [4, 3, 2, 5, 3]

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

# # grid plot examples

# # Create some sample data
# x = [1, 2, 3, 4, 5]
# y1 = [6, 7, 2, 4, 5]
# y2 = [1, 4, 3, 2, 6]
# y3 = [2, 3, 5, 7, 6]
# y4 = [4, 6, 7, 2, 3]

# # Create four different plots
# plot1 = figure(title="Line Plot")
# plot1.line(x, y1)

# plot2 = figure(title="Scatter Plot")
# plot2.scatter(x, y2)

# plot3 = figure(title="Circle Plot")
# plot3.circle(x, y3)

# plot4 = figure(title="Triangle Plot")
# plot4.triangle(x, y4)

# # Arrange the plots in a grid layout
# grid = gridplot([[plot1, plot2], [plot3, plot4]])

# # Output the visualization to an HTML file
# output_file("dashboard.html")

# # Show the dashboard
# show(grid)


# frame setup
# from bokeh.io import show, output_file
# from bokeh.layouts import row
# from bokeh.models import ColumnDataSource, ImageURL
# from bokeh.plotting import figure
# import os

# # Sample data for the plot
# x = [1, 2, 3, 4, 5]
# y = [6, 7, 2, 4, 5]

# # Create a plot
# plot = figure(title="Line Plot", width=400, height=400)
# plot.line(x, y)

# # Local image paths (replace with your own image paths)
# image_paths = ["image/audi_logo.jpg", "image/ferrari_logo.jpg"]

# # Convert local paths to URLs
# # image_urls = ["file://" + os.path.abspath(path) for path in image_paths]

# # Create a ColumnDataSource with image URLs
# source = ColumnDataSource(
#     data=dict(url=image_paths, x=[0.5, 0.5], y=[0.75, 0.25]))

# # Create a figure for images
# image_plot = figure(x_range=(0, 1), y_range=(0, 1), width=800, height=400)
# image_plot.image_url(url="url", x="x", y="y", w=0.9, h=0.8, source=source)

# # Hide grid lines and axes for the image plot
# image_plot.grid.visible = False
# image_plot.axis.visible = False

# # Arrange the plot and images in a layout
# layout = row(plot, image_plot)

# # Output the visualization to an HTML file
# output_file("dashboard_with_local_images_outside.html")

# # Show the dashboard
# show(layout)
