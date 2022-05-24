from . import github_api
import json
import os

# If the "data" directory doesn't exist, create it
if(not os.path.exists(f".{os.path.sep}data")):
    os.mkdir(f".{os.path.sep}data")
    
    # If the "data" directory doesn't exist, create it
    if(not os.path.exists(f".{os.path.sep}data/github")):
        os.mkdir(f".{os.path.sep}data/github")

# The directory to save the data and the file name
data_folder_name = f".{os.path.sep}data{os.path.sep}"
file_name = "repository_list.json"

# Check last updated and if it was updated clone and upload to other services
old_repository_data_file = open(f"{data_folder_name}{file_name}")
old_repository_data = json.load(old_repository_data_file)
print("Typeof old repo list: ", type(old_repository_data))

# Get every repository
repository_list = github_api.get_every_user_repository_as_json(
    os.environ.get("USERNAME"))

older_list = github_api.get_older_list(old_repository_data, repository_list)
print("Not updated repositories: ", older_list)
print("Amount of repositories in the old list: ",
    github_api.get_older_repositories_count(old_repository_data))

# Dump the data in a json file
with open(f"{data_folder_name}{file_name}", "w") as f:
    json.dump(repository_list, f)

github_api.print_rate_limits()