import requests


url = 'https://api.hh.ru/vacancies?text=python%20OR%20javascript%20OR%20typescript%20OR%20java%20OR%20c%23&area=1&date_from=2025-03-12'

response = requests.get(url)
response.raise_for_status()

data = response.json()
print(data)