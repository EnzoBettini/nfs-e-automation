# 🍎 Configuração para Mac

## Instalação

### 1. Instalar Python 3 (se ainda não tiver)
```bash
# Verificar se já tem Python 3
python3 --version

# Se necessário, instalar via Homebrew
brew install python3
```

### 2. Instalar dependências do projeto
```bash
# Na pasta raiz do projeto
# IMPORTANTE: Se pip3 install -r requirements.txt demorar muito (compilando pandas),
# você pode instalar apenas o que está faltando:
pip3 install webdriver-manager selenium python-dotenv

# OU se quiser instalar tudo do requirements.txt:
pip3 install -r requirements.txt
```

**Nota:** O pandas pode demorar vários minutos para compilar no Mac. Se você já tem pandas instalado (teste com `pip3 list | grep pandas`), pode instalar apenas as dependências que faltam.

## ChromeDriver - Como Funciona Agora

### ✅ Configuração Automática (Mac/Linux)
O código foi atualizado para usar **webdriver-manager** no Mac, que:
- Baixa automaticamente o ChromeDriver correto para sua versão do Chrome
- Atualiza automaticamente quando necessário
- Não precisa fazer download manual

### 🪟 Windows
No Windows, continua usando o arquivo `.exe` do diretório `src/others/chromedriver.exe`

### 🔧 Como o Código Detecta Automaticamente
```python
if sys.platform == "win32":
    # Windows: usa o caminho manual
    chromedriver_path = r"C:\Users\...\chromedriver.exe"
    service = Service(executable_path=chromedriver_path)
else:
    # Mac/Linux: usa webdriver-manager (automático)
    service = Service(ChromeDriverManager().install())
```

## Arquivos Atualizados

Todos os arquivos foram atualizados para funcionar no Mac:
- ✅ `src/treat_data.ipynb` - Tratamento de dados melhorado
- ✅ `src/get_cpf.ipynb` - ChromeDriver automático
- ✅ `src/invoices.ipynb` - ChromeDriver automático
- ✅ `src/tests/get_cpf_tests.ipynb` - ChromeDriver automático
- ✅ `src/tests/invoices_test.ipynb` - ChromeDriver automático
- ✅ `src/main.py` - Tratamento de dados + ChromeDriver automático

## Melhorias no Tratamento de Dados

O código agora:
- ✅ Remove linhas vazias (incluindo as que têm só vírgulas)
- ✅ Filtra IDs não numéricos (como aquele 'G' que dava erro)
- ✅ Cria automaticamente os diretórios `filtered` e `output` se não existirem
- ✅ Reseta os índices para ficarem sequenciais
- ✅ Tratamento de erros melhorado para evitar crashes

## Como Executar

```bash
# Executar notebooks
jupyter notebook src/get_cpf.ipynb

# Ou executar o script completo
python3 src/main.py
```

## Problemas Comuns

### Chrome não abre
```bash
# Verificar se o Chrome está instalado
open -a "Google Chrome"

# Se não tiver, instalar
brew install --cask google-chrome
```

### Erro de permissão no ChromeDriver
Na primeira execução, o Mac pode bloquear o ChromeDriver. Se isso acontecer:
1. Vá em **Preferências do Sistema > Privacidade e Segurança**
2. Permita a execução do ChromeDriver

### selenium ou webdriver-manager não encontrado
```bash
pip3 install --upgrade selenium webdriver-manager
```

## Diferenças Mac vs Windows

| Item | Windows | Mac |
|------|---------|-----|
| ChromeDriver | Manual (.exe) | Automático (webdriver-manager) |
| Separador de caminho | `\` | `/` |
| Python | `python` | `python3` |
| Pip | `pip` | `pip3` |

---

**Nota:** O código mantém compatibilidade total com Windows! 🎉

