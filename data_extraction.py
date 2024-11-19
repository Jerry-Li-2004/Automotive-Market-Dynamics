import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource , NumeralTickFormatter
from bokeh.plotting import figure

from bokeh.palettes import Category20


def get_sales_data():
    
    sales_df = pd.read_csv("dataset/Sales_table.csv")
    sales_data_df = sales_df.drop(columns=['Maker','Genmodel', 'Genmodel_ID'])

    volvo_sales = sales_data_df[sales_df['Maker'] =='VOLVO']
    toyota_sales = sales_data_df[sales_df['Maker'] =='TOYOTA']
    nissan_sales = sales_data_df[sales_df['Maker'] =='NISSAN']
    volkswagen_sales = sales_data_df[sales_df['Maker'] =='VOLKSWAGEN']

    total_volvo_sales = volvo_sales.sum(axis=0).values
    total_toyota_sales = toyota_sales.sum(axis=0).values
    total_nissan_sales = nissan_sales.sum(axis=0).values
    total_volkswagen_sales = volkswagen_sales.sum(axis=0).values
    return total_volvo_sales, total_toyota_sales, total_nissan_sales, total_volkswagen_sales 

def main_page_setup():
    #extract the data
    total_volvo_sales, total_toyota_sales, total_nissan_sales, total_volkswagen_sales = get_sales_data()
    years = np.arange(2001, 2021)
    data = pd.DataFrame({'Year': years, 'VOLVO': total_volvo_sales,
                        'TOYOTA': total_toyota_sales, 'NISSAN': total_nissan_sales, 'VOLKSWAGEN': total_volkswagen_sales})

    source = ColumnDataSource(data)

    main_page = figure(title="Automotive Market Dynamics Visualization", x_axis_label='Year',
            y_axis_label='Sales', sizing_mode='stretch_both', width=800, height=400)

    colors = Category20[4]
    colors_label = ['Volvo', 'Toyota', 'Nissan', 'Volkswagen']
    main_page.varea_stack(stackers=['VOLVO', 'TOYOTA', 'NISSAN', 'VOLKSWAGEN'],
                x='Year', color=colors, source=source, legend_label=colors_label)
    

    main_page.yaxis.formatter = NumeralTickFormatter(format="0,0")
    main_page.title.text_font_size = '20pt'
    main_page.legend.location = "top_left"
    main_page.legend.orientation = "horizontal"

    return main_page
