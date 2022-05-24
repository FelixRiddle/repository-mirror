"""Handler/Wrapper for the Github rest API


"""
import datetime
import dateutil.parser
import os
import pprint
import requests
import time

api_base_url = "https://api.github.com/"
# Remember to set to false in the future
debug = True
# Check if it exists and assing it to token
token = os.environ.get("GITHUB_ACCESS_TOKEN")
username = os.environ.get("USERNAME")

def _get_auth_user_repos_query_params(query_params:dict={}) -> str:
    full_query_params = ""
    if(query_params):
        # Accessibility type
        # Ex: all, owner, public, private
        accessibility_type = query_params.get("type", "all")
        
        # Page to request, defaults to
        page_number = str(query_params.get("page", 1))
        
        # Repositories per page
        # 100 is the max
        # The code belows defaults to 30 if the user didn't provide a value
        per_page = str(query_params.get("per_page", 30))
        full_query_params = f"?page={page_number}&per_page={per_page}&type={accessibility_type}"
    return full_query_params

def _show_debug(fn_name=""):
    if(debug):
        print(f"github_api -> {fn_name}")

# Check which one is older
def is_older(old_date_utc_string, new_date_utc_string):
    old_date = get_utc_date_from_string(old_date_utc_string)
    new_date = get_utc_date_from_string(new_date_utc_string)
    
    if(old_date < new_date):
        return True
    else:
        return False

def get_utc_date_from_string(the_date):
    new_date = dateutil.parser.parse(the_date)
    return new_date

def get_older_repositories_count(old_rep_list):
    _show_debug("get_older_repositories_count():")
    return len(list(old_rep_list))

# Get a list of older repositories
def get_older_list(prev_rep_list, new_rep_list):
    """Get a list of older repositories
    
    Inserts the name of the repository in the list and
    a boolean determining if it's older or not.
    If it throws an error when trying to find the key,
    it will be set to false"""
    _show_debug("get_older_list():")
    
    older_repos_list = {}
    
    # print("Prev_rep_list: ")
    # pprint.pprint(prev_rep_list)
    
    for repo in prev_rep_list:
        # If the key name doesn't exist in the repo object
        if not "name" in repo:
            continue
        
        repo_name = repo["name"]
        try:
            older_repo_date = repo["pushed_at"]
            new_repo_date = repo["pushed_at"]
            
            older_repos_list[repo_name] = is_older(older_repo_date,
                new_repo_date)
        except Exception as err:
            if(debug):
                print("------------------------ EROR --------------------------")
                print(err)
            older_repos_list[repo_name] = False
    
    return older_repos_list

# Get the repositories of the user provided
def get_user_repositories(user:str=username,
        options:dict={"query_params": {}, "headers": {}}):
    _show_debug("get_user_repositories")
    
    if token is None:
        if(debug):
            print("Token doesn't exist!")
        
        return
    
    full_query_params = _get_auth_user_repos_query_params(options.get("query_params"))
    
    # Example url: https://api.github.com/felixriddle/repos
    # For organizations url: https://api.github.com/orgs/perseverancia/repos
    # Filter by type: https://api.github.com/users/octocat/repos?type=owner
    
    headers = {}
    # IDK github recommends this
    headers["Accept"] = "application/vnd.github.v3+json"
    # Example token
    headers["Authorization"] = f"token {token}"
    
    # This only lists public repositories
    #enpoint_path = f"users/{user}/repos"
    # Get repositories of the authenticated user
    enpoint_path = f"user/repos"
    endpoint = f"{api_base_url}{enpoint_path}{full_query_params}"
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
        
        data = response.json()
    except Exception as err:
        print("Error: ", err)
    
    return data

# Get every user repository as json
def get_every_user_repository_as_json(user:str=username,
        options:dict={ "query_params": { "per_page": 100, }, "sleep": 10, }) -> list:
    _show_debug("get_every_user_repository_as_json():")
    
    # Check if sleep exists and return its value, if not default to
    # the second parameter
    sleep_time = options.get("sleep", 10)
    page = 1
    all_repositories = []
    
    # Query params
    query_params = options.get("query_params")
    per_page = 1
    if(query_params):
        # Elements per page
        per_page = query_params.get("per_page", 100)
    
    while(True):
        data:list = get_user_repositories(user, {
            "query_params": {
                "per_page": per_page,
                "page": page,
                "type": "owner"
            }
        })
        
        # There are no more repositories to list
        if(len(data) <= 0):
            break
        
        for dictionary in data:
            all_repositories.append(dictionary)
        
        page += 1
        time.sleep(sleep_time)
    
    return all_repositories
    

# Print the rate limits
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