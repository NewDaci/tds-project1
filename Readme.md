- Used python's library `requests`, scraped the data by first querying the GitHub API endpoint `/search/users?q=location:Paris followers:>200` to retrieve users in Paris with over 200 followers, then retrieving each user’s details from `/users/{username}` and their repositories from `/users/{username}/repos` with parameter `sort=pushed`.

- An interesting fact from the analysis is that there is a GitHub user with the username "*huggingface*," which resembles the popular machine learning company "**Hugging Face"**. This suggests that developers who use usernames linked to well-known industry trends or brands may attract curiosity and potentially gain additional visibility or followers.

- Actionable recommendation: Developers in **Paris** working in specialized fields like machine learning or AI may benefit from aligning their GitHub usernames and projects with recognizable industry terms, as it seems that recognizable names may attract higher visibility among followers. Developers should maintain active profiles with frequent repository updates to improve visibility in search results.

## Usage

1. Run the Python script `get_users_csv.py` first.
- It will generate the `users.csv` for users in `Paris` with more than `200` followers.

2. Next, after getting the users run the `get_repos_csv.py` to get the top 500 repositories of each users in `users.csv` file.
- this will generate the `repositories.csv` file.

# Ensure you have a valid GitHub API `token` and install the python's `requests` library.
