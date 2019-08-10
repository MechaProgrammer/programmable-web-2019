import json
import requests

url = "http://localhost:5000/api"
headers = {'Content-type': 'application/json'}

resp = requests.post(url=f'{url}/users/', data=json.dumps({
    "user": "tester",
    "balance": 123
}), headers=headers)

print(resp.content)

resp = requests.post(f'{url}/users/', data=json.dumps({
    'user': 'tester_2',
    'balance': 1231
}), headers=headers)
print(resp.content)

resp = requests.post(f'{url}/user/tester/money/', data=json.dumps({
    'money': 111,
}), headers=headers)
print(resp.content)

resp = requests.post(f'{url}/user/tester_2/money/', data=json.dumps({
    'money': 123,
}), headers=headers)
print(resp.content)

resp = requests.post(f'{url}/categories/tester/', data=json.dumps({
  "travel": 10,
  "entertainment": 10,
  "eating_out": 10,
  "house": 10,
  "bills": 10,
  "food": 10
}), headers=headers)

print(resp.content)

resp = requests.post(f'{url}/categories/tester_2/', data=json.dumps({
  "travel": 10123,
  "entertainment": 1032,
  "eating_out": 1021,
  "house": 101,
  "bills": 1023,
  "food": 1032
}), headers=headers)

print(resp.content)