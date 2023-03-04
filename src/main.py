import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

from requests_cache import CachedSession
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, DOWNLOADS, EXPECTED_STATUS, MAIN_DOC_URL,
                       PEP_URL)
from outputs import control_output
from utils import find_tag, get_response, get_soup

RESPONSE_LOG_ERROR = 'Ошибка при загрузке страницы {version_link}'
DOWLOAD_INFO = 'Архив был загружен и сохранён: {archive_path}'
ARGUMENTS_CLI = 'Аргументы командной строки: {args}'
PARSER_ERROR = 'Ошибка в работе парсера: {error}'


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url)
    sections_by_python = soup.select(
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1'
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            logging.add_message(
                RESPONSE_LOG_ERROR.format(version_link=version_link)
            )
            continue
        soup = get_soup(session, version_link)
        h1 = find_tag(soup, 'h1')
        dl = soup.find('dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            (version_link, h1.text, dl_text)
        )
    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = get_soup(session, MAIN_DOC_URL)
    sidebar = soup.find('div', {'class': 'sphinxsidebarwrapper'})
    for ul in sidebar.find_all('ul'):
        if 'All version' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ValueError('Значение не нашлось.')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (a_tag['href'], version, status)
        )
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_soup(session, downloads_url)
    urls_table = find_tag(soup, 'table', attrs={'class': 'docutils'})
    pdf_a4_tag = find_tag(
        urls_table,
        'a',
        {'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / DOWNLOADS
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url, verify=False)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(DOWLOAD_INFO.format(archive_path=archive_path))


def pep(session):
    soup = get_soup(session, PEP_URL)
    section = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    table = find_tag(section, 'table', attrs={'class': 'pep-zero-table'})
    tbody = find_tag(table, 'tbody')
    tr = tbody.find_all('tr')
    logs = []
    result = [('Статус', 'Количество')]
    count_pep = defaultdict(int)
    for item in tqdm(tr):
        td = find_tag(item, 'td')
        link = urljoin(PEP_URL, td.find_next_sibling().a['href'])
        status_table = td.text[1:]
        try:
            soup = get_soup(session, link)
        except ConnectionError:
            logging.add_message(
                RESPONSE_LOG_ERROR.format(version_link=link)
            )
            continue
        dl = find_tag(soup, 'dl')
        status_page = dl.find(string='Status').parent.find_next_sibling().text
        expected_status = EXPECTED_STATUS.get(status_table, [])
        if not expected_status:
            logging.info(f'Неизвестный ключ статуса: \'{status_table}\'')
        count_pep[status_page] += 1
    map(logging.info, logs)
    return [
        ('Статус', 'Количество'),
        *result.items(),
        ('Всего', sum(result.values())),
    ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(ARGUMENTS_CLI.format(args=args))
    try:
        session = CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception as error:
        logging.exception(
            PARSER_ERROR.format(error=error)
        )
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
