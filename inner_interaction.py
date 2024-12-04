from bokeh.models import Select, CustomJS, Button, ColumnDataSource
from bokeh.models import ColumnDataSource, NumeralTickFormatter, Span, Div, Spacer
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column, row

from data_extraction import model_lines


def model_selector(inner_page):
    # Extract the data from the ColumnDataSource used in inner_page
    source = inner_page.renderers[0].data_source
    data = source.data

    # print(data)

    # Create a Select widget with options for different car models
    model_names = [line.glyph.y for line in model_lines]
    # print(model_names)
    select = Select(title="Car Model:",
                    value=model_names[0], options=model_names)

    # Add a callback to update the plot when the selection changes
    select_callback = CustomJS(args=dict(source=source, data=data, lines=model_lines), code="""
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

def transition_page_set_up():
    # Create the transition page figure
    # transition_page = Div(text="<h1 style='font-size: 80px; text-align: center;'>Select Brand</h1>")

    audi_but = Button(label="audi", button_type="success",width=275, height=70)
    bmw_but = Button(label="bmw", button_type="success",width=275, height=70)
    ford_but = Button(label="ford", button_type="success",width=275, height=70)
    kia_but = Button(label="kia", button_type="success",width=275, height=70)
    mercedes_but = Button(label="mercedes", button_type="success",width=275, height=70)
    nissan_but = Button(label="nissan", button_type="success",width=275, height=70)
    peugeot_but = Button(label="peugeot", button_type="success",width=275, height=70)
    toyota_but = Button(label="toyota", button_type="success",width=275, height=70)
    vauxhall_but = Button(label="vauxhall", button_type="success",width=275, height=70)
    volkswagen_but = Button(label="volkswagen", button_type="success",width=275, height=70)


    audi_logo_html = """<img src="image/audi_logo.jpg" width="275" height="150">"""
    bmw_logo_html = """<img src="image/bmw_logo.jpg" width="275" height="150">"""
    ford_logo_html = """<img src="image/ford_logo.jpg" width="275" height="150">"""
    kia_logo_html = """<img src="image/kia_logo.jpg" width="275" height="150">"""
    mercedes_logo_html = """<img src="image/mercedes_logo.jpg" width="275" height="150">"""
    nissan_logo_html = """<img src="image/nissan_logo.jpg" width="275" height="150">"""
    peugeot_logo_html = """<img src="image/peugeot_logo.jpg" width="275" height="150">"""
    toyota_logo_html = """<img src="image/toyota_logo.jpg" width="275" height="150">"""
    vauxhall_logo_html = """<img src="image/vauxhall_logo.jpg" width="275" height="150">"""
    volkswagen_logo_html = """<img src="image/volkswagen_logo.jpg" width="275" height="150">"""

    audi_logo = Div(text=audi_logo_html)
    bmw_logo = Div(text=bmw_logo_html)
    ford_logo = Div(text=ford_logo_html)
    kia_logo = Div(text=kia_logo_html)
    mercedes_logo = Div(text=mercedes_logo_html)
    nissan_logo = Div(text=nissan_logo_html)
    peugeot_logo = Div(text=peugeot_logo_html)
    toyota_logo = Div(text=toyota_logo_html)
    vauxhall_logo = Div(text=vauxhall_logo_html)
    volkswagen_logo = Div(text=volkswagen_logo_html)


    # Combine the figure and buttons in a layout
    layout = column(row(audi_logo,bmw_logo,ford_logo,kia_logo,mercedes_logo),
                    row(audi_but,bmw_but,ford_but,kia_but,mercedes_but),
                    row(nissan_logo,peugeot_logo,toyota_logo,vauxhall_logo,volkswagen_logo),
                    row(nissan_but,peugeot_but,toyota_but,vauxhall_but,volkswagen_but)
                    )
    # show(layout)

    return layout

# transition_page_set_up()