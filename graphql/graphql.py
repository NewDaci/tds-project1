import requests
from env import token1

# Define the GraphQL query
query = """
{
  search(query: "location:Paris followers:>200", type: USER, first: 100) {
    edges {
      node {
        ... on User {
          login
          name
          repositories(first: 100, orderBy: {field: UPDATED_AT, direction: DESC}) {
            nodes {
              name
              createdAt
              stargazerCount
              primaryLanguage {
                name
              }
              licenseInfo {
                key
              }
            }
          }
        }
      }
    }
  }
}
"""

# Set up headers with your GitHub token
headers = {"Authorization": f"bearer {token1}"}
# Make the request
response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)

# Get the response data
data = response.json()
print(data)
