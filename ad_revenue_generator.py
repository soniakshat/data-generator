import pandas as pd
import numpy as np

def generate_ad_revenue_daily(start_date, end_date):
    # Generate random revenue data
    dates = pd.date_range(start_date, end_date, freq='D')
    revenue = np.random.randint(10, 100, size=len(dates))

    # Create a DataFrame
    df = pd.DataFrame({'Date': dates, 'Revenue': revenue})

    return df


def resample_and_display(df, freq):
    if freq == 'D':
        print("\nDaily Ad Revenue Data:")
        print(df)
    elif freq == 'W':
        df_resampled = df.resample('W', on='Date').sum()
        print("\nWeekly Ad Revenue Data:")
        print(df_resampled)
    elif freq == 'M':
        df_resampled = df.resample('MS', on='Date').sum()
        print("\nMonthly Ad Revenue Data:")
        print(df_resampled)
    elif freq == 'Q':
        df_resampled = df.resample('QS', on='Date').sum()
        print("\nQuarterly Ad Revenue Data:")
        print(df_resampled)
    elif freq == 'A':
        df_resampled = df.resample('YS', on='Date').sum()
        print("\nAnnual Ad Revenue Data:")
        print(df_resampled)
    else:
        raise ValueError("Invalid frequency value. Supported values are 'D', 'W', 'M', 'Q', and 'A'.")


# Example usage
start_date = '2022-01-01'
end_date = '2024-01-01'

# Generate daily ad revenue data
df_daily = generate_ad_revenue_daily(start_date, end_date)
df_daily.to_csv("ad_revenue_data.csv", index=False)
# df_daily.resample('MS', on='Date').sum().to_csv("ad_revenue_data.csv")



# # Display the data as daily
# resample_and_display(df_daily, 'D')
#
# # Display the data as weekly
# resample_and_display(df_daily, 'W')
#
# # Display the data as monthly
# resample_and_display(df_daily, 'M')
#
# # Display the data as quarterly
# resample_and_display(df_daily, 'Q')
#
# # Display the data as annually
# resample_and_display(df_daily, 'A')