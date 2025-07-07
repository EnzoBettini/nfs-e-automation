# Automação de Emissão de Notas Fiscais de Serviço (NFS-e)

## Descrição

Este projeto automatiza a emissão de Notas Fiscais de Serviço Eletrônicas (NFS-e) através de uma plataforma web, utilizando Selenium WebDriver para controlar o navegador Chrome.

A automação realiza login, leitura de dados de clientes a partir de uma planilha, preenchimento dos formulários no sistema, e simula a emissão das notas, facilitando e agilizando processos manuais.

## Funcionalidades Principais

- **Login automático:**
  Realiza autenticação utilizando credenciais armazenadas em arquivo `.env`.

- **Leitura de dados:**
  Importa CPF e valores dos clientes a partir de um arquivo CSV.

- **Processamento de clientes:**

  - Filtra clientes com CPF inválido, armazenando-os em arquivo separado.
  - Preenche os dados de endereço automaticamente quando necessário.
  - Seleciona o serviço correto em dropdown baseado em código.
  - Gera descrições personalizadas incluindo cálculo de imposto (17,72% do valor do cliente).
  - Preenche o valor da nota conforme o valor da planilha.
  - Para fins de teste, realiza clique no botão "Voltar" ao invés de confirmar a emissão da nota.

- **Gerenciamento de resultados:**

  - Clientes com CPF inválido são salvos em `sem_cpf.csv`.
  - Clientes com notas processadas são salvos em `notas_lancadas.csv`.

## Como usar

1. Crie um arquivo `.env` na pasta `data/secure/` com as variáveis:

   ```env
   LOGIN=seu_login_aqui
   SENHA_ISSE=sua_senha_aqui
   ```

2. Prepare a planilha `clientes_com_cpf.csv` dentro da pasta `data/output/` com os dados dos clientes.

3. Execute o script Python para iniciar a automação.

4. Ao final, verifique os arquivos `sem_cpf.csv` e `notas_lancadas.csv` na pasta `data/output/`.

---

# Service Invoice (NFS-e) Issuance Automation

## Overview

This project automates the issuance of Electronic Service Invoices (NFS-e) through a web platform using Selenium WebDriver to control the Chrome browser.

The automation logs in, reads client data from a spreadsheet, fills in the required forms, and simulates invoice issuance, streamlining manual tasks.

## Key Features

- **Automatic login:**
  Authenticates using credentials stored in a `.env` file.

- **Data import:**
  Loads clients' CPF and service values from a CSV file.

- **Client processing:**

  - Filters out clients with invalid CPF, saving them separately.
  - Automatically fills address fields when missing.
  - Selects the appropriate service option from a dropdown by code.
  - Generates customized service descriptions including tax calculation (17.72% of client value).
  - Inputs invoice value according to the spreadsheet.
  - For testing, clicks "Back" instead of confirming the invoice issuance.

- **Result management:**

  - Clients without valid CPF are saved in `sem_cpf.csv`.
  - Clients with processed invoices are saved in `notas_lancadas.csv`.

## How to Use

1. Create a `.env` file inside `data/secure/` folder with:

   ```env
   LOGIN=your_login_here
   SENHA_ISSE=your_password_here
   ```

2. Prepare the spreadsheet `clientes_com_cpf.csv` in the `data/output/` folder with client data.

3. Run the Python script to start the automation.

4. After completion, check the `sem_cpf.csv` and `notas_lancadas.csv` files in `data/output/`.
