import asyncio

from lib_parser import LibParser


def main():
    """
    Основная функция для запуска парсинга библиотеки.
    """
    url = r"https://pypi.org/project/fake-useragent/"

    lib = LibParser(url)
    print(lib.name)

if __name__ == "__main__":
    main()