from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
import pandas as pd

# extract and transform file from a file named customers.csv
def customerFile(fileName, fileName2):
    df  = pd.read_csv(fileName)
    df0 = pd.read_csv(fileName2)
    df = df.drop(columns=['id'])
    Custometorid = []
    first_name = []
    last_name = []
    email = []
    segement = []
    customer_type = []
    state = []
    city = []
    for i in range(1,len(df)+1):
        Custometorid.append("C" + str(i))
        nameCell = df['name'].iloc[i-1].split()
        if(len(nameCell)>1):
            first_name.append(nameCell[0])
            last_name.append(nameCell[1])
        else:
            first_name.append(nameCell[0])
            last_name.append("")
        email.append(first_name[i-1].lower() + last_name[i-1].lower() + str(i) + "@gmail.com")
        nameCell = []
        segement.append(df['segment'].iloc[i-1])
        customer_type.append(df0['Customer type'].iloc[i-1])
        state.append(df['state'].iloc[i-1])
        city.append(df['city'].iloc[i-1])
    values = list(zip(Custometorid, first_name, last_name, email, segement, customer_type, state, city))
    df2 = pd.DataFrame(values, columns = ['custometorid', 'first_name', 'last_name', 'email','segment', 'customer_type', 'state', 'city'])
    df2 = df2.drop_duplicates(subset=['custometorid', 'first_name', 'last_name', 'segment', 'state', 'city']) # drop any columns that are duplicated
    df2['email'] = pd.concat([df2['email'].iloc[:4], df2['email'].iloc[6:100], df2['email'].iloc[103:206], df2['email'].iloc[208:]]) # I just created some empty cells in email column which I will handle the empty cell in the later of the code
    df2.to_csv('/home/project/staging_area/customer_file.csv', index = False)

# extract a producttype from a file named products.csv 
def productFile(fileName, fileName2):
    df0 = pd.read_csv(fileName2)
    df = pd.read_csv(fileName)
    list_inside= []
    list_outside = []
    
    for i in range (1, len(df) + 1):
        list_inside.append('P' + str(i))
        list_inside.append(df['Product line'].iloc[i-1])
        list_inside.append("S" + str(i))
        list_inside.append(df0['custometorid'].sample(n=1).iloc[0])
        list_outside.append(list_inside)
        list_inside = []
    df2  = pd.DataFrame(list_outside, columns=['productid', 'product_type', 'saleid', 'customerid'])
    df2 = df2.sort_values(by='productid')
    df2.to_csv('/home/project/staging_area/product_File.csv', index=False)

#extract and transform a sales from payment_infor.csv 
def saleFile(fileName, fileName2):
    df = pd.read_csv(fileName)
    df2 = pd.read_csv(fileName2)
    saleid = []
    invoice_id = []
    quantity_ordered = []
    unit_price = []
    Tax = []
    for i in range(0, len(df)):
        saleid.append(df2['saleid'].iloc[i])
        invoice_id.append(df['Invoice ID'].iloc[i])
        quantity_ordered.append(df['Quantity'].iloc[i])
        unit_price.append(df['Unit price'].iloc[i])
        Tax.append(df['Tax 5%'].iloc[i])
    values = list(zip(saleid, invoice_id, quantity_ordered, unit_price, Tax))
    df3 = pd.DataFrame(values, columns = ['saleid', 'invoiceid', 'quantity_ordered', 'unit_price', 'tax'])
    df3 = df3.sort_values(by = 'saleid')
    df3.to_csv('/home/project/staging_area/sale_File.csv', index=False)

def storeFile(fileName):
    df = pd.read_csv(fileName)
    storeid = []
    state = []
    city=[]
    street=[]
    zips=[]
    for i in range (1, len(df) +1):
        storeid.append('B' + str(i))
        state.append(df['state'].iloc[i-1])
        city.append(df['city'].iloc[i-1])
        street.append(df['street'].iloc[i-1])
        zips.append(df['zip'].iloc[i-1])
    values = list(zip(storeid, state, city, street, zips))
    df2 = pd.DataFrame(values, columns = ['storeid', 'state', 'city', 'street', 'zip'])
    df2 = df2.sort_values(by = 'storeid')
    df2.to_csv('/home/project/staging_area/store_File.csv', index=False)

#extract and transform a payment from payment_infor.csv 
# fileName = payment file   fileName2 = customer_file   fileName3 = product_file    fileName4 = store_file  fileName5 = sale_file
def paymentFile(fileName, fileName2, fileName3, fileName4, fileName5):
    df = pd.read_csv(fileName)
    df2 = pd.read_csv(fileName2)
    df3 = pd.read_csv(fileName3)
    df4 = pd.read_csv(fileName4)
    df5 = pd.read_csv(fileName5)
    paymentid = []
    customerid = []
    productid = []
    storeid = []
    saleid = []
    transaction_num = []
    transaction_date = []
    transaction_time = []
    is_fraud = []
    

    for i in range (1, len(df)+1):
        paymentid.append('D' + str(i))
        customerid.append(df2['custometorid'].sample(n=1).iloc[0])
        productid.append(df3['productid'].sample(n=1).iloc[0])
        storeid.append(df5['storeid'].sample(n=1).iloc[0])
        saleid.append(df4['saleid'].sample(n=1).iloc[0])
        transaction_num.append(df['trans_num'].iloc[i-1])
        transaction_date_time = df['trans_date_trans_time'].iloc[i-1].split()
        if (len(transaction_date_time) > 1):
            transaction_date.append(transaction_date_time[0])
            transaction_time.append(transaction_date_time[1])
        else:
            transaction_date.append("0\\0\\0")
            transaction_time.append("00:00:00 AM//PM")
        is_fraud.append(df['is_fraud'].iloc[i-1])

    values = list(zip(paymentid, customerid, productid, storeid, saleid, transaction_date, transaction_time, transaction_num, is_fraud))
    df6 = pd.DataFrame(values, columns=['paymentid', 'customerid', 'productid', 'storeid', 'saleid', 'transaction_date', 'transaction_time', 'transaction_num', 'is_fraud'])
    df6 = df6.sort_values(by = 'paymentid')
    df6.to_csv('/home/project/staging_area/payment_File.csv', index=False)

#extract and transform a payment from product.csv 
def inventoryFile(fileName, fileName2):
    df = pd.read_csv(fileName)
    df2 = pd.read_csv(fileName2)
    inventoryid = []
    productid = []
    product_description = []
    stock_quantity = []
    warranty_period = []
    product_dimensions = []
    manufacturing_date = []
    expiration_date = []
    sku = []
    product_tags = []
    color = []
    product_rating = []
    for i in range (1, len(df)+1):
        inventoryid.append("I" + str(i))
        productid.append(df2['productid'].sample(n=1).iloc[0])
        product_description.append(df['Product Description'].iloc[i-1])
        stock_quantity.append(df['Stock Quantity'].iloc[i-1])
        warranty_period.append(df['Warranty Period'].iloc[i-1])
        product_dimensions.append(df['Product Dimensions'].iloc[i-1])
        manufacturing_date.append(df['Manufacturing Date'].iloc[i-1])
        expiration_date.append(df['Expiration Date'].iloc[i-1])
        sku.append(df['SKU'].iloc[i-1])
        product_tags.append(df['Product Tags'].iloc[i-1])
        color.append(df['Color/Size Variations'].iloc[i-1])
        product_rating.append(df['Product Ratings'].iloc[i-1])
    values = list(zip(inventoryid, productid, product_description, stock_quantity, warranty_period, product_dimensions, manufacturing_date, expiration_date, sku, product_tags, color, product_rating))
    df3 = pd.DataFrame(values, columns = ['inventoryid', 'productid', 'product_description', 'stock_quantity', 'warranty_period', 'product_dimentions', 'manufacturing_date', 'expiration_date', 'sku', 'product_tags', 'color', 'product_rating'])
    df3 = df3.sort_values(by = 'inventoryid')
    df3.to_csv('/home/project/staging_area/inventory_File.csv', index = False)

def Handling_missing_values(fileName, fileName2, fileName3, fileName5, fileName6):

    #list of dataframes that needs to be handled
    df_customerFile = pd.read_csv(fileName)
    df_productFile = pd.read_csv(fileName2)
    df_salesFile = pd.read_csv(fileName3)
    df_paymentFile = pd.read_csv(fileName5)
    df_inventoryFile = pd.read_csv(fileName6)

    # Handling missing value for customer file  --> fill the empty columns using fillna library
    df_customerFile['email'] = df_customerFile['email'].fillna('N/A')
    df_customerFile['segment'] = df_customerFile['segment'].fillna('N/A')
    df_customerFile['customer_type']= df_customerFile['customer_type'].fillna("NEW")
    df_customerFile['first_name'] = df_customerFile['first_name'].fillna(df_customerFile['last_name'])
    df_customerFile['last_name'] = df_customerFile['last_name'].fillna(df_customerFile['first_name'])
    df_customerFile = df_customerFile.drop_duplicates(subset=['custometorid']) 
    df_customerFile.to_csv('/home/project/staging_area/cleaned_file/customer_cleaned.csv', index=False)


    # Handling missing value for product file  --> fill the empty columns using fillna library
    df_productFile['product_type'] = df_productFile['product_type'].fillna('New Product')
    df_productFile = df_productFile.drop_duplicates(subset=['productid'])
    df_productFile.to_csv('/home/project/staging_area/cleaned_file/product_cleaned.csv', index=False)


    # Hadling any missing values for payment File  --> drop the empty columns and write in log file for future investgation
    required_columns = [
        'paymentid', 'customerid', 'productid', 'storeid',
        'saleid', 'transaction_date', 'transaction_time',
        'transaction_num', 'is_fraud'
        ]
    # Convert empty strings and whitespace-only cells to missing values
    df_paymentFile = df_paymentFile.replace(r'^\s*$', pd.NA, regex=True)
    # Find rows containing missing values
    missing_mask_payment = df_paymentFile[required_columns].isna().any(axis=1)
    df_missing = df_paymentFile.loc[missing_mask_payment].copy()
    # Record why each row was rejected
    df_missing['rejection_reason'] = (
        df_missing[required_columns].isna()
        .apply(lambda row: ', '.join(row.index[row].tolist()), axis=1)
    )
    # Exclude rows with missing values
    df_valid = df_paymentFile.loc[~missing_mask_payment].copy()
    # Find duplicate payment IDs among remaining valid rows
    duplicate_mask = df_valid.duplicated(subset=['paymentid'], keep='first')
    df_duplicates = df_valid.loc[duplicate_mask].copy()
    df_duplicates['rejection_reason'] = 'Duplicate paymentid'
    # Keep only unique payment IDs
    df_payment_clean = df_valid.loc[~duplicate_mask].copy()
    # Combine rejected records into one log
    df_payment_log = pd.concat(
        [df_missing, df_duplicates],
        ignore_index=True
    )
    # Save both files
    df_payment_clean.to_csv('/home/project/staging_area/cleaned_file/payment_cleaned.csv', index=False)
    df_payment_log.to_csv('/home/project/staging_area/logs_cleaned_file/payment_data_quality_log.csv', index=False)


    # Hadling any missing values for sales File  --> drop the empty columns and write in log file for future investgation
    indexes_sales = []
    reasons_sales = []
    for i in range(len(df_salesFile)):
        missing_columns = df_salesFile.iloc[i].indexes_sales[df_salesFile.iloc[i].isna()]
        if len(missing_columns) > 0:
            indexes_sales.append(i)
            reasons_sales.append(
                ", ".join(col + " has no value" for col in missing_columns)
            )
    df_log_file= df_salesFile.iloc[indexes_sales].copy()
    df_log_file["rejection_reason"] = reasons_sales
    df_update_file = df_salesFile.dropna().copy()
    df_update_file.to_csv("/home/project/staging_area/cleaned_file/sale_cleaned.csv", index=False)
    df_log_file.to_csv("/home/project/staging_area/logs_cleaned_file/log_file_sale_file.csv", index=False)


    # Hadling any missing values for inventory File  --> drop the empty columns other than product description and color and write in log file for future investgation and fill the empty color and product description by "N/A"
    df_inventoryFile['product_description'] = df_inventoryFile['product_description'].fillna("N/A")
    df_inventoryFile['color'] = df_inventoryFile['color'].fillna("N/A")
    missing_mask_inventory = df_inventoryFile.isna().any(axis=1)
    df_log_file_inventory = df_inventoryFile.loc[missing_mask_inventory].copy()
    df_log_file_inventory['rejection_reason'] = (
        df_log_file_inventory.isna()
        .apply(
            lambda row: ", ".join(
                col + " has no value"
                for col in row.index[row]
            ),
            axis=1
        )
    )
    df_update_file_inventory = df_inventoryFile.loc[~missing_mask_inventory].copy()
    df_update_file_inventory.to_csv('/home/project/staging_area/cleaned_file/inventory_cleaned.csv', index=False)
    df_log_file_inventory.to_csv('/home/project/staging_area/logs_cleaned_file/log_file_inventory_file.csv',index=False)
        


# DAG arguments
default_args = {
    'owner': 'Airflow',
    'start_date': datetime.today(),
    'email':'henokeshetumerid@gmail.com', 
    'email_on_failure':True,
    'email_on_retry':True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# DAG default
dags = DAG(
    "Extract-Transform-Load-Apache-Airflow",
    description="Apache Airflow Final Assignment",
    default_args = default_args,
    schedule = timedelta(minutes=1)
)


# task explanation
task1 = PythonOperator(
    task1 = "Extract and transform customer.csv from customer and product files",
    python_callable = customerFile,
    op_args=["/home/theia/customers.csv", "/home/theia/producttype.csv"],
    dag=dags
)

task2 = PythonOperator(
    task1 = "Extract and transform product.csv from product files",
    python_callable = productFile,
    op_args=["/home/theia/producttype.csv", "/home/project/staging_area/customer_file.csv"],
    dag=dags
)

task3 = PythonOperator(
    task3 = "Extract and transform sales.csv from product and producttype files",
    python_callable=saleFile,
    op_args=["/home/theia/producttype.csv", '/home/project/staging_area/product_File.csv'],
    dag = dags
)

task4 = PythonOperator(
    task4 = "Extract and transform store.csv from payment_infor file",
    python_callable=storeFile,
    op_args=["/home/theia/payment_infor.csv"],
    dag = dags
)

task5 = PythonOperator(
    task5 = "Extract and transform payment.csv from payment_infor, customer_file, product_file, store_file, sale_file files",
    python_callable=paymentFile,
    op_args=["/home/theia/payment_infor.csv", "/home/project/staging_area/customer_file.csv", '/home/project/staging_area/product_File.csv', '/home/project/staging_area/sale_File.csv', '/home/project/staging_area/store_File.csv'],
    dag = dags
)

task6 = PythonOperator(
    task6 = "Extract and transform inventory.csv from products and product_File files",
    python_callable=inventoryFile,
    op_args=["/home/theia/products.csv", '/home/project/staging_area/product_File.csv'],
    dag = dags
)

task7 = PythonOperator(
    task7 = "Handling missing values for payment, inventory, customer, product, store and sales files",
    python_callable = Handling_missing_values,
    op_args=['/home/project/staging_area/customer_file.csv', '/home/project/staging_area/product_File.csv', '/home/project/staging_area/sale_File.csv', '/home/project/staging_area/payment_file.csv', '/home/project/staging_area/inventory_file.csv'],
    dag=dags
)


# building the pipeline 
task1 >> task2 >> task3 >> task4 >> task5 >> task6 >> task7