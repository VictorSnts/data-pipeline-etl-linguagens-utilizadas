import requests
import pandas as pd
from Util import Util

class RepoData:
    def __init__(self, user_company):
        self.user_company = user_company
        self.access_token = "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"
        self.headers = {'Authorization' : 'Bearer ' + self.access_token,
                        'X-GitHub-Api-Version': '2022-11-28'
                        }
        self.base_url_api = "https://api.github.com"
        self.repos_list = self.get_repos()


    def get_pages_num(self):
        url = f"{self.base_url_api}/users/{self.user_company}/repos"
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


    def get_repos(self):
        Util.log_info(f"EXPORTANDO OS DADOS")
        Util.log_info(f"Obtendo infos completas dos repositorios de {self.user_company}")
        repos_list = []
        sum_repos = 0
        num_pages = self.get_pages_num()
        Util.log_info(f"Numero de paginas que serao acessadas: {num_pages}")

        page = 1
        while True:
            try:
                url = f"{self.base_url_api}/users/{self.user_company}/repos?page={page}"
                Util.log_info(f"URL da pagina: {url}")
                response = requests.get(url, headers=self.headers)
                repos_list.append(response.json())
                num_repos = len(response.json())
                Util.log_info(f"Numero de repos na pagina {page}: {num_repos}")
                sum_repos += num_repos
            except:
                repos_list.append(None)
            if page == num_pages: break
            page += 1

        Util.log_info(f"Total de repositorios: {sum_repos}")
        return(repos_list)
    

    def get_repos_info(self, info):
        Util.log_info(f"Obtendo {info} dos repositorios de {self.user_company}")
        list_infos = []
        for page in self.repos_list:
            for repo in page:
                list_infos.append(repo[info])
        return list_infos


    def get_data_df(self):
        Util.log_info(f"Gerando dataframe com as informacoes de {self.user_company}")
        list_repos_name = self.get_repos_info("name")
        list_repos_language = self.get_repos_info("language")
        data = {
            "repository" : list_repos_name,
            "language" : list_repos_language
            }
        return pd.DataFrame(data)
