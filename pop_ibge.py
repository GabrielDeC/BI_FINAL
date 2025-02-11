import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def coletar_tabela():
    url = "https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Brasil_por_popula%C3%A7%C3%A3o_(2022)"

    # Configura as opções do Chrome
    options = ChromeOptions()
    # Descomente a linha abaixo para executar o navegador em modo headless (sem interface gráfica)
    # options.add_argument("--headless")

    # Inicializa o driver do Chrome utilizando o ChromeDriverManager
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )

    try:
        # Acessa a URL
        driver.get(url)
        # Aguarda alguns segundos para que a página seja carregada
        time.sleep(5)

        # Localiza a tabela utilizando o seletor CSS para as classes especificadas
        tabela_elemento = driver.find_element(By.CSS_SELECTOR, "table.wikitable.sortable.jquery-tablesorter")

        # Extrai o HTML da tabela
        tabela_html = tabela_elemento.get_attribute("outerHTML")

        # Utiliza o pandas para ler a tabela a partir do HTML extraído
        dfs = pd.read_html(tabela_html)
        if dfs:
            df = dfs[0]  # Caso haja mais de uma tabela, seleciona a desejada (a primeira, neste caso)
            # Salva o DataFrame em um arquivo CSV
            df.to_csv("tabela_concentracoes.csv", index=False, encoding="utf-8-sig")
            print("Tabela salva com sucesso no arquivo 'tabela_concentracoes.csv'")
        else:
            print("Nenhuma tabela encontrada no HTML extraído.")
    
    except Exception as e:
        print("Erro durante a coleta da tabela:", e)
    
    finally:
        # Encerra o navegador
        driver.quit()

if __name__ == "__main__":
    coletar_tabela()
