#!/usr/bin/env python3

import os
import random
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    raise_on_redirect=True,
    raise_on_status=True,
    allowed_methods=False,
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

def get_lastfm_track(user, key):
    response = http.get('http://ws.audioscrobbler.com/2.0/', params={
        'method': 'user.getrecenttracks',
        'user': user,
        'api_key': key,
        'format': 'json',
        'limit': '1',
    }, headers={
        'user-agent': 'https://github.com/jkseppan/nowplaying',
    }, timeout=10)
    response.raise_for_status()
    json = response.json()
    track = json['recenttracks']['track'][0]
    return f"{track['name']} by {track['artist']['#text']}"

def set_github_status(user, token, emoji, message):
    mutation = """
        mutation SetUserStatus($emoji:String, $message:String) {
          changeUserStatus(input: {emoji: $emoji, message: $message}) {
            clientMutationId
          }
        }
    """
    variables = {'emoji': emoji, 'message': message}
    response = http.post(
        'https://api.github.com/graphql',
        json={'query': mutation, 'variables': variables},
        headers={
            'user-agent': 'https://github.com/jkseppan/nowplaying',
            'authorization': f'token {token}',
        },
        timeout=10
    )
    response.raise_for_status()
    return response.json()

def main():
    try:
        lf_user = os.environ['lf_user']
        lf_key = os.environ['lf_key']
        gh_user = os.environ['gh_user']
        gh_token = os.environ['gh_token']
    except KeyError:
        print("Set environment variables lf_user, lf_key, gh_user, gh_token")
        print("For lf_key see https://www.last.fm/api/account/create")
        print("For gh_token see https://github.com/settings/tokens")
        raise
    track = get_lastfm_track(lf_user, lf_key)
    print(track)
    if track:
        emoji = random.choice((
            ':musical_note:',
            ':musical_score:',
            ':musical_keyboard:',
            ':notes:',
            ':headphones:',
            ':man_dancing:',
            ':loudspeaker:',
        ))
        print(set_github_status(gh_user, gh_token, emoji, f"Now playing: {track}"))

if __name__ == '__main__':
    main()
