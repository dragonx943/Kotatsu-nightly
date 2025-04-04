import requests
from datetime import datetime, timedelta

time = datetime.now() - timedelta(days=1)
time_format = time.isoformat() + 'Z'

repos = [
    {'owner': 'KotatsuApp', 'name': 'Kotatsu'},
    {'owner': 'KotatsuApp', 'name': 'kotatsu-parsers'}
]

params = {
    'since': time_format,
}

with open('commits.txt', 'w', encoding='utf-8') as file:
    file.write("## What's Changed\n\n")
    
    ctribu_set = set()
    appU_status = False
    parsersU_status = False

    file.write("### App Updates:\n")

    for repo in repos:
        url = f'https://api.github.com/repos/{repo["owner"]}/{repo["name"]}/commits'
        
        response = requests.get(url, params=params)

        if response.status_code == 200:
            commits = response.json()

            for commit in commits:
                commit_message = commit['commit']['message'].split('\n')[0]
                commit_sha = commit['sha'][:7]
                commit_url = commit['html_url']

                if repo['name'] == 'Kotatsu':
                    appU_status = True
                    file.write(f"- {commit_message} - [`{commit_sha}`]({commit_url})\n")
                elif repo['name'] == 'kotatsu-parsers':
                    parsersU_status = True

    if not appU_status:
        file.write("- Nothing changed...\n")
    
    if parsersU_status:
        file.write("\n### Parsers Updates:\n")
        for repo in repos:
            if repo['name'] == 'kotatsu-parsers':
                url = f'https://api.github.com/repos/{repo["owner"]}/{repo["name"]}/commits'
                
                response = requests.get(url, params=params)

                if response.status_code == 200:
                    commits = response.json()

                    for commit in commits:
                        commit_message = commit['commit']['message'].split('\n')[0]
                        commit_sha = commit['sha'][:7]
                        commit_url = commit['html_url']
                        
                        file.write(f"- {commit_message} - [`{commit_sha}`]({commit_url})\n")
    else:
        file.write("\n### Parsers Updates:\n- Nothing changed...\n")

    print("✅ File created: 📋 commits.txt")
