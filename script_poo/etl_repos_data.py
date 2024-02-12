from RepoData import RepoData
from LoadData import LoadData
from datetime import datetime


USER_COMPANY = "apple"
LOAD_INFO = {
    "OWNER" : "VictorSnts",
    "REPOSITORY" : "linguagens-utilizadas-empresas"
}

DATE = datetime.now().strftime('%Y%m%d')
FILE = f"data/{USER_COMPANY}_repos_language_{DATE}.csv"


repo_data = RepoData(USER_COMPANY)
df_data   = repo_data.get_data_df()
df_data.to_csv(FILE, index=False)

loader = LoadData(LOAD_INFO["OWNER"], LOAD_INFO["REPOSITORY"], FILE)
loader.load_data()

# netflix_repo = RepoData("netflix")
# netflix_df = amazon_repo.get_data_df()
# print(netflix_df)

# spotify_repo = RepoData("spotify")
# spotify_df = amazon_repo.get_data_df()
# print(spotify_df)