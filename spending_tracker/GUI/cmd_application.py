import click
import requests
import json
import pprint
import sys


# http://alamolo.pythonanywhere.com
client_url = 'http://localhost:5000'
headers = {'Content-type': 'application/json'}

proxies = {
    'http': None,
    'https': None
}


def api_post(url, payload):
    print(f'POST - {url} - {payload}')
    r = requests.post(
        url=url,
        json=payload,
        headers=headers,
        proxies=proxies
    )
    print(r.status_code)
    return r


def api_get(url):
    print(f'GET - {url}')
    r = requests.get(
        url=url,
        headers=headers,
        proxies=proxies
    )
    print(r.status_code)
    return r


def api_patch(url, payload):
    print(f'PATCH - {url} - {payload}')
    r = requests.patch(
        url=url,
        json=payload,
        headers=headers,
        proxies=proxies
    )
    print(r.status_code)
    return r


def api_delete(url):
    print(f'DELETE - {url}')
    r = requests.delete(
        url=url,
        headers=headers,
        proxies=proxies
    )
    print(r.status_code)
    return r


def get_user_uris(user):
    """Use this only if the exists"""
    entry_point = api_get(f'{client_url}/api/').json()
    users_uri = client_url + entry_point['users'] + user + '/'
    r = api_get(users_uri)
    if r.status_code == 404:
        return r.status_code
    r = r.json()
    user_uri = client_url + r['links']['self']
    wallet_uri = client_url + r['links']['wallet']
    categories_uri = client_url + r['links']['categories']
    return user_uri, wallet_uri, categories_uri


@click.command()
@click.option('--user', default='tester', help='username')
@click.option('--money', default=0, help='Users money')
def make_user(user, money):
    """Create user and give him money"""
    entry_point = api_get(f'{client_url}/api/').json()
    user_creation = client_url + entry_point['users']

    payload = {
        'user': user
    }

    r = api_post(url=user_creation, payload=payload)
    if int(r.status_code) == 409:
        print(f'User {user} already exists.')
        sys.exit()
    user_uri = r.headers['Location']
    r = api_get(user_uri)

    user_uri, wallet_uri, categories_uri = get_user_uris(user)
    print(user_uri)

    money_payload = dict(money=money)
    r = api_post(wallet_uri, payload=money_payload)
    print('Added money to the wallet')


def get_single_user(user):
    entry_point = api_get(f'{client_url}/api/').json()
    user_creation = client_url + entry_point['users'] + user + '/'
    r = api_get(url=user_creation)
    if r.status_code == 404:
        print(f'User {user} does not exists')
        sys.exit()
    print(pprint.pformat(r.json()))


@click.command()
@click.option('--collection', is_flag=True, help='Query all users')
@click.option('--user', default=None, help='Query single user')
def query_users(collection, user):
    if collection:
        get_all_users()
        return
    if user:
        get_single_user(user)
        return
    else:
        click.echo('You need to query either all or users. See --help for help.')


@click.command()
@click.option('--user', default=None, help='Username', required=True)
@click.option('--travel', default=0, help='Money to be added to travel.')
@click.option('--entertainment', default=0, help='Money to be added to entertainment.')
@click.option('--eating_out', help='Money to be added to eating out.')
@click.option('--house', default=0, help='Money to be added to house.')
@click.option('--bills', default=0, help='Money to be added to -bills.')
@click.option('--food', default=0, help='Money to be added to food.')
def create_categories(user, **kwargs):
    payload = dict(categories=dict())
    for args in kwargs:
        payload['categories'][args] = kwargs[args]
    print(payload)
    print(user)
    make_categories(user, payload)


@click.command()
@click.option('--user', default=None, help='User to be deleted', required=True)
def delete(user):
    delete_user(user)


def get_all_users():
    """Query all users from the database"""
    entry_point = api_get(f'{client_url}/api/').json()
    user_all = client_url + entry_point['users']
    r = api_get(user_all).json()
    print(pprint.pformat(r))


def make_categories(user, payload):
    user_uri, wallet_uri, categories_uri = get_user_uris(user)
    r = api_post(url=categories_uri, payload=payload)
    if r.status_code == 404:
        print(f'User {user} has no wallet to add categories to.')
        sys.exit()


def get_categories(user):
    user_uri, wallet_uri, categories_uri = get_user_uris(user)
    r = api_get(categories_uri)
    if r.status_code == 404:
        print(f'User {user} has no wallet.')
        sys.exit()
    print(r.json())
    print(pprint.pformat(r))


def delete_user(user):
    try:
        user_uri, wallet_uri, categories_uri = get_user_uris(user)
    except TypeError:
        print('User does not exist')
        sys.exit()
    r = api_delete(user_uri)
    if r.status_code == 404:
        print(f'Cant delete user - User {user} does not exist.')
        sys.exit()
    if r.status_code == 204:
        print('Deleted')


def add_categories(user, payload):
    user_uri, wallet_uri, categories_uri = get_user_uris(user)
    r = api_patch(categories_uri, payload)
    if r.status_code == 404:
        print(f'Cant delete user - User {user} does not exist.')
        sys.exit()
    if r.status_code == 400:
        print(r.json()['message'])


