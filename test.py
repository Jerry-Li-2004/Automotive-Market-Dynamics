from bokeh.io import show
from bokeh.layouts import column
from bokeh.models import Button, CustomJS, Div

# Define your different visualizations or pages
page1 = Div(text="<h1>Page 1: Visualization 1</h1>")
page2 = Div(text="<h1>Page 2: Visualization 2</h1>")

# Create a button
button1 = Button(label="Switch Page", button_type="success",
                 width=100, height=30)

# JavaScript callback to toggle between pages and hide the button on Page 2
button1_callback = CustomJS(args=dict(page1=page1, page2=page2, button1=button1), code="""
    if (page1.visible) {
        page1.visible = false;
        page2.visible = true;
        button1.visible = false;
    } else {
        page1.visible = true;
        page2.visible = false;
        button1.visible = true;
    }
""")

button1.js_on_click(button1_callback)

# Initially, only page1 is visible
page1.visible = True
page2.visible = False

# Layout with button and the pages
layout = column(button1, page1, page2)

# Show the layout
show(layout)
