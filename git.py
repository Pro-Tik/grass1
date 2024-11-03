import os
import requests
import base64

# Configuration
GITHUB_USERNAME = "Pro-Tik"
GITHUB_TOKEN = "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"
DIRECTORY_PATH = os.getcwd()  # Current directory

# Create a new repository
def create_repository(repo_name):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "private": False,  # Set to True for a private repo
        "description": "Uploaded files from script"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f"Repository '{repo_name}' created successfully.")
    else:
        print(f"Failed to create repository: {response.content}")

# Upload files to the repository
def upload_files(repo_name):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/contents/"
    
    # List of files to ignore
    ignore_files = {'.git', 'COMMIT_EDITMSG', 'config', 'description', 'HEAD', 'index'}
    
    for root, dirs, files in os.walk(DIRECTORY_PATH):
        for file in files:
            # Skip files that are in the ignore list
            if file in ignore_files:
                print(f"Skipped {file} due to ignore rules.")
                continue

            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                content = f.read()
                b64_content = base64.b64encode(content).decode('utf-8')

            # Prepare the data to be sent to GitHub
            data = {
                "message": f"Add {file}",
                "content": b64_content,
                "path": os.path.relpath(file_path, DIRECTORY_PATH)
            }
            response = requests.put(url + data["path"], json=data, headers={"Authorization": f"token {GITHUB_TOKEN}"})

            if response.status_code == 201:
                print(f"Uploaded {file} to repository.")
            else:
                print(f"Failed to upload {file}: {response.content}")

# Main execution
if __name__ == "__main__":
    repo_name = input("Enter the repository name: ")
    create_repository(repo_name)
    upload_files(repo_name)
