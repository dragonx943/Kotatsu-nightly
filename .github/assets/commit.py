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
                commit_message = commit['commit']['message']
                commit_sha = commit['sha'][:7]
                commit_url = commit['html_url']
                author_login = commit['author']['login'] if commit.get('author') else commit['committer']['login']
                
                ctribu_set.add(author_login)

                if repo['name'] == 'Kotatsu':
                    appU_status = True
                    file.write(f"- {commit_message} [`({commit_sha})`]({commit_url})\n")
                elif repo['name'] == 'kotatsu-parsers':
                    parsersU_status = True
                    file.write(f"\n### Parsers Updates:\n- {commit_message} [`({commit_sha})`]({commit_url})\n")

    if not appU_status:
        file.write("- Nothing changed...\n")
    
    if not parsersU_status:
        file.write("\n### Parsers Updates:\n- Nothing changed...\n")
    
    file.write("\n## Contributors\n")
    ctribu_list = list(ctribu_set)
    for contributor in ctribu_list:
        contributor_url = f"https://github.com/{contributor}"
        avt_url = f"https://wsrv.nl/?url=github.com/{contributor}.png?w=64&h=64&mask=circle&fit=cover&maxage=1w"
        file.write(f'[<img src="{avt_url}" width="32" height="32" alt="{contributor}" />]({contributor_url})\n')
    
    if ctribu_list:
        if len(ctribu_list) == 1:
            ctribu_names = ctribu_list[0]
        else:
            ctribu_names = ', '.join(ctribu_list[:-1])
            ctribu_names += f", and {ctribu_list[-1]}"
        file.write(f"###### {ctribu_names}\n")

    print("✅ File created: 📋 commits.txt")