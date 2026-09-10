import os
import re
import requests

USERNAME = "kocembaw"         
README_PATH = "README.md"
START = "<!--START_SECTION:activity-->"
END = "<!--END_SECTION:activity-->"

def fetch_recent_repos():
    url = f"https://api.github.com/users/kocembaw/repos"
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    resp = requests.get(url, params={"sort": "updated", "per_page": 5}, headers=headers)
    resp.raise_for_status()

    lines = []
    for repo in resp.json():
        name = repo["name"]
        link = repo["html_url"]
        desc = repo.get("description") or "brak opisu"
        lines.append(f"- [{name}]({link}) <<< {desc}")
    return "\n".join(lines)

def update_readme(content):
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()
    block = f"{START}\n{content}\n{END}"
    pattern = re.compile(f"{re.escape(START)}.*?{re.escape(END)}", re.DOTALL)
    readme = pattern.sub(block, readme)
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme)

if __name__ == "__main__":
    update_readme(fetch_recent_repos())
