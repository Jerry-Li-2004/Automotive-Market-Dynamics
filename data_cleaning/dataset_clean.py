import pandas as pd

# Load the datasets
sales_df = pd.read_csv('dataset/Sales_table.csv')
price_df = pd.read_csv('dataset/Price_table.csv')
ad_df = pd.read_csv('dataset/Ad_table (extra).csv')


def standardize_names(df, maker_col, genmodel_col):
    df[maker_col] = df[maker_col].str.title().str.replace(
        '-', ' ').str.replace('_', ' ')
    df[maker_col] = df[maker_col].replace(
        'Mercedes Benz', 'Mercedes')  # special case
    return df


# Standardize names in all datasets
sales_df = standardize_names(sales_df, 'Maker', 'Genmodel')
price_df = standardize_names(price_df, 'Maker', 'Genmodel')
ad_df = standardize_names(ad_df, 'Maker', 'Genmodel')

# Save the cleaned datasets
sales_df.to_csv('data_cleaning/Sales_table.csv', index=False)
price_df.to_csv('data_cleaning/Price_table.csv', index=False)
ad_df.to_csv('data_cleaning/Ad_table.csv', index=False)
