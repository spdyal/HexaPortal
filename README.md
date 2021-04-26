# HexaPortal
Приложение на Flask, расчитанное на публикацию и просмотр миров игроков Hexagonal Sandbox.

В навигационной строке для неавторизованных пользователей в правом верхнем углу доступны кнопки для авторизации и регистрации. Если пользователь зашёл в свой аккаунт, в том же месте расположены кнопки перехода на личную страницу пользователя и деавторизации.
Под навигационной строкой есть кнопка, перенаправляющая на страницу игры Hexagonal Sandbox в Github

# Главная страница
На главной странице сайта видны все опубликованные пользователями миры. В табличке мира указано название мира, его описание, есть ссылка на личную страницу автора, а так же кнопка скачивания мира.
Если пользователь является автором мира, или же имеет должность модератора, ему доступны кнопки редактирования сведений о мире и удаления мира с сервера.
Если пользователь авторизован, ему доступна кнопка публикации нового мира.
# Личные страницы пользователей `/user/<id>`
На личной странице пользователя видны все опубликованные обладателем страницы миры. Структура табличек миров идентична табличкам с главной страницы, за исключением отсутствия подписи автора по очевидным причинам.
Если пользователь является модератором, ему доступна кнопка повышения обладателя страницы до модератора.
# Публикация мира `/new_world`
Страница публикации мира доступна исключительно авторизованным пользователям. В форме публикации мира есть поля ввода названия мира, его описания и выбора zip файла с миром.
# Редактирование сведений о мире `/edit_world/<id>`
Страница редактирования мира доступна исключительно авторизованным пользователям. В форме редактирования можно изменить название мира и его описание.
# Регистрация пользователя `/register`
В форме регистрации необходимо заполнить свою почту, пароль (дважды) и имя пользователя на сайте. Пароли обязаны совпадать, почта не должна повторять почту другого пользователя сайта.
# Авторизация пользователя `/login`
В форме авторизации необходимо указать свою почту и пароль. Данные, введённые пользователем обязаны совпадать с данными сервера.
# Деавторизация `/logout`
Деавторизация пользователя сбрасывает вход в аккаунт и перенаправляет пользователя на главную страницу.
# Повышение пользователя до уровня модератора `/make_mod/<id>`
Запрос повышения пользователя до уровня модератора доступен только авторизированным пользователям, являющимися модераторами. Повышение устанавливает пользователю с указанным в запросе ID уровень модератора и перенаправляет на его личную страницу.
# Удаление мира `/delete_world/<id>`
Запрос удаления мира доступен только авторизованным пользователям, являющимися либо модераторами, либо авторами мира. Удаление мира стирает данные мира из датабазы, удаляет его файл из архива и перенаправляет пользователя на главную страницу.
# Загрузка мира `/download_world/<id>`
Запрос загрузки мира загружает на диск пользователя zip файл мира с указанным ID. 

# О модераторах
Модераторы - особоуполномоченные пользователи, способные редактировать и удалять все миры на сервере, а так же повышать других пользователей до модераторов. Рядом с именами модераторов на сайте есть зелёный значок с подписью "модератор".
Данные для входа в тестовый аккаунт spdyal с правами модератора: 

Почта: a@a.a 

Пароль: a 

