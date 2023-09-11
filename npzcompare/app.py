from flask import Flask, request
from github import Github, GithubIntegration
from pathlib import Path

app = Flask(__name__)
app_id = '388093'

cert_path = Path(__file__).parent / "bot_key.pem"
with cert_path.open() as cert_file:
    app_key = cert_file.read()

github_integration = GithubIntegration(app_id, app_key)

@app.route("/", methods=["POST"])
def github_bot():
    payload = request.json

    # PR creation of PR synchronization
    if not all(k in payload.keys() for k in ['action', 'pull_request'])\
            and payload['action'] in ['opened', 'synchronized']:
        return "ok"

    owner = payload['repository']['owner']['login']
    repository_name = payload['repository']['name']

    github_connection = Github(
        login_or_token=github_integration.get_access_token(
            github_integration.get_installation(owner, repo_name).id
        )
    )
    repo = github_connection.get_repo(f"{owner}/{repo_name}")
    
    print(payload)

