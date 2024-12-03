
from bokeh.models import Select, CustomJS

from data_extraction import model_lines


def model_selector(inner_page):
    # Extract the data from the ColumnDataSource used in inner_page
    source = inner_page.renderers[0].data_source
    data = source.data

    # print(data)

    # Create a Select widget with options for different car models
    model_names = [line.glyph.y for line in model_lines]
    # print(model_names)
    select = Select(title="Car Model:", value=model_names[0], options=model_names)

    # Add a callback to update the plot when the selection changes
    select_callback = CustomJS(args=dict(source=source, data=data,lines = model_lines), code="""
        const selected_model = cb_obj.value;

        for (let i = 0; i < lines.length; i++) {
            if (cb_obj.value == lines[i].glyph.y.field) {
                lines[i].visible = true; // Unmute line when corresponding checkbox is checked
            } else {
                lines[i].visible = false; // Unmute line when corresponding checkbox is checked
            }
        }
    """)
    select.js_on_change('value', select_callback)

    return select
