"""Handler/Wrapper for the Github rest API


"""
import datetime
import os
import requests

api_base_url = "https://api.github.com/"
# Remember to set to false in the future
debug = True
# Check if it exists and assing it to token
token = os.environ.get("GITHUB_ACCESS_TOKEN")
username = os.environ.get("USERNAME")

def _show_debug(fn_name=""):
    if(debug):
        print(f"github_api -> {fn_name}")

# Check which one is older
def is_older(old_date, new_date):
    if(old_date < new_date):
        return True
    else:
        return False

def get_utc_date_from_string(the_date):
    return datetime.datetime.strptime(the_date,
        "%Y-%m-%dT%H:%M:%S.%fZ")

# Get a list of older repositories
def get_older_list(prev_rep_list, new_rep_list):
    """Get a list of older repositories
    
    Inserts the name of the repository in the list and
    a boolean determining if it's older or not.
    If it throws an error when trying to find the key,
    it will be set to false"""
    older_repos_list = {}
    
    for key, val in prev_rep_list:
        try:
            # TODO: Parse dates
            older_repo_date = prev_rep_list[key]["pushed_at"]
            new_repo_date = new_rep_list[key]["pushed_at"]
            
            older_repos_list[key] = is_older(older_repo_date,
                new_repo_date)
        except Exception as err:
            older_repos_list[key] = False
    
    return older_repos_list

# Get the repositories of the user provided
def get_user_repositories(user=username):
    _show_debug("get_user_repositories")
    
    if token is None:
        if(debug):
            print("Token doesn't exist!")
        
        return
    
    # Example url: https://api.github.com/felixriddle/repos
    # For organizations url: https://api.github.com/orgs/perseverancia/repos
    # Filter by type: https://api.github.com/users/octocat/repos?type=owner
    headers = {
        # Example token
        "Authorization": f"token {token}"
    }
    
    enpoint_path = f"users/{user}/repos"
    endpoint = f"{api_base_url}{enpoint_path}"
    response = ""
    data = ""
    
    if(debug):
        print("Endpoint: ", endpoint)
        print("Headers: ", headers)
    
    try:
        response = requests.get(endpoint, headers=headers)
        
        if(debug):
            print("URL: ", response.url)
            print("Status code: ", response.status_code)
            print("Redirection history: ", response.history)
        
        data = response.json()
    except Exception as err:
        print("Error: ", err)
    
    return data
    

def print_rate_limits(user=username):
    _show_debug("print_rate_limits")
    
    if token is None:
        if(debug):
            print("Token doesn't exist!")
        
        return
    
    headers = {
        # Example token
        "Authorization": f"token {token}"
    }
    
    enpoint_path = f"users/{user}"
    endpoint = f"{api_base_url}{enpoint_path}"
    response = ""
    data = ""
    
    if(debug):
        print("Endpoint: ", endpoint)
        print("Headers: ", headers)
    
    try:
        r = requests.get(endpoint, headers=headers)
        
        if(r.headers["x-ratelimit-limit"] is not None):
            print("X-Ratelimit-Limit: ", r.headers["x-ratelimit-limit"])
        if(r.headers["x-ratelimit-remaining"] is not None):
            print("X-Ratelimit-Remaining: ", r.headers["x-ratelimit-remaining"])
        if(r.headers["x-ratelimit-reset"] is not None):
            print("X-Ratelimit-Reset: ", r.headers["x-ratelimit-reset"])
        if(r.headers["x-ratelimit-used"] is not None):
            print("X-Ratelimit-Used: ", r.headers["x-ratelimit-used"])
        
        data = r.json()
    except Exception as err:
        print("Error: ", err)
    
    return data