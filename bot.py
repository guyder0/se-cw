import requests, time, os
from backend import * # тут загружается и будет использоваться обученная модель

TOKEN = os.environ.get('SE-CW_TOKEN') # токен бота загружается из переменных среды
API_URL = 'https://api.telegram.org/bot' # сюда отправляются запросы для telegram bot api

# начинаем long-polling
offset = -2
while True:
    updates = requests.get(f'{API_URL}{TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            user_id = result['message']['from']['id']
            offset = result['update_id']

            if 'photo' in result['message']:
                file_id = result['message']['photo'][-1]['file_id']
                file_info = requests.get(f"{API_URL}{TOKEN}/getFile?file_id={file_id}").json()
                file_path = file_info['result']['file_path']
                response = requests.get(f"https://api.telegram.org/file/bot{TOKEN}/{file_path}")
                with open(INPUT_PTH, "wb") as file:
                    file.write(response.content)
                generate_monet()
                with open(OUTPUT_PTH, 'rb') as photo:
                    response = requests.post(f'{API_URL}{TOKEN}/sendPhoto',
                                             data={'chat_id': user_id}, files={'photo': photo})
            else:
                response = requests.get(url=f'{API_URL}{TOKEN}/sendMessage',
                                        params={
                                            'chat_id': user_id,
                                            'text': 'Боту можно отправлять только изображения!'
                                        })

    time.sleep(3)