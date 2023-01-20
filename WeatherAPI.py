import requests

url = 'http://api.openweathermap.org/data/2.5/weather?q=Tripoli&appid=52a17d91b3ed0697b05a7dd6fdc708c4'

response = requests.get(url)
jsoncontent = response.json()

print(jsoncontent['main']['feels_like'])