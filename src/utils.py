from bs4 import BeautifulSoup
from requests import RequestException

from constants import ENCODING_UTF8
from exceptions import ParserFindTagException

GET_RESPONSE = 'Возникла ошибка при загрузке страницы {url}'
FIND_TAG_ERROR = 'Не найден тег {tag} {attrs}'


def get_response(session, url, encoding=ENCODING_UTF8):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException:
        raise ConnectionError(
            GET_RESPONSE.format(url=url)
        )


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(
        tag, attrs={} if attrs is None else attrs
    )
    if searched_tag is None:
        raise ParserFindTagException(
            FIND_TAG_ERROR.format(
                tag=tag,
                attrs=attrs
            )
        )
    return searched_tag


def get_soup(session, url, features='lxml'):
    return BeautifulSoup(
        get_response(session, url).text,
        features=features
    )
