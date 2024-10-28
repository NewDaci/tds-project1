import requests
import csv
from env import token1

HEADERS = {"Authorization": f"token {token1}"}

def get_users_in_basel():
    users = []
    query = "location:Paris+followers:>200"
    page = 1
    per_page = 100
    total_users = 0

    while True:
        url = f"https://api.github.com/search/users?q={query}&per_page={per_page}&page={page}"
        response = requests.get(url, headers=HEADERS)
        print(f"Fetching page {page}...")

        if response.status_code != 200:
            print("Error fetching data:", response.json())
            break

        data = response.json()
        users.extend(data['items'])
        total_users += len(data['items'])

        if len(data['items']) < per_page:
            break

        page += 1

    detailed_users = []
    for user in users:
        user_info = get_user_details(user['login'])
        detailed_users.append(user_info)

    return detailed_users

def get_user_details(username):
    user_url = f"https://api.github.com/users/{username}"
    user_data = requests.get(user_url, headers=HEADERS).json()

    return {
        'login': user_data['login'],
        'name': user_data['name'],
        'company': clean_company_name(user_data['company']),
        'location': user_data['location'],
        'email': user_data['email'],
        'hireable': user_data['hireable'],
        'bio': user_data['bio'],
        'public_repos': user_data['public_repos'],
        'followers': user_data['followers'],
        'following': user_data['following'],
        'created_at': user_data['created_at'],
    }

def clean_company_name(company):
    if company:
        company = company.strip().upper()
        if company.startswith('@'):
            company = company[1:]
    return company


def save_users_to_csv(users):
    with open('users4.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['login', 'name', 'company', 'location', 'email', 'hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at'])
        writer.writeheader()
        writer.writerows(users)


if __name__ == "__main__":
    users = get_users_in_basel()
    save_users_to_csv(users)

    print("Done")
