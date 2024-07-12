import aiohttp
from typing import List

import asyncio
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent


WEBSITE = 'https://pypi.org'
HEADERS = {"User-Agent": UserAgent().random}


async def fetch_page_content(session: aiohttp.ClientSession, url: str) -> str:
        """
        Функция для получения содержимого страницы.

        :param session: aiohttp.ClientSession объект для выполнения запроса
        :param url: URL страницы, которую нужно получить
        :return: Текстовое содержимое страницы
        """
        async with session.get(url, headers=HEADERS) as response:
            return await response.text()


class PyPILibrary:
    def __init__(self, url):
        self._url = url
        self._history_url = f"{url}#history" if url[-1] == '/' else f"{url}/#history"

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._parse())

    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def latest_version(self):
        return self._latest_version
    
    @property
    def versions(self):
        return self._versions
    
    @property
    def pip_comand(self):
        return self._pip_comand
    
    @property
    def maintainers(self):
        return self._maintainers
    
    async def _parse(self):
        async with aiohttp.ClientSession() as session:
            main_page_content = await fetch_page_content(session, self._url)
            main_page_parser = BS(main_page_content, "html.parser").find("main", {"id": "content"})

            page_title = main_page_parser.find("h1", {"class": "package-header__name"}).text.strip().split()
            self._name = page_title[0]
            self._latest_version = page_title[1]
            
            self._description = main_page_parser.find("p", {"class": "package-description__summary"}).text
            self._pip_comand = main_page_parser.find("span", {"id": "pip-command"}).text.strip()
    
            versios_page_content = await fetch_page_content(session, self._history_url)
            versions_page_parser = BS(versios_page_content, "html.parser").find_all("a", {"class": "card release__card"})

            versions = []
            for item in versions_page_parser:
                version = item.find("p", {"class": "release__version"}).text.strip()
                version_date = item.find("p", {"class": "release__version-date"}).text.strip()
                versions.append([version, version_date])

            self._versions = versions
        

class Searher:

    @classmethod
    async def search(cls, request: str) -> List[PyPILibrary]:
        async with aiohttp.ClientSession() as session:
            search_page_content = await fetch_page_content(session, cls.get_request_url(request))
            links_items: List[BS] = BS(search_page_content, "html.parser").find_all("a", {"class": "package-snippet"})

            libraries = []
            for item in links_items:
                library = {}

                href = item.get('href')

                library["url"] = WEBSITE + href
                library["name"] = item.find("span", {"class": "package-snippet__name"}).text.strip()
                library["description"] = item.find("p", {"class": "package-snippet__description"}).text.strip()
                library["version"] = item.find("span", {"class": "package-snippet__version"}).text.strip()
                library["date"] = item.find("span", {"class": "package-snippet__created"}).text.strip()

                libraries.append(library)

            return libraries

    @classmethod
    def get_request_url(cls, request):
        return f'{WEBSITE}/search/?q={request}&o='