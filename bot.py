import requests, time, os

TOKEN = os.environ.get('SE-CW_TOKEN')
API_URL = 'https://api.telegram.org/bot'

# тут начинаем long-polling
offset = -2
while True:
    updates = requests.get(f'{API_URL}{TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            if 'photo' in result['message']:
                print('Отправлено фото')
            else:
                print('Отправлено не фото')

    time.sleep(3)