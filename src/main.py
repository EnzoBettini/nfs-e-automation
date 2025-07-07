import pandas as pd

df = pd.read_csv('../data/input/conf.csv', sep = None, engine='python')

colunas_para_excluir = ['MAQ BAN.', 'MAQ CL.', 'SERVIÇO', 'DATA', 'CLIENTE', 'ANIMAL', 'FORMA PGTO'];
df = df.drop(columns=colunas_para_excluir);
df = df.dropna()

colunas = list(df.columns)
colunas[0] = 'ID'
df.columns = colunas
df['ID'] = df['ID'].astype(int)

display(df)
df.to_csv('../data/input/filtered/filtered_df.csv', index=False)

import re
import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configurações iniciais ---

# Carrega variáveis do arquivo .env
dotenv_path = "../data/secure/.env"
load_dotenv(dotenv_path)
EMAIL = os.getenv("EMAIL")
SENHA = os.getenv("SENHA")

# Caminho do chromedriver
chromedriver_path = r"C:\Users\User\Desktop\Repositorios\Automações\src\others\chromedriver.exe"

# Configurações do navegador Chrome
options = Options()
options.add_argument("--start-maximized")
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

# --- Login e navegação até Consulta Vendas ---

driver.get("https://app.simples.vet/login/login.php")
time.sleep(2)

driver.find_element(By.ID, "l_usu_var_email").send_keys(EMAIL)
driver.find_element(By.ID, "l_usu_var_senha").send_keys(SENHA)
driver.find_element(By.ID, "l_usu_var_senha").send_keys(Keys.RETURN)

# Espera o menu "Vendas" carregar e clica
WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//a[.//span[text()='Vendas ']]"))
).click()

# Clica em "Consulta vendas"
WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@class='link-menu' and contains(text(), 'Consulta vendas')]"))
).click()

time.sleep(2)

# --- Carrega DataFrame original e faz busca por ID na consulta vendas ---

df = pd.read_csv("../data/input/filtered/filtered_df.csv")

for index, row in df.iterrows():
    id_value = str(row['ID'])

    input_id = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "p__ven_var_chave"))
    )
    input_id.clear()
    input_id.send_keys(id_value)
    input_id.send_keys(Keys.RETURN)
    time.sleep(2)

    try:
        ficha_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ficha"))
        )
        ficha_text = ficha_element.text  # exemplo: "(16603)"
        cliente_num = re.search(r"\((\d+)\)", ficha_text).group(1)
    except Exception as e:
        print(f"Erro ao capturar ficha para ID {id_value}: {e}")
        cliente_num = None

    df.loc[index, 'cliente'] = cliente_num

# Agrupa e soma valores por cliente
df['VALOR'] = df['VALOR'].str.replace(',', '.').astype(float)
df_resumo = df.groupby('cliente', as_index=False)['VALOR'].sum()
df_resumo = df_resumo.sort_values(by='cliente')
df_resumo['CPF'] = ""  # coluna para CPF

# --- Navega para o menu Clientes ---

# Clica no menu "Clientes" usando o seletor do botão confiável
clientes_btn = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.link-menu[data-id='118']"))
)
clientes_btn.click()
time.sleep(2)

# --- Loop para buscar CPF para cada cliente ---

for index, row in df_resumo.iterrows():
    cliente_id = str(row['cliente'])
    print(f"Processando cliente {cliente_id} (linha {index})...")

    try:
        # Preenche campo de busca por cliente
        input_nome = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "p__pes_var_nome"))
        )
        input_nome.clear()
        input_nome.send_keys(cliente_id)
        input_nome.send_keys(Keys.RETURN)
        print("Pesquisa enviada.")
        time.sleep(3)

        # Clica no primeiro resultado da lista
        elemento = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//tbody[@id='bodyLoad']//a[contains(@class, 'linkAnimalLista')]"))
        )
        elemento.click()
        print("Cliente clicado.")
        time.sleep(3)

        # Clica no span para abrir edição do responsável (CPF)
        div_responsavel = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "divDadosProprietario"))
        )
        div_responsavel.click()
        print("Seção de responsável aberta.")
        time.sleep(2)

        # Busca o input do CPF e pega o valor
        try:
            cpf_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "pes_var_cpf"))
            )
            cpf_value = cpf_input.get_attribute("value").strip()
            if not cpf_value:
                cpf_value = "000.000.000-00"
        except Exception as e:
            print(f"Erro ao buscar CPF do cliente {cliente_id}: {e}")
            cpf_value = "000.000.000-00"

        df_resumo.loc[index, 'CPF'] = cpf_value
        print(f"CPF obtido: {cpf_value}")

        # Fecha a tela do cliente
        fechar_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "v__btn_fechar_topo"))
        )
        fechar_btn.click()
        print("Tela fechada.")
        time.sleep(2)

        # Tenta clicar no menu "Clientes" com retry para garantir clique
        for attempt in range(3):
            try:
                clientes_btn = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.link-menu[data-id='118']"))
                )
                clientes_btn.click()
                print("Voltando para menu Clientes.")
                time.sleep(2)
                break  # saiu do loop se clicou com sucesso
            except Exception as e:
                print(f"Tentativa {attempt + 1} para clicar no menu Clientes falhou: {e}")
                time.sleep(2)
        else:
            print("Não conseguiu clicar no menu Clientes após 3 tentativas.")

    except Exception as e:
        print(f"Erro ao processar cliente {cliente_id}: {repr(e)}")
        df_resumo.loc[index, 'CPF'] = "000.000.000-00"

print("\nResultado final:")
print(df_resumo)

# Opcional: salvar resultado em CSV
df_resumo.to_csv("../data/output/clientes_com_cpf.csv", index=False)




# --- Configurações iniciais ---

dotenv_path = "../data/secure/.env"
load_dotenv(dotenv_path)
EMAIL = os.getenv("LOGIN")
SENHA = os.getenv("SENHA_ISSE")

chromedriver_path = r"C:\Users\User\Desktop\Repositorios\Automações\src\others\chromedriver.exe"

options = Options()
options.add_argument("--start-maximized")
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

# --- Login ---

driver.get("https://auth.maringa.ecity.com.br/v2/sign_in?return_to=https%3A%2F%2Fauth.maringa.ecity.com.br%2Fv2%2Foauth2%2Fauthorize%3Fresponse_type%3Dcode%26client_id%3Dba1c97e995f70%26redirect_uri%3Dhttps%253A%252F%252Fmaringa.fintel.com.br%252FAccount%252FSenhaWeb%26scope%3D%26state%3DNfs")

WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "login"))).send_keys(EMAIL)
driver.find_element(By.ID, "password").send_keys(SENHA)
driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
time.sleep(3)
driver.get("https://maringa.fintel.com.br/ConsultaNotasFiscaisEmitidas")
time.sleep(3)

# --- Lê os dados da planilha ---
df = pd.read_csv("../data/output/clientes_com_cpf.csv")

# DataFrames para guardar resultados
df_sem_cpf = pd.DataFrame(columns=df.columns)
df_notas_lancadas = pd.DataFrame(columns=df.columns)

for index, row in df.iterrows():

    cpf = row['CPF']
    valor = float(row['VALOR'])
    imposto = round(valor * 0.1772, 2)

    if cpf == "000.000.000-00":
        print(f"CPF inválido encontrado, pulando: {cpf} (linha {index})")
        df_sem_cpf = pd.concat([df_sem_cpf, pd.DataFrame([row])], ignore_index=True)
        continue

    print(f"Processando CPF: {cpf} | Valor: {valor} | Imposto: R${imposto:.2f}")

    btn_emitir = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/Emissor/Nfse' and contains(@class, 'btn-primary')]"))
    )
    btn_emitir.click()

    # time.sleep(1)  # para visualizar passo a passo

    input_cpf = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "Tomador_CnpjCpf"))
    )
    input_cpf.clear()
    input_cpf.send_keys(cpf)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnBuscarTomador"))
    ).click()
    time.sleep(1.5)  # necessário aguardar o preenchimento

    cep = driver.find_element(By.ID, "tomador_Cep").get_attribute("value")
    logradouro = driver.find_element(By.ID, "tomador_Logradouro").get_attribute("value")
    numero = driver.find_element(By.ID, "tomador_Numero").get_attribute("value")

    if not cep or not logradouro or not numero:
        if not cep:
            driver.find_element(By.ID, "tomador_Cep").clear()
            driver.find_element(By.ID, "tomador_Cep").send_keys("87013-060")
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@onclick, 'Emissor_BuscarCep')]"))
            ).click()
            time.sleep(1)

        if not numero:
            driver.find_element(By.ID, "tomador_Numero").clear()
            driver.find_element(By.ID, "tomador_Numero").send_keys("123")
            time.sleep(0.5)
    servico_select = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "IdServico"))
    )
    for option in servico_select.find_elements(By.TAG_NAME, 'option'):
        if "050802" in option.text:
            option.click()
            break
    descricao = f"Prestação de serviços. Informação aproximada de tributação R${imposto:.2f} (17.72%) conforme lei 12.741/2012 fonte IBPT."
    descricao_input = driver.find_element(By.ID, "Descricao")
    descricao_input.clear()
    descricao_input.send_keys(descricao)
    valor_input = driver.find_element(By.ID, "VlrUnitario")
    valor_input.clear()
    valor_input.send_keys(f"{valor:.2f}".replace('.', ','))

    # Em vez de clicar em confirmar, clicamos em Voltar para teste
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Voltar')]"))
    ).click()

    print(f"Feito teste para CPF {cpf} - clicou em Voltar ao invés de confirmar.")

    # Guarda os dados processados com sucesso
    df_notas_lancadas = pd.concat([df_notas_lancadas, pd.DataFrame([row])], ignore_index=True)

    time.sleep(3)  # comente esse sleep depois para acelerar

# Salva arquivos de saída
df_sem_cpf.to_csv("../data/output/sem_cpf.csv", index=False)
df_notas_lancadas.to_csv("../data/output/notas_lancadas.csv", index=False)

print("✅ Teste finalizado. Arquivos 'sem_cpf.csv' e 'notas_lancadas.csv' gerados.")

