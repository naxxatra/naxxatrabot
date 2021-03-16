import random
import requests
from helpers import is_date, today as get_today


class Numbers:
    """
    Bot functions for consuming the Numbers API at https://numbersapi.com
    """
    def __init__(self, query=None):
        self.query = query
        self.api_root = "http://numbersapi.com"
        self.response_msg = None

    def random(self):
        """
        Return a random fact about all kinds of numbers
        :return: str
        """
        choices = ["trivia", "year", "date", "math"]
        random_choice = random.choice(choices)
        try:
            r = requests.get(f'{self.api_root}/random/{random_choice}')
            if r.status_code == 200:
                print(f"Numbers.random(): Fetched a random {random_choice} fact")
                return r.text
        except Exception as e:
            print("Numbers.random(): Exception:", e)

    def math(self, number):
        """
        Return a mathematical trivia about a number
        :return: str
        """
        print(f"Numbers.math(): Mathematical Trivia about {number}")
        try:
            r = requests.get(f'{self.api_root}/{number}/math')
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print("Numbers.math(): Exception:", e)

    def trivia(self, number):
        """
        Return a random trivia about a number
        :return: str
        """
        print(f"Numbers.trivia(): General trivia about {number}")
        try:
            r = requests.get(f'{self.api_root}/{number}')
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print("Numbers.trivia(): Exception:", e)

    def year(self, year):
        pass

    def date(self, date):
        """
        Return a random trivia about a date
        :return: str
        """
        print(f"Numbers.date(): Trivia about {date}")
        try:
            r = requests.get(f'{self.api_root}/{date}/date')
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print("Numbers.date(): Exception:", e)

    def today(self):
        today_date = get_today("%m/%d")
        return self.date(today_date)

    def response(self):
        if self.query:
            if self.query.isdigit():
                self.response_msg = self.trivia(self.query)
                self.response_msg += "\n"
                self.response_msg += self.math(self.query)
            elif is_date(self.query):
                self.response_msg = self.date(self.query)
            elif self.query == "today":
                self.response_msg = self.today()
            elif self.query == "random":
                self.response_msg = self.random()
        else:
            self.response_msg = self.random()
        return self.response_msg
