from . import github_api
import json
import os

repository_list = github_api.get_user_repositories()

# If the "data" directory doesn't exist, create it
if(not os.path.exists(f".{os.path.sep}data")):
    os.mkdir(f".{os.path.sep}data")

# The directory to save the data and the file name
data_folder_name = f".{os.path.sep}data{os.path.sep}"
file_name = "repository_list.json"

# Check last updated and if it was updated clone and upload to other services
old_repository_data_file = open(f"{data_folder_name}{file_name}")
old_repository_data = json.load(old_repository_data_file)
older_list = github_api.get_older_list(old_repository_data[0], repository_list[0])
print("Older list: ", older_list)

# Dump the data in a json file
with open(f"{data_folder_name}{file_name}", "w") as f:
    json.dump(repository_list, f)

github_api.print_rate_limits()