import requests

url = 'https://github.com/Justin-Stevenson/fantasy-football-projections-2021/blob/master/data/qb.json'
result = requests.get(url, allow_redirects=False)

print(result.status_code)

something = {
    "name": "Justin"
}

value = something['message']

print(value.type())