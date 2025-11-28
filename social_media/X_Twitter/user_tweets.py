import requests
import os
import json
import datetime


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url():
    # Replace with user ID below
    username = "EFAparty"
    return f"https://api.twitter.com/2/users/by/username/{username}"


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {
        "tweet.fields": "created_at"}

def get_params_for_tweets():
    return {
        "tweet.fields": "created_at,public_metrics,entities,geo",
        "max_results": 50  # Change this value as needed (max 100)
    }


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def get_tweets_for_user(user_id):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = get_params_for_tweets()
    return connect_to_endpoint(url, params)

def main():
    url = create_url()
    params = get_params()
    user_id = connect_to_endpoint(url, params)['data']['id']
    json_response = get_tweets_for_user(user_id)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    # Save to a uniquely named file with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'user_tweets_output_{timestamp}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_response, f, ensure_ascii=False, indent=2)
    print(f"Saved output to {filename}")


if __name__ == "__main__":
    main()
