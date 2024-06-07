import os
import uuid
import random
import pandas as pd
import getindianname
import datetime as dt

start_date = dt.datetime(2018, 5, 17)
end_date = dt.datetime(2020, 5, 25)

number_of_data_to_generate = 10000

user_login_csv = "login_data.csv"
user_purchase_csv = "purchase_data.csv"


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    else:
        print(f"File '{file_path}' not found.")


should_delete_first = False
if should_delete_first:
    delete_file(user_login_csv)
    delete_file(user_purchase_csv)


def save_df_as_csv(dataframe, filename, index=False, header=True):
    dataframe.to_csv(filename, index=index, header=header)


def read_csv_to_df(file_path, **kwargs):
    """
    Reads a CSV file into a Pandas DataFrame.

    Parameters:
        file_path (str): The path to the CSV file.
        **kwargs: Additional keyword arguments to pass to pd.read_csv().

    Returns:
        pd.DataFrame: The resulting DataFrame.
    """
    try:
        df = pd.read_csv(file_path, **kwargs)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None


def generate_uuid(seed):
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, f"{"www.spellenx.com"}-{seed}"))


def generate_random_datetime():
    date_range = end_date - start_date
    random_days = random.randint(0, date_range.days)
    random_date = start_date + dt.timedelta(days=random_days)
    return random_date.timestamp()


def generate_end_datetime(start_datetime):
    time_change = dt.timedelta(minutes=random.randint(15, 75), seconds=random.randint(0, 60)).total_seconds()
    end_datetime = start_datetime + time_change
    return end_datetime


def generate_login_data(num_entries):
    df = pd.DataFrame(
        columns=['user_id', 'user_name', 'game_id', 'login_datetime', 'logout_datetime', 'session_duration'])

    def add_entry(uid, name, gid, login_datetime, logout_datetime, session_time):
        new_entry = pd.DataFrame({
            'user_id': [uid],
            'user_name': [name],
            'game_id': [gid],
            'login_datetime': [login_datetime],
            'logout_datetime': [logout_datetime],
            'session_duration': [session_time]
        })
        df.loc[len(df)] = new_entry.values[0]
        return df

    for i in range(1, num_entries):
        user_id = generate_uuid(i)
        user_name = getindianname.randname()
        game_id = random.randint(1, 5)

        st_dt = dt.datetime.fromtimestamp(generate_random_datetime())
        en_dt = dt.datetime.fromtimestamp(generate_end_datetime(dt.datetime.timestamp(st_dt)))

        diff = en_dt - st_dt
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        session_duration = dt.time(hour=hours, minute=minutes, second=seconds)

        add_entry(user_id, user_name, game_id, st_dt, en_dt, session_duration)

    df.drop_duplicates()
    df.drop_duplicates(subset=['user_id'], keep="first")

    return df

##################################################################################


print("Getting login data...")
user_login_data = read_csv_to_df(user_login_csv)

if user_login_data is None:
    print("CSV not found! Creating new data")
    user_login_data = generate_login_data(number_of_data_to_generate)
    save_df_as_csv(user_login_data, user_login_csv)

print(user_login_data.head())
print(user_login_data.size)
###################################################################################


class Product:
    def __init__(self, id, name, type, price):
        self.id = id
        self.name = name
        self.type = type
        self.price = price

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_price(self):
        return self.price
    #
    # def __repr__(self):
    #     return f"Product(id={self.id}, name={self.name}, type={self.type}, price={self.price})"


class ProductRepository:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def get_product_by_id(self, id):
        for product in self.products:
            if product.id == id:
                return product
        return None


# Create some products
product1 = Product(1, "Coin-1", "Consumable", 49.99)
product2 = Product(2, "Coin-2", "Consumable", 99.99)
product3 = Product(3, "Coin-3", "Consumable", 149.99)
product4 = Product(4, "Gem-1", "Consumable", 49.99)
product5 = Product(5, "Gem-2", "Consumable", 99.99)
product6 = Product(6, "Gem-3", "Consumable", 149.99)
product7 = Product(7, "Ad_Free", "One-Time", 99.99)


# Create a product repository
repository = ProductRepository()

# Add products to the repository
repository.add_product(product1)
repository.add_product(product2)
repository.add_product(product3)
repository.add_product(product4)
repository.add_product(product5)
repository.add_product(product6)
repository.add_product(product7)

trx_ids = []

multiplier = random.randint(5, 10)


def generate_transaction_id(prefix="TXN-"):
    random_number = str(random.randint(5000, number_of_data_to_generate * multiplier * 2))
    tnx = prefix + random_number
    if tnx in trx_ids:
        generate_transaction_id()
    else:
        trx_ids.append(tnx)
        return tnx


def generate_purchase_data(num_entries):
    df = pd.DataFrame(columns=['user_id', 'trx_id', 'purchase_timestamp', 'product_id', 'product_name', 'product_type', 'product_price'])

    def add_entry(uid, tnx_id, purchase_stamp, pro_id, pro_name, pro_type, pro_price):
        new_entry = pd.DataFrame({
            'user_id': [uid],
            'trx_id': [tnx_id],
            'purchase_timestamp': [purchase_stamp],
            'product_id': [pro_id],
            'product_name': [pro_name],
            'product_type': [pro_type],
            'product_price': [pro_price]
        })
        df.loc[len(df)] = new_entry.values[0]
        return df

    for i in range(1, num_entries):
        sample = user_login_data.sample(frac=0.25)
        user_uuid = sample['user_id'].tolist()
        uuid = random.choice(user_uuid)
        tnx_id = generate_transaction_id()
        purchase_stamp = dt.datetime.fromtimestamp(generate_random_datetime())
        ran_num = random.randint(1,7)
        pro = repository.get_product_by_id(ran_num)
        add_entry(uuid, tnx_id, purchase_stamp, pro.get_id(), pro.get_name(), pro.get_type(), pro.get_price())

    # Identify the rows where product_id is 7
    product_7_df = df[df['product_id'] == 7]

    # Find the user_ids that are repeating in this subset
    repeating_user_ids = product_7_df['user_id'].value_counts()
    repeating_user_ids = repeating_user_ids[repeating_user_ids > 1].index

    # Remove these repeating user_id rows from the original dataframe
    df = df[~((df['product_id'] == 7) & (df['user_id'].isin(repeating_user_ids)))]

    return df


user_purchase_data = read_csv_to_df(user_purchase_csv)

print("Getting Purchase data...")
if user_purchase_data is None:
    print("CSV not found! Creating new data...")
    user_purchase_data = generate_purchase_data(number_of_data_to_generate * multiplier)
    save_df_as_csv(user_purchase_data, user_purchase_csv)

print(user_purchase_data.head())
print(user_purchase_data.size)

print("purchase data where ad free was purchased")

ext_data = user_purchase_data.loc[user_purchase_data['product_id'] == 7]
print(ext_data)


print("Total unique users", user_login_data['user_id'].nunique())
print("Unique User who purchased", user_purchase_data['user_id'].nunique())

product_names = []
earned = []

for i in range(1, 8):
    pro = repository.get_product_by_id(i)
    sum_product_price = user_purchase_data.loc[user_purchase_data['product_id'] == pro.get_id(), 'product_price'].sum()
    product_names.append(pro.get_name())
    earned.append(sum_product_price)
    print(f"Earned from {pro.get_name()} Purchase", sum_product_price)



import matplotlib.pyplot as plt
fig = plt.figure(figsize=(10, 5))

# creating the bar plot
plt.bar(product_names, earned, color='blue',
        width=0.4)

plt.xlabel("Products")
plt.ylabel("Amount Earned in INR")
plt.title("Earned per product in INR")
plt.show()

# # Convert purchase_timestamp to datetime
# df['purchase_timestamp'] = pd.to_datetime(df['purchase_timestamp'], unit='s')
#
# # Define the date range
# start_date = 'YYYY-MM-DD'  # Replace with your start date
# end_date = 'YYYY-MM-DD'    # Replace with your end date
#
# # Filter the DataFrame for the date range and product_id == 7
# filtered_df = df[(df['purchase_timestamp'] >= start_date) &
#                  (df['purchase_timestamp'] <= end_date) &
#                  (df['product_id'] == 7)]
#
# # Get the count of product_id == 7 within the date range
# product_7_count = filtered_df.shape[0]
#
# # Calculate the sum and average of purchase_price for product_id == 7 within the date range
# product_7_sum = filtered_df['purchase_price'].sum()
# product_7_avg = filtered_df['purchase_price'].mean()
#
# # Print the results
# print(f"Number of product_id == 7 within the date range: {product_7_count}")
# print(f"Sum of purchase_price for product_id == 7 within the date range: {product_7_sum}")
# print(f"Average of purchase_price for product_id == 7 within the date range: {product_7_avg}")