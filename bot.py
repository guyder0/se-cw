import requests, time, os
import backend # тут загружается и будет использоваться обученная модель

TOKEN = os.environ.get('SE-CW_TOKEN') # токен бота загружается из переменных среды
API_URL = 'https://api.telegram.org/bot' # сюда отправляются запросы для telegram bot api

# начинаем long-polling
offset = -2 # чтобы получить все апдейты пока бот не работал
while True:
    updates = requests.get(f'{API_URL}{TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']: # проверяем есть ли вообще апдейты
        for result in updates['result']: # пробегаемся по всем апдейтам в цикле
            user_id = result['message']['from']['id'] # сохраняем id пользователя (совпадает с id чата)
            offset = result['update_id'] # чтобы не получать старые апдейты
            if 'photo' in result['message']: # есть ли в сообщении фото
                print('Отправлено фото')
            else: # если отправлено не фото, то сообщить об этом пользователю
                response = requests.get(url=f'{API_URL}{TOKEN}/sendMessage',
                                        params={
                                            'chat_id': user_id,
                                            'text': 'Боту можно отправлять только изображения!'
                                        })

    time.sleep(3)