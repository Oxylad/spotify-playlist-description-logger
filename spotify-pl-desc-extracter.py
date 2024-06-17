import requests, json, time, spotify_token, key
from datetime import datetime
from discord_webhook import DiscordWebhook

def get_token():
    # Define the URL and the headers
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Define the POST data
    data = {
        "grant_type": "client_credentials",
        "client_id": key.spotify_id,
        "client_secret": key.spotify_secret
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        response_data = response.json()
        # Get the access token
        access_token = response_data.get("access_token")
        print("Access Token:", access_token)

        # Save the token to token.py
        with open("spotify_token.py", "w") as token_file:
            token_file.write(f'spotify_token = "{access_token}"\n')
    else:
        print("Failed to retrieve token:", response.status_code)
        print("Response:", response.text)





def fetch_web_api(endpoint, method, body=None):
    url = f'https://api.spotify.com/{endpoint}'
    headers = {
        'Authorization': f'Bearer {spotify_token.spotify_token}',
        }
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=body)
    else:
        raise ValueError('Method not supported')
        response.raise_for_status()
    return response.json()

def get_playlist_description():
    endpoint = f'v1/playlists/{playlist_ID}'
    return fetch_web_api(endpoint, 'GET')


def check_token():
    with open('datafile.json', 'r') as infile:
        ans = json.load(infile)

    if list(ans)[0][0] == 401:
        get_token()


def main():
    previous_description = None

    while True:
        get_token()
        get_playlist_data = get_playlist_description()

        with open('datafile.json', 'w') as outfile:
            json.dump(get_playlist_data, outfile, indent=4)

        # Read data from JSON file
        with open('datafile.json', 'r') as infile:
            ans = json.load(infile)

        check_token()

        current_description = ans['description']
        if current_description != previous_description:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Send data to Discord webhook
            webhook = DiscordWebhook(
                url=discord_webhook_url,
                content=f"{current_time} : {current_description}"
            )
            response = webhook.execute()
        previous_description = current_description
        time.sleep(59)


main()


