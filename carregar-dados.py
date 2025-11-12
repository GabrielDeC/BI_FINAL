import os
import glob
import pandas as pd
import mysql.connector

folder_path = 'Dados_Tratados/'

conn = mysql.connector.connect(
    host='',
    user='',
    password='',
    database=''
)

cursor = conn.cursor()

csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

def sanitize_column_name(col):
    return col.strip().replace(" ", "_").replace(":", "")

for csv_file in csv_files:    
    table_name = os.path.splitext(os.path.basename(csv_file))[0]
    print(f"Processando arquivo: {csv_file} -> Tabela: {table_name}")

    df = pd.read_csv(csv_file)

    columns = [sanitize_column_name(col) for col in df.columns]
    df.columns = columns

    cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`;")

    columns_sql = ', '.join([f"`{col}` TEXT" for col in columns])
    create_table_query = f"CREATE TABLE `{table_name}` ({columns_sql});"
    cursor.execute(create_table_query)

    placeholders = ', '.join(['%s'] * len(columns))
    columns_formatted = ', '.join([f"`{col}`" for col in columns])
    insert_query = f"INSERT INTO `{table_name}` ({columns_formatted}) VALUES ({placeholders});"

    data = df.values.tolist()

    if data:
        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"Tabela '{table_name}' criada e populada com sucesso!")
    else:
        print(f"O arquivo {csv_file} está vazio ou não possui dados válidos para inserção.")

cursor.close()
conn.close()