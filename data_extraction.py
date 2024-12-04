import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, NumeralTickFormatter, Span
from bokeh.plotting import figure, show, output_file

from bokeh.palettes import Category20

filter_lines = []
model_lines = []


def get_all_sales_data():
    data = {'Total_Sales': []}

    sales_df = pd.read_csv("dataset/Sales_table.csv")
    sales_data_df = sales_df.drop(columns=['Maker', 'Genmodel', 'Genmodel_ID'])

    # all car brand name
    car_brand_names = sales_df['Maker'].drop_duplicates().to_list()
    for brand in car_brand_names:
        data[brand] = sales_data_df[sales_df['Maker']
                                    == brand].sum(axis=0).values[::-1]
        data['Total_Sales'].append((brand, sum(data[brand])))

    data['Total_Sales'] = sorted(
        data['Total_Sales'], key=lambda n: n[1])[::-1][0:10]

    data["Top_10_Brands"] = [t[0] for t in data['Total_Sales']]

    # higher sale on upper position
    data['Top_10_Brands'] = data['Top_10_Brands'][::-1]

    return data


def get_sales_forecast_data():
    data = {'Total_Sales': []}

    sales_df = pd.read_csv("prediction_analysis/Projected_Sales_data.csv")
    columns = list(sales_df.columns)
    df_segment0 = columns[0:3]
    df_segment1 = columns[3:23]
    df_segment2 = columns[23:29]
    reorder_sequence = df_segment0 + df_segment2[::-1] + df_segment1
    sales_df = sales_df[reorder_sequence]
    sales_data_df = sales_df.drop(columns=['Maker', 'Genmodel', 'Genmodel_ID'])

    # all car brand name
    car_brand_names = sales_df['Maker'].drop_duplicates().to_list()
    for brand in car_brand_names:
        data[brand] = sales_data_df[sales_df['Maker']
                                    == brand].sum(axis=0).values[::-1]
        data['Total_Sales'].append((brand, sum(data[brand])))

    data['Total_Sales'] = sorted(
        data['Total_Sales'], key=lambda n: n[1])[::-1][0:10]

    data["Top_10_Brands"] = [t[0] for t in data['Total_Sales']]

    # higher sale on upper position
    data['Top_10_Brands'] = data['Top_10_Brands'][::-1]

    return data


def get_brand_sales_data(brand):  # extract tip 10 sales of specific brand
    sales_df = pd.read_csv("data_cleaning/Sales_table.csv")
    sales_df = sales_df.drop(columns=['Genmodel_ID'])
    sales_df['Genmodel'] = sales_df['Genmodel'].str.replace(f'{brand} ', '')

    brand_sales = sales_df[sales_df['Maker'] == brand]
    year_columns = brand_sales.columns[2:]
    brand_sales['Total_Sales'] = brand_sales[year_columns].sum(axis=1)

    brand_sales = brand_sales.nlargest(10, 'Total_Sales')

    # print(brand_sales['Genmodel'])
    return brand_sales


def get_sales_data():

    sales_df = pd.read_csv("dataset/Sales_table.csv")
    sales_data_df = sales_df.drop(columns=['Maker', 'Genmodel', 'Genmodel_ID'])

    volvo_sales = sales_data_df[sales_df['Maker'] == 'VOLVO']
    toyota_sales = sales_data_df[sales_df['Maker'] == 'TOYOTA']
    nissan_sales = sales_data_df[sales_df['Maker'] == 'NISSAN']
    volkswagen_sales = sales_data_df[sales_df['Maker'] == 'VOLKSWAGEN']

    total_volvo_sales = volvo_sales.sum(axis=0).values
    total_toyota_sales = toyota_sales.sum(axis=0).values
    total_nissan_sales = nissan_sales.sum(axis=0).values
    total_volkswagen_sales = volkswagen_sales.sum(axis=0).values
    return total_volvo_sales[::-1], total_toyota_sales[::-1], total_nissan_sales[::-1], total_volkswagen_sales[::-1]


def main_page_setup():
    # extract the data
    # sales_data = get_all_sales_data()
    # years = np.arange(2001, 2021)
    sales_data = get_sales_forecast_data()
    years = np.arange(2001, 2027)

    data = pd.DataFrame({'Year': years})
    for brand in sales_data['Top_10_Brands']:
        data[brand] = sales_data[brand]

    source = ColumnDataSource(data)

    main_page = figure(title="Automotive Market Dynamics Visualization", x_axis_label='Year',
                       y_axis_label='Sales', sizing_mode='stretch_height', width=1200)

    colors = Category20[len(sales_data['Top_10_Brands'])]
    main_page.varea_stack(stackers=sales_data['Top_10_Brands'],
                          x='Year', color=colors, source=source, legend_label=sales_data['Top_10_Brands'])

    vline = Span(location=2020, dimension='height',
                 line_color='Blue', line_width=2)
    main_page.add_layout(vline)

    main_page.yaxis.formatter = NumeralTickFormatter(format="0,0")
    main_page.title.text_font_size = '20pt'
    main_page.legend.location = "top_left"
    main_page.legend.orientation = "horizontal"
    # main_page.legend.click_policy="hide"

    return main_page


def filter_line_page_setup():
    global filter_lines
    # extract the data
    # sales_data = get_all_sales_data()
    # years = np.arange(2001, 2021)

    # sales forecasting
    sales_data = get_sales_forecast_data()
    years = np.arange(2001, 2027)

    data = pd.DataFrame({'Year': years})
    for brand in sales_data['Top_10_Brands']:
        data[brand] = sales_data[brand]

    source = ColumnDataSource(data)

    main_page = figure(title="Automotive Market Dynamics Visualization", x_axis_label='Year',
                       y_axis_label='Sales', sizing_mode='stretch_height', width=1200)

    colors = Category20[len(sales_data['Top_10_Brands'])]

    for brand, color in zip(sales_data['Top_10_Brands'], colors):
        line = main_page.line(x='Year', y=brand, line_width=4,
                              color=color, source=source, legend_label=brand)
        filter_lines.append(line)

    vline = Span(location=2020, dimension='height',
                 line_color='Blue', line_width=2)
    main_page.add_layout(vline)

    main_page.yaxis.formatter = NumeralTickFormatter(format="0,0")
    main_page.title.text_font_size = '20pt'
    main_page.legend.location = "top_left"
    main_page.legend.orientation = "horizontal"
    # main_page.legend.click_policy="hide"

    return main_page


def brand_sales_graph_setup(brand_name):
    global model_lines
    # extract the data
    sales_data = get_brand_sales_data(brand_name)
    years = np.arange(2001, 2021)

    data = pd.DataFrame({'Year': years})
    for model in sales_data['Genmodel']:
        # print(model[6:])
        model_row = sales_data.loc[sales_data['Genmodel'] == model]
        # Assuming the sales data starts from the 3rd column to the second last column
        sales_values = model_row.iloc[0, 2:-1].values
        data[model] = sales_values

    source = ColumnDataSource(data)

    inner_page = figure(title="Automotive Market Dynamics Visualization", x_axis_label='Year',
                        y_axis_label='Sales', sizing_mode='stretch_height', width=1200)

    colors = Category20[len(sales_data['Genmodel'])]

    for model, color in zip(sales_data['Genmodel'], colors):
        line = inner_page.line(x='Year', y=model, line_width=4,
                               color=color, source=source, legend_label=model)
        model_lines.append(line)

    for i in range(len(model_lines)):
        if (i > 0):
            model_lines[i].visible = False

    # inner_page.add_layout(line)
    inner_page.yaxis.formatter = NumeralTickFormatter(format="0,0")
    inner_page.title.text_font_size = '20pt'
    inner_page.legend.location = "top_left"
    inner_page.legend.orientation = "horizontal"
    # inner_page.legend.click_policy="hide"

    return inner_page


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
    categories = ['Sales', 'Price (low)',
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
