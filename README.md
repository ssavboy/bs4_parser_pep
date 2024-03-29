# Проект парсинга pep

## Задачи
 - спарсить данные обо всех документах PEP
 - сравнить статус на странице PEP со статусом в общем списке
 - посчитать количество PEP в каждом статусе и общее количество PEP; данные о статусе документа нужно брать со страницы каждого PEP, а не из общей таблицы
 - сохранить результат в табличном виде в csv-файл

## Описание аргументов и параметров

1. Режимы работы парсера `mode`:
  * `download` - скачивание архива с документацией актуальной версии Python
  * `latest-versions` - список ссылок на актуальные версии Python
  * `pep` - информация по статусам и количеству PEP
  * `whats-new` - список ссылок на описание обновлений Python

2. Опциональные параметры `option`:
  * `-h, --help` - описание аргументов для запуска парсера
  * `-c, --clear-cache` - очистка кэша
  * `-o {pretty,file}, --output {pretty,file}` - способы вывода информации, `PrettyTable` | `csv-файл`

## Подготовка и запуск проекта
- Клонировать репозиторий
    ```
    git@github.com:ssavboy/bs4_parser_pep.git
    ```
- Создать и активировать виртуальное окружение
    ```
    python -m venv venv
    ```
- Установить зависимости
    ```
    pip install -r requirements.txt
    ```
- Запустить main.py
    ```
    python main.py <mode> [option]
    ```

## Стэк технологии
- Python 3.7
- Logging
- <a href='https://pypi.org/project/requests/'>Requests</a> 
- <a href='https://pypi.org/project/requests-cache/'>Requests-Cache</a> 
- <a href='https://pypi.org/project/beautifulsoup4/'>BeautifulSoup4</a>
- <a href='https://pypi.org/project/prettytable/'>Prettytable</a>

## Автор: <a href='https://github.com/ssavboy'>Kirill Molchanov</a>
