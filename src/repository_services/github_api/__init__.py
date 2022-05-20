"""Handler/Wrapper for the Github rest API


"""
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
    response_text = ""
    
    if(debug):
        print("Endpoint: ", endpoint)
        print("Headers: ", headers)
    
    try:
        response = requests.get(endpoint, headers=headers)
        
        if(debug):
            print("URL: ", response.url)
            print("Status code: ", response.status_code)
            print("Response text: ", response.text)
            print("Redirection history: ", response.history)
        
        response_text = response.text
    except Exception as err:
        print("Error: ", err)
    
    return response_text

# Get repositories that have a specified amount of stars
# Just for testing
def get_repositories_with_stars(query=">1000000"):
    _show_debug("get_repositories_with_stars")
    
    enpoint_path = f"search/repositories?q=stars:{query}"
    endpoint = f"{api_base_url}{enpoint_path}"
    
    response = requests.get(endpoint)
    #response = requests.get(endpoint, data={"api_key": api_key})
    if(debug):
        print("Status code: ", response.status_code)
        print("Response text: ", response.text)
    return response.text

def print_rate_limits(user=username):
    _show_debug("get_user_repositories")
    
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
    response_text = ""
    
    # if(debug):
    #     print("Endpoint: ", endpoint)
    #     print("Headers: ", headers)
    
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
        
        response_text = r.text
    except Exception as err:
        print("Error: ", err)
    
    return response_text