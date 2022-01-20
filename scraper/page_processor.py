from bs4 import BeautifulSoup


class PageProcessor:
    relevant_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p']

    def __init__(self, html):
        self.__soup = BeautifulSoup(html, features='html.parser')
        self.__fulltext = ""
        self.__text_groups = dict(zip(PageProcessor.relevant_tags,
                                      [
                                          [self.append(element.text) for element in self.__soup.find_all(key_tag)]
                                          for key_tag in PageProcessor.relevant_tags]
                                      ))

    def append(self, text):
        self.__fulltext += text

    def get_fulltext(self):
        return self.__fulltext
