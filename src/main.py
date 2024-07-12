import asyncio

from pypi_parser import *


def main():
    """
    Основная функция для запуска парсинга библиотеки.
    """
    libs = asyncio.run(Searher.search("flet"))
    print(libs)

if __name__ == "__main__":
    main()