import requests
import csv


token1="paste token here"
# after generating the users.csv file from get_users_csv.py 
# use the users.csv file so that it doesn't consume the API rate limit and work with the offline dataset.

repo_url = "https://api.github.com/users/{}/repos?per_page=100&page={}&sort=pushed"

# Save repositories to CSV
def save_repos_to_csv(repos, filename="repositories.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "login",
                "full_name",
                "created_at",
                "stargazers_count",
                "watchers_count",
                "language",
                "has_projects",
                "has_wiki",
                "license_name",
            ],
        )
        writer.writeheader()
        for repo in repos:
            writer.writerow(repo)


fake_data = [
{'login': 'huggingface', 'name': 'Hugging Face', 'company': '', 'location': 'NYC + Paris', 'email': '', 'hireable': '', 'bio': 'The AI community building the future.', 'public_repos': '259', 'followers': '37849', 'following': '0', 'created_at': '2017-02-12T11:20:28Z'},
{'login': 'brunosimon', 'name': 'Bruno Simon', 'company': 'CREATIVE JOURNEY', 'location': 'Paris', 'email': '', 'hireable': 'True', 'bio': '', 'public_repos': '79', 'followers': '18718', 'following': '0', 'created_at': '2013-09-11T23:44:41Z'},
{'login': 'MysteriousSonOfGod', 'name': 'Juste Elysée M.', 'company': 'ERMANUS EWECKHANAH', 'location': 'Paris (France)', 'email': '', 'hireable': 'false', 'bio': '💻📚 Code Seer👨\u200d💻, creator,...$:>Python, Javascript, Css3, Html5,...  \r\n#♞⏱️🎹🔬,...', 'public_repos': '1097', 'followers': '742', 'following': '11836', 'created_at': '2018-12-09T08:36:12Z'},
{'login': 'fabpot', 'name': 'Fabien Potencier', 'company': 'SYMFONY/PLATFORM.SH/BLACKFIRE', 'location': 'Paris, France', 'email': 'fabien@symfony.com', 'hireable': '', 'bio': 'Founder and project lead at Symfony\r\nCPO at Platform.sh\r\n', 'public_repos': '77', 'followers': '13239', 'following': '0', 'created_at': '2009-01-17T13:42:51Z'},
{'login': 'Charles-Chrismann', 'name': 'Charles Chrismann', 'company': "INSTITUT DE L'INTERNET ET DU MULTIMÉDIA (IIM)", 'location': 'Paris, La Défense', 'email': '', 'hireable': '', 'bio': "Étudiant en 3e année de Développement Web à l'IIM ", 'public_repos': '35', 'followers': '11725', 'following': '218358', 'created_at': '2021-01-28T14:18:01Z'},
{'login': 'stof', 'name': 'Christophe Coevoet', 'company': 'INCENTEEV', 'location': 'Paris', 'email': '', 'hireable': 'false', 'bio': '', 'public_repos': '674', 'followers': '2091', 'following': '39', 'created_at': '2010-10-14T13:56:42Z'}
]

repo_data = []
limit=1
flag=False

with open("users.csv", mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for user in reader:
# for i in ["app"]:
#     for user in fake_data:
        temp = []
        max_repos = 500
        pageno = 1

        if flag:
            break

        while len(temp) < max_repos:
            # Alternate headers based on API limit
            if limit <= 3100:
                response = requests.get(repo_url.format(user["login"], pageno), headers={"Authorization": f"token {token1}"})
            else:
                response = requests.get(repo_url.format(user["login"], pageno), headers={"Authorization": f"token {token1}"})

            limit += 1

            # Check for API rate limit error
            if response.status_code == 403:
                print("API LIMIT REACHED, breaking the loop")
                print("Current user whose repos was getting collected:", user["login"])
                flag = True
                break

            # print(response.status_code)

            # Check for successful response
            if response.status_code != 200:
                print("Error:", response.status_code)
                break

            repos = response.json()

            # Add repositories to the list
            temp.extend(repos)

            # Check if the current batch contains fewer than 100 repos, stop if it does
            if len(repos) < 100:
                break

            # Stop if we've reached the maximum number of repos to fetch (500)
            if len(temp) >= max_repos:
                break

            # Move to the next page
            print(f"Currently on page {pageno} for the user: {user['login']}")
            pageno += 1


        if not flag: #flag to check for API limit
            for repo in temp:
                repo_data.append(
                    {
                        "login": user["login"],
                        "full_name": repo["full_name"],
                        "created_at": repo["created_at"],
                        "stargazers_count": repo["stargazers_count"],
                        "watchers_count": repo["watchers_count"],
                        "language": repo.get("language", ""),
                        "has_projects": "true" if repo["has_projects"] else "false",  # Handle booleans
                        "has_wiki": "true" if repo["has_wiki"] else "false",  # Handle booleans
                        "license_name": (
                            repo.get("license", {}).get("key", "")
                            if repo.get("license")
                            else ""
                        ),  # Handle NoneType
                    }
                )


            # Return up to 500 repos
            print("Total Request send to the server till now:", limit)
            print("Total page went till page no. minus 1 is:", pageno-1)
            print("Total repo for the user:",user["login"],"is:",user["public_repos"],"out of which got scraped is:",len(temp))


if not flag:
    save_repos_to_csv(repo_data)
    print("repositories.csv file created!")
