from bokeh.io import curdoc
from bokeh.models import Button
from bokeh.io import show
from bokeh.layouts import column
from bokeh.models import Select, CustomJS, Button, Spacer, Div, HelpButton, Tooltip
from bokeh.models.dom import HTML
from bokeh.models import Div
from bokeh.plotting import figure, show
from bokeh.layouts import column, row
import pandas as pd
import numpy as np

from data_extraction import brand_sales_graph_setup, predicted_price_graph_setup
from main_interaction import info_with_cursor, vertical_line_with_cursor, year_slider


def model_selector(inner_page, model_lines):
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

    audi_logo_html = """<img src="brand_logo/1.png" width="275" height="150">"""
    bmw_logo_html = """<img src="brand_logo/2.png" width="275" height="150">"""
    ford_logo_html = """<img src="brand_logo/3.png" width="275" height="150">"""
    kia_logo_html = """<img src="brand_logo/4.png" width="275" height="150">"""
    mercedes_logo_html = """<img src="brand_logo/5.png" width="275" height="150">"""
    nissan_logo_html = """<img src="brand_logo/6.png" width="275" height="150">"""
    peugeot_logo_html = """<img src="brand_logo/7.png" width="275" height="150">"""
    toyota_logo_html = """<img src="brand_logo/8.png" width="275" height="150">"""
    vauxhall_logo_html = """<img src="brand_logo/9.png" width="275" height="150">"""
    volkswagen_logo_html = """<img src="brand_logo/10.png" width="275" height="150">"""

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
    layout = column(row(audi_logo, bmw_logo, ford_logo, kia_logo, mercedes_logo),
                    # row(audi_but,bmw_but,ford_but,kia_but,mercedes_but),
                    row(nissan_logo, peugeot_logo, toyota_logo,
                        vauxhall_logo, volkswagen_logo),
                    # row(nissan_but,peugeot_but,toyota_but,vauxhall_but,volkswagen_but)
                    )
    top_row = row(audi_logo, bmw_logo, ford_logo, kia_logo, mercedes_logo)
    bottom_row = row(nissan_logo, peugeot_logo, toyota_logo,
                     vauxhall_logo, volkswagen_logo)
    # show(layout)

    return top_row, bottom_row


def normalize_values(data):
    # Transpose the dictionary to work with columns
    transposed_data = list(zip(*data.values()))

    # Normalize each column
    normalized_data = []
    for col in transposed_data:
        min_val = min(col)
        max_val = max(col)
        normalized_col = [(val - min_val) / (max_val - min_val)
                          * 1 if max_val != min_val else 0 for val in col]
        normalized_data.append(normalized_col)

    # Transpose back to original structure
    normalized_data = list(zip(*normalized_data))

    # Create a new dictionary with normalized values
    normalized_dict = {key: list(values)
                       for key, values in zip(data.keys(), normalized_data)}

    return normalized_dict


def find_best_car_ID(car_data):
    # Calculate the average of 5 elements in the list for each key
    averages = {key: sum(values) / len(values)
                for key, values in car_data.items()}

    # Find the key with the highest average value
    best_car_ID = max(averages, key=averages.get)

    return best_car_ID


def find_best_car(car_data):
    ad_df = pd.read_csv("data_cleaning/Ad_table.csv")
    best_car_ID = find_best_car_ID(car_data)

    # Find the car name based on the best car ID
    car_name = ad_df.loc[ad_df['Genmodel_ID']
                         == best_car_ID, 'Genmodel'].values

    # Handle the case where no matching Genmodel_ID is found
    if len(car_name) > 0:
        return car_name[0]
    else:
        return "Car ID not found"


def specification_power_values(brand_name=None):
    # brand_name = 'Audi'
    # required dataset
    price_df = pd.read_csv("data_cleaning/Price_table.csv")
    sales_df = pd.read_csv("data_cleaning/Sales_table.csv")
    ad_table_df = pd.read_csv("data_cleaning/Ad_table.csv")

    car_brand_directory = {}
    data = {}
    # Price average for each series (1)
    car_price = price_df.loc[price_df['Maker']
                             == brand_name, ["Genmodel", "Genmodel_ID", "Entry_price"]]
    car_price = car_price[car_price['Entry_price'] != 0]
    price_average = car_price.groupby('Genmodel_ID')['Entry_price'].mean()
    price_average = price_average.to_dict()
    # print(price_average)

    # Average_mpg (3), Engine power (4), Top speed (5)
    car_spec = ad_table_df.loc[ad_table_df['Maker']
                               == brand_name, ['Genmodel', "Genmodel_ID", 'Average_mpg', 'Engine_power', 'Top_speed']]

    car_spec = car_spec.dropna()
    car_spec['Average_mpg'] = car_spec['Average_mpg'].str.replace(
        ' mpg', '').astype(float)
    car_spec['Top_speed'] = car_spec['Top_speed'].str.replace(
        ' mph', '').astype(float)
    car_spec_average = car_spec.groupby(
        'Genmodel_ID')[['Average_mpg', 'Engine_power', 'Top_speed']].mean()
    car_spec_average = car_spec_average.to_dict()

    # Sales data (2)
    car_sales = sales_df.loc[sales_df['Maker'] == brand_name]
    car_gen_model_names = car_sales['Genmodel_ID'].drop_duplicates().to_list()

    for genmodel in car_gen_model_names:
        specific_genmodel_df = car_sales[car_sales['Genmodel_ID'] == genmodel]
        sales_columns = car_sales.columns[3:]
        sales_total = specific_genmodel_df[sales_columns].sum(axis=1).values[0]
        data[genmodel] = [0, 0, 0, 0, 0]
        data[genmodel][0] = sales_total
    # at this stage we found the sales total (popularity) of each car gen model
    new_data = {key.split()[-1]: value for key, value in data.items()}
    # print(new_data)
    gen_model_names = list(new_data.keys())
    # print(gen_model_names)
    for genmodel in gen_model_names:
        if (genmodel in price_average.keys() and genmodel in car_spec_average['Average_mpg'].keys()):
            new_data[genmodel][1] = price_average[genmodel]
            new_data[genmodel][2] = car_spec_average['Average_mpg'][genmodel]
            new_data[genmodel][3] = car_spec_average['Engine_power'][genmodel]
            new_data[genmodel][4] = car_spec_average['Top_speed'][genmodel]

    car_brand_directory[brand_name] = new_data
    car_brand_directory[brand_name] = {
        k: v for k, v in car_brand_directory[brand_name].items() if all(value != 0 for value in v)}

    car_brand_directory[brand_name] = normalize_values(
        car_brand_directory[brand_name])  # normalization

    for genmodel in car_brand_directory[brand_name].keys():
        car_brand_directory[brand_name][genmodel][1] = 1 - \
            car_brand_directory[brand_name][genmodel][1]
        # car_brand_directory[brand_name][genmodel][3] = 1 - \
        #     car_brand_directory[brand_name][genmodel][3]
        # reverse price, engine power scale, lower price higher score
    # index 0: sales (higher popularity, higher score), 1: price (lower price, higher score])
    # 2: Average_mpg (higher the higher), 3: Engine power (lower the best, cost saving), 4: Top speed (higher the better)

    average_performance = [sum(x) / len(x)
                           for x in zip(*car_brand_directory[brand_name].values())]

    return find_best_car(car_brand_directory[brand_name]), car_brand_directory[brand_name][find_best_car_ID(car_brand_directory[brand_name])], average_performance


def power_shield_setup(performance_values, visualization_title=None):
    categories = ['Sales', 'Price (Low)',
                  'Fuel Effiency', 'Horsepower', 'Top Speed']

    # oil cost: petrol, diesel, electric different costs
    # all categorical data are normalized

    multiplier = 3
    values = [x * multiplier for x in performance_values]
    num_vars = len(categories)
    # compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the loop

    # repeat the first value to close the circular plot
    values += values[:1]

    # Convert to polar coordinates
    x = [v * np.cos(a) for v, a in zip(values, angles)]
    y = [v * np.sin(a) for v, a in zip(values, angles)]

    # Convert to polar coordinates for the outer edges
    outer_x = [multiplier * np.cos(a) for a in angles]
    outer_y = [multiplier * np.sin(a) for a in angles]

    if (visualization_title == None):
        visualization_title = "Average Car Model Performance"
    else:
        visualization_title = "Top Car Model Performance: " + visualization_title

    p = figure(title=visualization_title, match_aspect=True,
               tools="", x_axis_type=None, y_axis_type=None, width=500, height=400)
    p.grid.grid_line_color = None
    p.title.text_font_size = '12pt'
    # add the circular plot
    p.line(x, y, line_width=5)
    p.line(outer_x, outer_y, line_width=1,
           line_dash="dotted", line_color="gray")
    p.circle(x, y, size=5)

    # add category labels
    for i, category in enumerate(categories):
        angle = angles[i]
        x_label = 3.8 * np.cos(angle)
        y_label = 3.8 * np.sin(angle)
        category = category + "\n" + \
            str(round(performance_values[i]*10, 1)) + " / 10"
        p.text(x=[x_label], y=[y_label], text=[category],
               text_align="center", text_baseline="middle", text_font_size="10pt")

    # add parallel axes
    for angle in angles[:-1]:  # exclude the last angle to avoid duplicate axis
        p.line([0, multiplier * np.cos(angle)], [0, multiplier *
               np.sin(angle)], line_dash="dotted", line_color="gray")

    return p


def get_top_performance_model_html(brand):
    part1 = """<div id="logo" style="text-align: right;"> <img src="car_image/"""
    part2 = str(brand) + """.jpg" """
    part3 = """alt="Logo" width="500" height="400" style="cursor: pointer;"></div>"""
    return (part1+part2+part3)


def brand_page_setup(target_brand):
    logo_html = """<img src="brand_logo/2.png" width="275" height="150">"""

    brand_logos = {
        'Audi': '1.png',
        'BMW': '2.png',
        'Ford': '3.png',
        'Kia': '4.png',
        'Mercedes': '5.png',
        'Nissan': '6.png',
        'Peugeot': '7.png',
        'Toyota': '8.png',
        'Vauxhall': '9.png',
        'Volkswagen': '10.png'
    }

    if target_brand in brand_logos:
        logo_html = f"""<img src="brand_logo/{
            brand_logos[target_brand]}" width="275" height="150">"""

    logo = Div(text=logo_html)
    inner_layer_sales_graph, model_lines = brand_sales_graph_setup(
        target_brand)
    inner_layer_predicted_price_graph, predicted_model_lines = predicted_price_graph_setup(
        target_brand)
    # inner_layer_sales_graph.width = 250
    # inner_layer_predicted_price_graph.width = 250

    # top model photo
    top_performance_model_html = get_top_performance_model_html(target_brand)
    # top_performance_model_html = """
    # <div id="audi_logo" style="text-align: right;">
    #     <img src="car_image/volkswagen_golf.jpg" alt="Logo" width="500" height="400" style="cursor: pointer;">
    # </div>
    # """
    top_performance_model = Div(text=top_performance_model_html)

    # power shield setup
    best_model, best_performance, average_performance = specification_power_values(
        target_brand)
    visualization_title = target_brand + " " + best_model
    best_power_shield = power_shield_setup(
        best_performance, visualization_title)
    average_power_shield = power_shield_setup(average_performance)

    # inner page interaction
    # vertical_line_with_cursor(inner_layer_sales_graph)
    # info_with_cursor(inner_layer_sales_graph)  # show information when hover

    brand_page = row(column(row(logo, model_selector(inner_layer_sales_graph, model_lines), top_performance_model),
                            row(column(inner_layer_sales_graph, year_slider(inner_layer_sales_graph))), sizing_mode="stretch_both"), column(info_box(), best_power_shield, average_power_shield))
    # show(brand_page)
    return brand_page

# brand_page_setup('Audi')


def info_box():
    help_button = HelpButton(tooltip=Tooltip(content=HTML("""
    <b> formula for power shield </b>
    """), position="right"))
    return help_button

# show(column(extra_info()))
