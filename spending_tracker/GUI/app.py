import click
import requests
import json
import pprint


client_url = 'http://localhost:5000'
headers = {'Content-type': 'application/json'}


def api_post(url, payload):
    print(f'POST - {url} - {payload}')
    r = requests.post(
        url=url,
        json=payload,
        headers=headers
    )
    print(r.status_code)
    return r


def api_get(url):
    print(f'GET - {url}')
    r = requests.get(
        url=url,
        headers=headers
    )
    print(r.status_code)
    return r.json()


def api_put(url, payload):
    print(f'PUT - {url} - {payload}')
    r = requests.put(
        url=url,
        json=payload,
        headers=headers
    )
    print(r.status_code)
    return r.json()


def api_delete(url):
    print(f'DELETE - {url}')
    r = requests.delete(
        url=url,
        headers=headers
    )
    print(r.status_code)
    return r.json()


def get_user_uris(user):
    entry_point = api_get(f'{client_url}/api/')
    users_uri = client_url + entry_point['users'] + user + '/'
    r = api_get(users_uri)
    user_uri = client_url + r['links']['self']
    wallet_uri = client_url + r['links']['wallet']
    categories_uri = client_url + r['links']['categories']
    return user_uri, wallet_uri, categories_uri


# @click.command()
# @click.option('--user', default='tester', help='username')
# @click.option('--money', default=0, help='Users money')
# def make_user(user, money):
#     entry_point = requests.get(url=f'{url}/api/', headers=headers)
#     user_uri = entry_point['users']
#     payload = {
#         'user': user
#     }
#     r = requests.post(url=f'{url}{user_uri}', data=json.dumps(payload), headers=headers)
#     print(r.json())


# if __name__ == '__main__':
#     make_user()


def make_user(user, money):
    user_uri, wallet_uri, categories_uri = get_user_uris(user)

    payload = {
        'user': user
    }

    # Make user
    r = api_post(url=user_uri, payload=payload)
    if r.status_code == 409:
        Exception('user exists already')
    user_uri = r.headers['Location']

    # Get user
    r = api_get(user_uri)

    # Make wallet
    money_payload = dict(money=money)
    r = api_post(wallet_uri, payload=money_payload)
    print('Done')


def get_all_users():
    entry_point = api_get(f'{client_url}/api/')
    user_all = client_url + entry_point['users']
    r = api_get(user_all)
    print(pprint.pformat(r))


def make_categories(user, payload):
    user_uri, wallet_uri, categories_uri = get_user_uris(user)
    r = api_post(url=categories_uri, payload=payload)


def get_categories(user):
    user_uri, wallet_uri, categories_uri = get_user_uris(user)
    r = api_get(categories_uri)
    print(pprint.pformat(r))


def delete_user(user):
    user_uri, wallet_uri, categories_uri = get_user_uris(user)
    r = api_delete(user_uri)
    print(r)


def add_categories(user, payload):
    user_uri, wallet_uri, categories_uri = get_user_uris(user)
    r = api_put(categories_uri, payload)


asd = {
    'categories': {
        'travel': 10,
        'entertainment': 5
    }
}

add_categories('matti', asd)