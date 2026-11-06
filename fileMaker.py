import pandas as pd

df = pd.read_csv('\\Users\\henok\\OneDrive\\Desktop\\Data_engineering\\staging_area\\sourceFile\\customers.csv')
df1 = pd.read_csv('\\Users\\henok\\OneDrive\\Desktop\\Data_engineering\\staging_area\\sourceFile\\producttype.csv')
df6 = pd.read_csv('\\Users\\henok\\OneDrive\\Desktop\\Data_engineering\\staging_area\\payment_File_raw.csv')
df9 = pd.read_csv('\\Users\\henok\\OneDrive\\Desktop\\Data_engineering\\staging_area\\sale_file_raw.csv')
df_inventoryFile = pd.read_csv('\\Users\\henok\\OneDrive\\Desktop\\Data_engineering\\staging_area\\inventory_raw_file.csv')
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
    state.append(df['state'].iloc[i-1])
    customer_type.append(df1['Customer type'].iloc[i-1])
    city.append(df['city'].iloc[i-1])
values = list(zip(Custometorid, first_name, last_name, email, segement, customer_type, state, city))
df2 = pd.DataFrame(values, columns = ['custometorid', 'first_name', 'last_name', 'email', 'segment', 'customer_type', 'state', 'city'])
df2['email'] = pd.concat([df2['email'].iloc[:4], df2['email'].iloc[6:100], df2['email'].iloc[103:206], df2['email'].iloc[208:]])
df2['email'] = df2['email'].fillna("NONE")


df3 = pd.read_csv("\\Users\\henok\\OneDrive\\Desktop\\Data_engineering\\staging_area\\sourceFile\\producttype.csv")
df4 = pd.read_csv('customer_file.csv')
list_inside= []
list_outside = []
    
for i in range (1, len(df3) + 1):
    list_inside.append('P' + str(i))
    list_inside.append(df3['Product line'].iloc[i-1])
    list_inside.append("S" + str(i))
    list_inside.append(df4['custometorid'].sample(n=1).iloc[0])
    list_outside.append(list_inside)
    list_inside = []
df5 = pd.DataFrame(list_outside, columns=['productid', 'product_type', 'saleid', 'customerid'])


# Fill optional columns
df_inventoryFile['product_description'] = df_inventoryFile['product_description'].fillna("N/A")
df_inventoryFile['color'] = df_inventoryFile['color'].fillna("N/A")
missing_mask = df_inventoryFile.isna().any(axis=1)
df_log_file_inventory = df_inventoryFile.loc[missing_mask].copy()
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
df_update_file_inventory = df_inventoryFile.loc[~missing_mask].copy()
df_update_file_inventory.to_csv('\\Users\\henok\\OneDrive\\Desktop\\Data_engineering\\staging_area\\inventory_cleaned_file.csv', index=False)
df_log_file_inventory.to_csv('\\Users\\henok\\OneDrive\\Desktop\\Data_engineering\\staging_area\\inventory_log_file.csv',index=False)