import requests
import csv
import sys

token="here"
headers = {"Authorization": f"token {token}"}

# run this for 4 times to extract all the data
# https://api.github.com/search/users?q=location:Paris%20followers:>200&per_page=100&page=1
# here page will run from 1 to 4 that will extract all 379 users of paris with more than 200 followers.

page_number = 1
location="Paris"
followers="200"
base_url = f'https://api.github.com/search/users?q=location:{location} followers:>{followers}&per_page=100&page={page_number}'

all_users = [] # this contains all the users in paris who has more than 200 followers

res = requests.get(base_url, headers=headers)
if res.status_code !=200:
    print("Some error encountered", res.status_code, res.json()["message"])
    sys.exit()

total_users=res.json().get('total_count',0)
print(f"Total users who are in {location} and have more than {followers} followers:",total_users)


while len(all_users) < total_users:
    base_url = f'https://api.github.com/search/users?q=location:{location} followers:>{followers}&per_page=100&page={page_number}'
    response = requests.get(base_url, headers=headers)
    data = response.json()
    if response.status_code !=200:
        print("Some error encountered", response.status_code, data["message"])
        sys.exit()
    
    # Add users from the current page to the list
    all_users.extend(data.get('items', []))
    print(f"printing length of all users after scrapping page no.: {page_number}",len(all_users))
    print(f" {len(data.get('items', []))} users on the page no.: {page_number}")
    # Check if we have received fewer than 100 users (indicates the last page)

    if len(data.get('items', [])) < 100:
        print("On the last page breaking the loop")
        break  
    
    page_number += 1

print("page no till scraped:",page_number)
print("all users length:",len(all_users))


# below code to generate the users.csv file that contains details about all the users that are in paris with more than 200 followers.

print("Now fetching each user details....")
# Fetch user details
def get_user_details(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=headers)
    return response.json()

# Save users to CSV
def save_users_to_csv(users, filename="users.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "login",
                "name",
                "company",
                "location",
                "email",
                "hireable",
                "bio",
                "public_repos",
                "followers",
                "following",
                "created_at",
            ],
        )
        writer.writeheader()
        for user in users:
            writer.writerow(user)

            
# Function to clean up company names
def clean_company_name(company):
    if company:
        return company.strip().lstrip('@').upper()
    return company

counter = 1
user_data = []
for user in all_users:
        details = get_user_details(user["login"])
        print(f"Getting details {counter} for the user:", user["login"])
        user_data.append(
            {
                "login": details["login"],
                "name": details.get("name", ""),
                # Use an empty string if company is None
                "company": clean_company_name(details.get("company", "") or ""),  # Handle NoneType
                "location": details.get("location", ""),
                "email": details.get("email", ""),
                "hireable": "true" if details.get("hireable") is True else "false", 
                "bio": details.get("bio", ""),
                "public_repos": details.get("public_repos", 0),
                "followers": details.get("followers", 0),
                "following": details.get("following", 0),
                "created_at": details.get("created_at", ""),
            }
        )
        counter += 1


save_users_to_csv(user_data)
print("users.csv file created!")