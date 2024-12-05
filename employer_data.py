from collections import defaultdict
from utils import fetch_json


class EmployerData:
    def __init__(self, queries, area=26):
        self.queries = queries
        self.area = area
        self.employer_scores = defaultdict(lambda: [0] * len(queries))

    def collect_employers(self):
        """Собирает данные о работодателях и подсчитывает баллы."""
        for query_index, query in enumerate(self.queries):
            seen_employers = set()
            vacancies = self._fetch_vacancies(query)

            for vacancy in vacancies:
                employer = vacancy["employer"]
                employer_id, employer_name = employer["id"], employer["name"]

                if employer_id not in seen_employers:
                    seen_employers.add(employer_id)
                    self.employer_scores[(employer_id, employer_name)][query_index] = 1

    def _fetch_vacancies(self, query):
        """Получает вакансии для конкретного запроса."""
        url = "https://api.hh.ru/vacancies"
        params = {"text": query, "area": self.area}
        return fetch_json(url, params).get("items", [])

    def get_scores(self):
        """Возвращает собранные данные с баллами работодателей."""
        return self.employer_scores
