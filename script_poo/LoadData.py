import requests
from Util import Util


class LoadData:
    def __init__(self, owner, repository, file_path):
        self.owner = owner
        self.repository = repository
        self.file_path = file_path
        self.access_token = "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"
        self.headers = {'Authorization' : 'Bearer ' + self.access_token,
                        'X-GitHub-Api-Version': '2022-11-28'
                        }
        self.base_url_api = "https://api.github.com"


    def repo_exists(self):
        Util.log_info(f"CARREGANDO OS DADOS")
        Util.log_info(f"Verificando o repositorio {self.repository}, para carregar o arquivo.")

        url = f'{self.base_url_api}/repos/{self.owner}/{self.repository}'
        response = requests.get(url)

        if response.status_code == 200:
            Util.log_info(f"O repositorio {self.repository} ja existe.")
            return True
        elif response.status_code == 404:
            Util.log_info(f"O repositorio {self.repository} nao existe. Criando o repositorio.")
            return False
        else:
            raise Exception(ReferenceError, f"Erro ao verificar o repositório {self.repository}. Código de resposta: {response.status_code}")


    def create_repo(self):
        url = f"{self.base_url_api}/user/repos"
        data = {
            "name" : self.repository,
            "description" : "Criando repo para carga de arquivos referente as linguagens de programa'xão utilizadas nas empresas",
            "private" : False
        }

        response = requests.post(url, json=data, headers=self.headers)
        if response.status_code == 201:
            Util.log_info(f"Repositorio {self.repository} criado com sucesso.")
        else:
            raise Exception(ReferenceError, f"Erro ao criar o repositório {self.repository}. Código de resposta: {response.status_code}")

    def load_data(self):
        url = f"{self.base_url_api}/repos/{self.owner}/{self.repository}/contents/{self.file_path}"
        if not self.repo_exists():
            self.create_repo()

        encoded_file = Util.file_to_base64(self.file_path)

        data = {
            "message" : "Importando novo aquivo de dados",
            "content" : encoded_file.decode("utf-8")
            }

        response = requests.put(url, json=data, headers=self.headers)
        if response.status_code == 201:
            Util.log_info(f"Arquivo {self.file_path} carregado com sucesso.")
        else:
            raise Exception(ReferenceError, f"Erro ao criar o repositório {self.repository}. Código de resposta: {response.status_code}")