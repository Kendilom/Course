import requests
import json

BASE_URL = 'https://images-api.nasa.gov'

search_url = f'{BASE_URL}/search'
params = {
    'q': 'Curiosity rover Mars',
    'media_type': 'image',
    'page_size': 10
}

response = requests.get(search_url, params=params)
response.raise_for_status()

data = response.json()
with open('response.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

items = data['collection']['items']

nasa_ids = []

for item in items:
    nasa_id = item['data'][0]['nasa_id']
    nasa_ids.append(nasa_id)

print(nasa_ids)
downloaded = 0

for nasa_id in nasa_ids:
    if downloaded == 2:
        break

    asset_url = f'{BASE_URL}/asset/{nasa_id}'

    asset_response = requests.get(asset_url)
    asset_response.raise_for_status()

    asset_data = asset_response.json()


    files = asset_data['collection']['items']

    jpg_url = None

    for file in files:
        if file['href'].endswith('.jpg'):
            jpg_url = file['href']
            print(jpg_url)
            break

    if jpg_url is None:
        continue


    image_response = requests.get(jpg_url)
    image_response.raise_for_status()

    filename = f'mars_photo{downloaded + 1}.jpg'

    with open(filename, 'wb') as file:
        file.write(image_response.content)

    downloaded += 1


