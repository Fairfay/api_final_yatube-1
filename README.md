## API YATUBE
---
#### Что это?
API YATUBE - это финальный проект спринта №9 в учебной программе Яндекс.Практикум.
Он был написан для изучения возможностей API фреймворка Django Rest.
YATUBE представляет из себя мини-соцсеть с возможностью регистрации и авторизации, 
публикации и просмотре записей, подписки на интересных авторов.
Все взаимодействие с проектом происходит исключительно посредством API запросов на сервер.  
#### Как установить?
скачать репозиторий с проектом по команде:
```
git clone https://github.com/Shiiq/api_final_yatube
```  
установить и активировать виртуальное окружение:
```
python -m venv venv
source venv/Scripts/activate
```
установить зависимости:
```
pip install -r requirements.txt
```  
выполнить миграции:
```
python manage.py migrate
```  
запустить сервер разработки:
```
python manage.py runserver
```

Готово! Можно попробовать отправить несколько запросов на сервер.

#### Как пользоваться?
Регистрируемся, отправив POST запрос на эндпоинт `/users/`:
```
{
    "username": "ваш юзернейм",
    "password": "ваш пароль"
}
```
Теперь нужно получить токен, отправим POST запрос 
с параметрами `"username", "password"` на эндпоинт `/jwt/create/`.
Если все сделано верно, ответ от сервера будет выглядеть так:
```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI ...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1 ..."
}
```
Готово! Для дальнейшей работы с API необходимо в заголовках(Headers) запроса 
передавать дополнительный параметр _Authorization_ со таким значением:
```
Bearer 'здесь должен быть токен из поля access'
```  
Рассмотрим пару запросов, например для публикации поста.
В теле запроса нужно указать такие параметры: 
"text" - основное содержимое, текст поста,
"group" (принимает целочисленное значение, id группы) - опциально, группа к которой будет принадлежать пост.
Теперь отправим POST запрос на эндпоинт `/posts/`:
```
{
    "text": "La-la-la",
    "group": "1"
}
```
Посмотреть список публикаций можно через пустой GET запрос на эндпоинт `/posts/`.
А подписаться на интересного автора можно таким способом. Отправим POST запрос на `/follow/` 
с параметром `username`, куда должен быть вписан юзернейм автора. Если все получилось, при GET запросе
на `/follow/` будет показан список актуальных подписок. Выглядит это так:
```
{
    "user": "Вы",
    "following": "Интересный автор"
}
```  
Подробная карта доступных эндпойнтов и запросов проекта доступна по адресу `/redoc/`   
Это был краткий обзор функционала проекта API YATUBE.  
#### Автор: Киряков Петр, 2022
