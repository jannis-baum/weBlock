from bs4 import BeautifulSoup

class PageProcessor:
    def __init__(self, html):
        self.__soup = BeautifulSoup(html, features="html.parser")

    def get_fulltext(self):
        return " ".join([element.text for element in self.__soup.find_all("p")])

    def get_all_paragraphs(self):
        return [element.text for element in self.__soup.find_all("p")]

