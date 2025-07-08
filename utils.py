# --- Remove read-only file attribute ---
import re
import requests
import os
import stat


def remove_readonly(func, path, _):
    """Error handler for the shutil.rmtree function.

    Args:
        func (function): The function that raised the exception.
        path (str): The path to the file that caused the exception.
        _: The exception information.
    """
    # Check the permissions and make the file writeable if needed
    os.chmod(path, stat.S_IWRITE)

    # Retry the operation
    func(path)

# --- Check if the provided URL is a valid GitHub repository URL ---
def is_valid_github_url(url):
    """Check if the provided URL is a valid GitHub repository URL.

    Args:
        url (str): The provided URL.
    
    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    # Check if the URL matches the GitHub repository URL pattern
    github_repo_url_pattern = r'https?://github\.com/[\w.-]+/[\w.-]+/?'
    if not re.match(github_repo_url_pattern, url):
        print("This is not a valid GitHub repository URL")
        return False
    
    # Check if the URL is reachable
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return False
        if response.headers.get('Server') != 'github.com':
            return False
        return True
    except:
        print("This is not a valid GitHub repository URL")
        return False
