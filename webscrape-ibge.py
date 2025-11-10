import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def coletar_tabela():
    url = "https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Brasil_por_popula%C3%A7%C3%A3o_(2022)"
    
    options = ChromeOptions()

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(url)
        time.sleep(5)

        tabela_elemento = driver.find_element(By.CSS_SELECTOR, "table.wikitable.sortable.jquery-tablesorter")

        tabela_html = tabela_elemento.get_attribute("outerHTML")

        dfs = pd.read_html(tabela_html)
        if dfs:
            df = dfs[0]
            caminho_dados_saida = "Dados_Tratados/tabela_concentracoes.csv"
            df.to_csv(caminho_dados_saida, index=False, encoding="utf-8-sig")
            print("Tabela salva com sucesso no arquivo 'tabela_concentracoes.csv'")
        else:
            print("Nenhuma tabela encontrada no HTML extraído.")
    
    except Exception as e:
        print("Erro durante a coleta da tabela:", e)
    
    finally:
        driver.quit()

if __name__ == "__main__":
    coletar_tabela()
