
import requests
import pandas as pd
import base64
from datetime import datetime

DATE = datetime.now().strftime('%Y%m%d')
ACCESS_TOKEN = "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"
HEADERS = {'Authorization' : 'Bearer ' + ACCESS_TOKEN,
           'X-GitHub-Api-Version': '2022-11-28'}
BASE_URL_API = "https://api.github.com"
USER_COMPANY = "nathos"
SAVE_DATA_INFO = {
    "file_name" : f"{USER_COMPANY}_repos_languages_{DATE}.csv",
    "owner" : "VictorSnts",
    "repo" : "linguagens-utilizadas-empresas"
}

## OK
def print_info(info):
    print(f"INFO: {info}")
    print("--")

## OK
def get_pages_num(url):
    response = requests.get(url)
    link_header = response.headers.get('link')

    if link_header:
        links = link_header.split(',')
        last_page_info = next(link for link in links if 'rel="last"' in link)
        total_pages = int(last_page_info.split(';')[0].split("page=")[-1].replace(">", ""))
        return total_pages
    else:
        if response.status_code == 200: return 1
        else: raise Exception(ReferenceError, f"Nao foi possivel identificar o numero de paginas. Código de resposta: {response.status_code}")

## OK
def get_repos():
    url = f"{BASE_URL_API}/users/{USER_COMPANY}/repos"
    print_info(url)
    repos_list = []
    sum_repos = 0
    pages_num = get_pages_num(url)
    print_info(f"Numero de paginas que serao acessadas: {pages_num}")

    page = 1
    while True:
        try:
            url_page = f"{url}?page={page}"
            print_info(f"URL da pagina: {url_page}")
            response = requests.get(url_page, headers=HEADERS)
            repos_list.append(response.json())
            num_repos = len(response.json())
            print_info(f"Numero de repos na pagina {page}: {num_repos}")
            sum_repos += num_repos
        except:
            repos_list.append(None)
        if page == pages_num: break
        page += 1

    print_info(f"Total de repositorios: {sum_repos}")
    return(repos_list)

## OK
def get_repos_name(repos):
    list_repos_name = []

    for page in repos_list:
        for repo in page:
            list_repos_name.append(repo["name"])

    return list_repos_name

## OK
def get_repos_language(repos):
    list_repos_language = []

    for page in repos_list:
        for repo in page:
            list_repos_language.append(repo["language"])

    return list_repos_language

## OK
def create_df(data):
    return pd.DataFrame(data)

## OK
def save_data(data, file_name):
    df = create_df(data) ## OK
    df.to_csv(file_name, index=False) ## OK

## OK
def repo_exists(owner, repo):
    url = f'{BASE_URL_API}/repos/{owner}/{repo}'
    response = requests.get(url)

    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        raise Exception(ReferenceError, f"Erro ao verificar o repositório {repo}. Código de resposta: {response.status_code}")

## OK
def create_repo(repo, description):
    url = f"{BASE_URL_API}/user/repos"
    data = {
        "name" : repo,
        "description" : description,
        "private" : False
    }

    response = requests.post(url, json=data, headers=HEADERS)
    if response.status_code == 201:
        print_info(f"Repositorio {repo} criado com sucesso.")
    else:
        raise Exception(ReferenceError, f"Erro ao criar o repositório {repo}. Código de resposta: {response.status_code}")

## OK
def file_to_base64(file_name):
    with open(file_name, "rb") as file:
        file_content = file.read()

    return base64.b64encode(file_content)

## OK
def load_data(file_name, owner, repo):
    url = f"{BASE_URL_API}/repos/{owner}/{repo}/contents/{file_name}"
    encoded_file = file_to_base64(file_name)

    data = {
        "message" : "Importando novo aquivo de dados",
        "content" : encoded_file.decode("utf-8")
        }

    response = requests.put(url, json=data, headers=HEADERS)
    if response.status_code == 201:
        print_info(f"Arquivo {file_name} carregado com sucesso.")
    else:
        raise Exception(ReferenceError, f"Erro ao criar o repositório {repo}. Código de resposta: {response.status_code}")


# Exportando os Dados
print_info(f"EXPORTANDO OS DADOS")
print_info(f"Obtendo infos completas dos repositorios de {USER_COMPANY}")
repos_list = get_repos() ## OK


# Transformando os Dados
print_info(f"TRANSFORMANDO OS DADOS")
print_info(f"Obtendo nomes dos repositorio de {USER_COMPANY}")
list_repos_name = get_repos_name(repos_list) ## OK

print_info(f"Obtendo linguagens de programação dos repositorios de {USER_COMPANY}")
list_repos_language = get_repos_language(repos_list) ## OK

data = {
    "repository" : list_repos_name,
    "language" : list_repos_language
} ## OK

print_info(f"Salvando dados dos repositorios de {USER_COMPANY} no arquivo {SAVE_DATA_INFO['file_name']}")
save_data(data, SAVE_DATA_INFO["file_name"])


# Carregando os dados
print_info(f"CARREGANDO OS DADOS")
print_info(f"Verificando o repositorio {SAVE_DATA_INFO['repo']}, para carregar o arquivo.")
if repo_exists(SAVE_DATA_INFO["owner"], SAVE_DATA_INFO["repo"]):
    print_info(f"O repositorio {SAVE_DATA_INFO['repo']} ja existe.")
else:
    print_info(f"O repositorio {SAVE_DATA_INFO['repo']} nao existe. Criando o repositorio.")
    create_repo(SAVE_DATA_INFO['repo'], "Criando repo para carga de arquivos referente as linguagens de programa'xão utilizadas nas empresas")

print_info("Carregando o arquivo.")
load_data(SAVE_DATA_INFO["file_name"], SAVE_DATA_INFO["owner"], SAVE_DATA_INFO['repo'])



