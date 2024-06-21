import os


class Keywords:
    def __init__(self):
        self.keywords = self.load_keywords()
        self.current_index = 0

    @staticmethod
    def load_keywords():
        keywords_str = os.getenv('KEYWORDS')
        return [keyword.strip() for keyword in keywords_str.split(',')]

    def get_next_keyword(self):
        if self.current_index < len(self.keywords):
            keyword = self.keywords[self.current_index]
            self.current_index += 1
            return keyword
        else:
            return None

    def save_state(self):
        with open('current_keyword_index.txt', 'w') as file:
            file.write(str(self.current_index))

    def load_state(self):
        try:
            with open('current_keyword_index.txt', 'r') as file:
                self.current_index = int(file.read())
        except FileNotFoundError:
            self.current_index = 0
