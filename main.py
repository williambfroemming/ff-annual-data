"""Script created to get the league data for wins, losses, points for, points against for all members.
Data is then used to be lifted and shifted into an Excel spreadsheet and dashboard with historical data"""

import requests
import csv

def create_member_data(rosters, users):
    # Create a dictionary to map user IDs to display names
    user_display_names = {entry['user_id']: entry['display_name'] for entry in users}

    # Create owner_roster_list using list comprehensions
    owner_roster_list = [
        {
            "owner_id": roster["owner_id"],
            "roster_id": roster["roster_id"],
            "fpts": roster["settings"]["fpts"] + roster["settings"]["fpts_decimal"] / 100,
            "fpts_against": roster["settings"]["fpts_against"] + roster["settings"]["fpts_against_decimal"] / 100,
            "wins": roster["settings"]["wins"],
            "losses": roster["settings"]["losses"],
            "display_name": user_display_names.get(roster["owner_id"])  # Get display name using the user_id map
        }
        for roster in rosters  # Loop through the rosters
    ]

    return owner_roster_list

def create_csv(data):
    # Specify the CSV file path
    csv_file_path = '<FILEPATH>'

    # Define the CSV fieldnames based on the dictionary keys
    fieldnames = ['owner_id', 'roster_id', 'wins', 'losses', 'fpts', 'fpts_against', 'display_name']

    # Write the data to the CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"\nCSV file '{csv_file_path}' has been created.")

def main():
    # Make a GET request to the Sleeper API endpoint for rosters
    rosters_response = requests.get('https://api.sleeper.app/v1/league/<LEAGUE_ID>/rosters').json()
    users_response = requests.get('https://api.sleeper.app/v1/league/<LEAGUE_ID/users').json()
    
    member_py_data = create_member_data(rosters_response, users_response)
    
    create_csv(member_py_data)

if __name__ == "__main__":
    main()
