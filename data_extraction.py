import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, NumeralTickFormatter, Span
from bokeh.plotting import figure
from bokeh.palettes import Category20


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
    filter_lines = []
    sales_data = get_sales_forecast_data()
    years = np.arange(2001, 2027)

    data = pd.DataFrame({'Year': years})
    for brand in sales_data['Top_10_Brands']:
        data[brand] = sales_data[brand]

    source = ColumnDataSource(data)

    filter_page = figure(title="Automotive Market Dynamics Visualization", x_axis_label='Year',
                         y_axis_label='Sales', sizing_mode='stretch_height', width=1200)

    colors = Category20[len(sales_data['Top_10_Brands'])]

    for brand, color in zip(sales_data['Top_10_Brands'], colors):
        line = filter_page.line(x='Year', y=brand, line_width=4,
                                color=color, source=source, legend_label=brand)
        filter_lines.append(line)

    vline = Span(location=2020, dimension='height',
                 line_color='Blue', line_width=2)
    filter_page.add_layout(vline)

    filter_page.yaxis.formatter = NumeralTickFormatter(format="0,0")
    filter_page.title.text_font_size = '20pt'
    filter_page.legend.location = "top_left"
    filter_page.legend.orientation = "horizontal"
    # filter_page.legend.click_policy="hide"

    return filter_page, filter_lines


def brand_sales_graph_setup(brand_name):
    model_lines = []
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

    inner_page = figure(title=brand_name + "'s Model Sales Performance Trackers", x_axis_label='Year',
                        y_axis_label='Sales', width=500, height=400)

    colors = Category20[len(sales_data['Genmodel'])]

    # current version (without legend)
    for model, color in zip(sales_data['Genmodel'], colors):
        line = inner_page.line(x='Year', y=model, line_width=4,
                               color=color, source=source)
        model_lines.append(line)

    # previous version (with legend)
    # for model, color in zip(sales_data['Genmodel'], colors):
    #     line = inner_page.line(x='Year', y=model, line_width=4,
    #                            color=color, source=source, legend_label=model)
    #     model_lines.append(line)

    for i in range(len(model_lines)):
        if (i > 0):
            model_lines[i].visible = False

    # inner_page.add_layout(line)
    inner_page.yaxis.formatter = NumeralTickFormatter(format="0,0")
    inner_page.title.text_font_size = '12pt'
    # inner_page.legend.location = "top_left"
    # inner_page.legend.orientation = "horizontal"
    # inner_page.legend.click_policy="hide"
    return inner_page, model_lines


def predicted_price_data(target_brand):
    projected_price_df = pd.read_csv(
        "data_cleaning/Projected_Price_data.csv")

    projected_price_data = projected_price_df[projected_price_df['Maker']
                                              == target_brand]
    projected_price_data = projected_price_data.head(10)
    return projected_price_data


def predicted_price_graph_setup(brand_name):
    model_lines = []
    # extract the data
    sales_data = predicted_price_data(brand_name)
    years = np.arange(2022, 2027)

    data = pd.DataFrame({'Year': years})
    for model in sales_data['Genmodel']:
        # print(model[6:])
        model_row = sales_data.loc[sales_data['Genmodel'] == model]
        # Assuming the sales data starts from the 3rd column to the second last column
        sales_values = model_row.iloc[0, 2:-1].values
        data[model] = sales_values

    source = ColumnDataSource(data)

    inner_page = figure(title=brand_name + "'s Model Price Performance Trackers", x_axis_label='Year',
                        y_axis_label='Price (in Pound)', width=500, height=400)

    colors = Category20[len(sales_data['Genmodel'])]

    # current version (without legend)
    for model, color in zip(sales_data['Genmodel'], colors):
        line = inner_page.line(x='Year', y=model, line_width=4,
                               color=color, source=source)
        model_lines.append(line)

    for i in range(len(model_lines)):
        if (i > 0):
            model_lines[i].visible = False

    # inner_page.add_layout(line)
    inner_page.yaxis.formatter = NumeralTickFormatter(format="0,0")
    inner_page.title.text_font_size = '12pt'
    # inner_page.legend.location = "top_left"
    # inner_page.legend.orientation = "horizontal"
    # inner_page.legend.click_policy="hide"
    return inner_page, model_lines
