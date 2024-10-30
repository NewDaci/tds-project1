import requests

# Replace this with your GitHub token
GITHUB_TOKEN = 'here'

# List of usernames to query
usernames = ["huggingface", "brunosimon", "MysteriousSonOfGod", "fabpot", "stof"]

# Construct the query dynamically to request each user
query = """
query {
"""
for username in usernames:
    query += f"""
    {username}: user(login: "{username}") {{
        login
        name
        company
        location
        email
        bio
        publicRepos: repositories(privacy: PUBLIC) {{
            totalCount
        }}
        followers {{
            totalCount
        }}
        following {{
            totalCount
        }}
        createdAt
    }}
    """
query += "\n}"

# Set up headers with authorization
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

# Send the request
response = requests.post(
    'https://api.github.com/graphql',
    json={"query": query},
    headers=headers
)

# Check for a successful response
if response.status_code == 200:
    data = response.json().get("data", {})
    print(f"Fetched {len(data)} users.")
    for username, user_data in data.items():
        print(f"Username: {username}, Data: {user_data}")
else:
    print("Error:", response.status_code, response.json())