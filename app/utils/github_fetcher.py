import requests
import os
from typing import List, Optional

def get_organization_members(username: str) -> Optional[List[str]]:
    url = f"https://api.github.com/orgs/{username}/public_members"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        members_data = response.json()
        return [member['login'] for member in members_data]
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Organization '{username}' not found on GitHub.")
        else:
            print(f"HTTP Error fetching GitHub members for '{username}': {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred fetching GitHub data: {e}")
        return None