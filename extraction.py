import os
import subprocess
import shutil
import stat
import sys
import time

from utils import is_valid_github_url, remove_readonly

# --------------------- The extraction process ---------------------
def extraction_tool(repo_url, zip_destination):
    """Extracts the source code from the provided GitHub repository URL in a zip file.

    Args:
        repo_url (str): The URL of the GitHub repository.
        zip_destination (str): The destination directory for the extracted files.
    """
    # Extract the repository name from the URL
    repo_name = repo_url.split('/')[-1].replace('.git', '')

    # Delete the target directory if it already exists
    if os.path.exists(repo_name):
        shutil.rmtree(repo_name, onerror=remove_readonly)

    # Create a directory to store the repository
    os.makedirs(repo_name, exist_ok=True)

    # Clone the repository using git command
    subprocess.run(['git', 'clone', repo_url, repo_name])
    
    # Check if the repo_name folder is empty
    if not os.listdir(repo_name):
        print("The repository is empty.")
        # Remove the repo directory in case of error
        if os.path.exists(repo_name):
            shutil.rmtree(repo_name)
        return
    
    # Traverse the repository and delete non-matching files
    for dirpath, dirnames, filenames in os.walk(repo_name, topdown=True):
        # Skip the .git directory
        if '.git' in dirnames:
            dirnames.remove('.git')
        for file in filenames:
            if not file.endswith(('.java', '.cpp', '.h', '.hpp', '.cs', '.py')):
                os.remove(os.path.join(dirpath, file))

    # Define the .git directory path
    git_dir_path = os.path.join(repo_name, '.git')

    # Set read, write, and execute permissions for the owner
    os.chmod(git_dir_path, stat.S_IRWXU)

    # Delete the .git directory with administrator privileges
    while os.path.exists(git_dir_path):
        # Loop because the directory can be deleted only after being released from all other processes
        if os.name == 'nt':  # For Windows
            subprocess.run(['rmdir', '/s', '/q', git_dir_path], shell=True, check=True)
        else:  # For Unix-based systems
            subprocess.run(['rm', '-rf', git_dir_path], check=True)
        time.sleep(1)

    # Zip the final folder
    shutil.make_archive(repo_name, 'zip', repo_name)

    # Define the destination file path
    dest_file_path = os.path.join(zip_destination, repo_name + '.zip')

    # Check if the file already exists
    if os.path.exists(dest_file_path):
        # If it does, delete it
        os.remove(dest_file_path)

    # Move the new file to the destination directory
    shutil.move(repo_name + '.zip', zip_destination)

    # Set read, write, and execute permissions for the owner
    os.chmod(repo_name, stat.S_IRWXU)

    # Delete the repository file with administrator privileges
    while os.path.exists(repo_name):
        # Loop because the directory can be deleted only after being released from all other processes
        if os.name == 'nt':  # For Windows
            subprocess.run(['rmdir', '/s', '/q', repo_name], shell=True, check=True)
        else:  # For Unix-based systems
            subprocess.run(['rm', '-rf', repo_name], check=True)
        time.sleep(1)

def main(argv):
    """Function that should be executed first.

    Args:
        argv (list[type]]): List of the provided CLI arguments.
    """
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Please provide a valid GitHub repository URL")
        sys.exit(1)

    # Get repository URL from Galaxy arguments and check if it is valid and get output path
    repo_url = sys.argv[1]
    zip_destination = sys.argv[2]

    # Check if the provided URL is a valid GitHub repository URL
    if not is_valid_github_url(repo_url):
        sys.exit(1)

    # Run the extraction tool
    extraction_tool(repo_url, zip_destination)

if __name__ == '__main__':
    print("Running Github-extraction-tool.")
    main(sys.argv)