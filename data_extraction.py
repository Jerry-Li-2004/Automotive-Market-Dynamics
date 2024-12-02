import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, NumeralTickFormatter, TapTool
from bokeh.plotting import figure

from bokeh.palettes import Category20

global_lines = []

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
    global global_lines
    # extract the data
    sales_data = get_all_sales_data()
    years = np.arange(2001, 2021)

    data = pd.DataFrame({'Year': years})
    for brand in sales_data['Top_10_Brands']:
        data[brand] = sales_data[brand]

    source = ColumnDataSource(data)

    main_page = figure(title="Automotive Market Dynamics Visualization", x_axis_label='Year',
                       y_axis_label='Sales', sizing_mode='stretch_both', width=800, height=400)

    colors = Category20[len(sales_data['Top_10_Brands'])]
    main_page.varea_stack(stackers=sales_data['Top_10_Brands'],
                          x='Year', color=colors, source=source, legend_label=sales_data['Top_10_Brands'])

    main_page.yaxis.formatter = NumeralTickFormatter(format="0,0")
    main_page.title.text_font_size = '20pt'
    main_page.legend.location = "top_left"
    main_page.legend.orientation = "horizontal"
    # main_page.legend.click_policy="hide"

    return main_page


def filter_line_page_setup():
    global global_lines
    # extract the data
    sales_data = get_all_sales_data()
    years = np.arange(2001, 2021)

    data = pd.DataFrame({'Year': years})
    for brand in sales_data['Top_10_Brands']:
        data[brand] = sales_data[brand]

    source = ColumnDataSource(data)

    main_page = figure(title="Automotive Market Dynamics Visualization", x_axis_label='Year',
                       y_axis_label='Sales', sizing_mode='stretch_both', width=800, height=400)

    colors = Category20[len(sales_data['Top_10_Brands'])]

    for brand, color in zip(sales_data['Top_10_Brands'], colors):
        line = main_page.line(x='Year', y=brand, line_width = 4, color=color, source=source, legend_label=brand)
        global_lines.append(line)


    main_page.yaxis.formatter = NumeralTickFormatter(format="0,0")
    main_page.title.text_font_size = '20pt'
    main_page.legend.location = "top_left"
    main_page.legend.orientation = "horizontal"
    # main_page.legend.click_policy="hide"

    return main_page