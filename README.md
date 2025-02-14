# Python Бот-помощник: Руководство по использыванию и документация
## Описание проекта
Данный бот предназначен для ответов на не сложные вопросы, а вопросы посложнее перенаправляет на специалиста. Бот обучается с помощью нейросети.
## Пример бота
### [Telegram бот](https://t.me/ForspeechBot)
![Анимация](https://github.com/user-attachments/assets/80435a92-ef3b-43c6-9c9d-073cb1ba9357)
### [Сообщество Вконтакте](https://vk.com/club229054478)
![Анимация](https://github.com/user-attachments/assets/4cd3ef63-b070-4bc3-93fc-32a6a472fe5b)
## Что понадобится?
### Предварительные требования
Скачайте или склонируйте репозиторий на свой компьютер.
Python3 должен быть уже установлен. 
### Установка зависимостей
Используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Дополнительные требования
#### Telegram
Создать телеграм бота и получить токен. Для регистрации и получения токена, нужно написать в [@BotFather](https://t.me/BotFather)
```
/newbot - регистрация нового бота
/token - получить токен бота 
```
Получить ID вашего чата. Чтобы получить свой chat_id, напишите в Telegram специальному боту: [@userinfobot](https://telegram.me/userinfobot)
#### Вконтакте
- Зарегестрируйтесь в социальной сети [Вконтакте](https://vk.com).
- Создайте [сообщество](https://vk.com/groups?w=groups_create_new__main) Вконтакте.
- Разрешить отправку сообщений. На странице сообщества перейдите "Управление" → "Сообшения", включите сообщения сообщества.
- Получите API-токен сообщества. На странице сообщества перейдите "Управление" → "Настройки" → "Работа с API".
#### DialogFlow
- Создайте проект [DialogFlow](https://cloud.google.com/dialogflow/es/docs/quick/setup), для получения ```project_id```
- Создайте [агента DialogFlow](https://cloud.google.com/dialogflow/es/docs/quick/build-agent)
### Переменные окружения
Создайте файл ```.env``` в вашей директории проекта, откройте его в любом текстовом редакторе. Вам понадобятся следующие переменные окружения:
```
TELEGRAM_TOKEN=Ваш API_token телеграм бота
VK_TOKEN=Ваш API_token сообщества вконтакте
PROJECT_ID=project_id проекта DialogFlow
CHAT_ID=ID вашего чата телеграм
TELEGRAM_LOGGER=Ваш API_token телеграм бота для логов
```
## Как запустить
### Обучить нейросеть
Для обучения нейросети создайте файл в директории ```training_phrases.json```, откройте в любом тестовом редакторе внесите обучающие данные. [Пример](https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json) обучающих фраз.
Запустите команду
```bush
python load_test_data.py
```
После выполнения команды данные будут загружены в проект DialogFlow и будут использоваться в ботах.
### Запуск Telegram бота
```bush
python tg_bot.py
```
Напишите боту любой вопрос, который передали в файле ```training_phrases.json```
### Запуск бота Вконтакте
```bush
python vk_bot
```
Напишите любой вопрос сообществу, который передали в файле ```training_phrases.json```
## Цели проекта
Проект написан в образовательных целях.



