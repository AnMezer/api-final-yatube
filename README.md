
# API, позволяющее создавать посты, комментировать их и оформлять подписку на выбранного пользователя.

**Эндпоинты:**
  - **/api/v1/posts/** - для создания, просмотра, редактирования постов.
  - **/api/v1/posts/<post_id>/comments/** - для создания, просмотра редактирования комментариев.
  - **/api/v1/groups/** - для просмотра списка сообществ.
  - **/api/v1/follow/** - для управления подписками.

1. Клонировать репозиторий и перейти в папку проекта:
  ```Bash
  git clone https://github.com/AnMezer/api-final-yatube.git
  ```
  ```Bash
  cd yatube_api
  ```
2. Cоздать и активировать виртуальное окружение:
  ```Bash
  python3 -m venv env
  ```
  ```Bash
  source env/bin/activate
  ```
3. Установить зависимости из файла requirements.txt:
  ```Bash
  python3 -m pip install --upgrade pip
  ```
  ```Bash
  pip install -r requirements.txt
  ```
4. Выполнить миграции:
  ```Bash
  python3 manage.py migrate
  ```
5. Запустить проект:
  ```Bash
  python3 manage.py runserver
  ```

[**Полная документация.**](https://anmezer.github.io/api-final-yatube/)
