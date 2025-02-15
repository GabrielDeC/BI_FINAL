## Código que Carregou as bases utilizado no VISUAL STUDIO

import os
import glob
import pandas as pd
import mysql.connector

# Defina o caminho para a pasta queclea contém os arquivos CSV
folder_path = 'Dados_Tratados/'  # Altere para o caminho desejado

# Configuração da conexão com o MySQL
conn = mysql.connector.connect(
    host='127.0.0.1',       # ou o host apropriado
    user='root',     # substitua pelo seu usuário MySQL
    password='Str0ngP@ssw0rd!',   # substitua pela sua senha MySQL
    database='dw_covid'    # substitua pelo nome do seu banco de dados
)

cursor = conn.cursor()

# Busca por todos os arquivos CSV na pasta
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

def sanitize_column_name(col):
    """Remove caracteres inválidos e substitui espaços por underline nos nomes das colunas."""
    return col.strip().replace(" ", "_").replace(":", "")

for csv_file in csv_files:
    # Extrai o nome do arquivo (sem a extensão) para usar como nome da tabela
    table_name = os.path.splitext(os.path.basename(csv_file))[0]
    print(f"Processando arquivo: {csv_file} -> Tabela: {table_name}")

    # Lê o arquivo CSV em um DataFrame utilizando pandas
    df = pd.read_csv(csv_file)

    # Ajusta os nomes das colunas para evitar erros no MySQL
    columns = [sanitize_column_name(col) for col in df.columns]
    df.columns = columns  # Atualiza os nomes das colunas no DataFrame

    # Opcional: Remove a tabela se ela já existir para recriá-la
    cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`;")

    # Cria a tabela com os nomes das colunas do CSV, definindo todas como TEXT.
    columns_sql = ', '.join([f"`{col}` TEXT" for col in columns])
    create_table_query = f"CREATE TABLE `{table_name}` ({columns_sql});"
    cursor.execute(create_table_query)

    # Prepara a query de inserção utilizando placeholders (%s) para cada coluna
    placeholders = ', '.join(['%s'] * len(columns))
    columns_formatted = ', '.join([f"`{col}`" for col in columns])
    insert_query = f"INSERT INTO `{table_name}` ({columns_formatted}) VALUES ({placeholders});"

    # Converte os dados do DataFrame para uma lista de listas
    data = df.values.tolist()

    # Insere os dados na tabela (executemany para inserir todas as linhas)
    if data:  # Verifica se há dados para inserir
        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"Tabela '{table_name}' criada e populada com sucesso!")
    else:
        print(f"O arquivo {csv_file} está vazio ou não possui dados válidos para inserção.")

# Fecha a conexão com o banco de dados
cursor.close()
conn.close()