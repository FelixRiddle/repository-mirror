from . import github_api
import json
import os

sep = os.path.sep

# If the "data" directory doesn't exist, create it
if(not os.path.exists(f".{sep}data")):
    os.mkdir(f".{sep}data")

# If the "github" directory doesn't exist, create it
if(not os.path.exists(f".{sep}data{sep}github")):
    os.mkdir(f".{sep}data{sep}github")

# The directory to save the data and the file name
data_folder_name = f".{sep}data{sep}github{sep}"
file_name = "repository_list.json"
github_repo_list_path = f"{data_folder_name}{file_name}"

# Get every repository
repository_list = github_api.get_every_user_repository_as_json(
    os.environ.get("USERNAME"))

if(os.path.exists(github_repo_list_path)):
    # Check last updated and if it was updated clone and upload to other services
    old_repository_data_file = open(github_repo_list_path)
    old_repository_data = json.load(old_repository_data_file)
    print("Typeof old repo list: ", type(old_repository_data))
    
    # Get repositories that have to be updated
    older_list = github_api.get_older_list(old_repository_data, repository_list)
    print("Not updated repositories: ", older_list)
    print("Amount of repositories in the old list: ",
        github_api.get_older_repositories_count(old_repository_data))

# Dump the data in a json file
with open(github_repo_list_path, "w") as f:
    json.dump(repository_list, f)

github_api.print_rate_limits()