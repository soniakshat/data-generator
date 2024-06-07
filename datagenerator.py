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
user_uuid = user_login_data['user_id'].tolist()
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


def generate_transaction_id(prefix="TXN-"):
    random_number = str(random.randint(100000, 999999))
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
        uuid = random.choice(user_uuid)
        tnx_id = generate_transaction_id()
        purchase_stamp = generate_random_datetime()
        ran_num = random.randint(1,7)
        pro = repository.get_product_by_id(ran_num)
        add_entry(uuid, tnx_id, purchase_stamp, pro.get_id(), pro.get_name(), pro.get_type(), pro.get_price())

    return df


user_purchase_data = read_csv_to_df(user_purchase_csv)

print("Getting Purchase data...")
if user_purchase_data is None:
    print("CSV not found! Creating new data...")
    user_purchase_data = generate_purchase_data(number_of_data_to_generate * random.randint(5, 10))
    save_df_as_csv(user_purchase_data, user_purchase_csv)

# remove data where same user purchased ad free multiple times and keep only first such record


print(user_purchase_data.head())
print(user_purchase_data.size)


print("purchase data where ad free was purchased")

ext_data = user_purchase_data.loc[user_purchase_data['product_id'] == 7]
print(ext_data)
