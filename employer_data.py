from collections import defaultdict
from utils import fetch_json


class EmployerData:
    def __init__(self, queries, area):
        self.queries = queries
        self.area = area
        self.employer_scores = defaultdict(lambda: [0] * len(queries))
        self.employer_vacancy_links = defaultdict(lambda: [[] for _ in range(len(queries))])

    def collect_employers(self):
        for query_index, query in enumerate(self.queries):
            vacancies = self._fetch_vacancies(query)

            for vacancy in vacancies:
                employer = vacancy["employer"]
                employer_id, employer_name = employer["id"], employer["name"]
                self.employer_scores[(employer_id, employer_name)][query_index] += 1
                self.employer_vacancy_links[(employer_id, employer_name)][query_index].append(vacancy["alternate_url"])

    def _fetch_vacancies(self, query):
        url = "https://api.hh.ru/vacancies"
        params = {"text": query, "area": self.area}
        return fetch_json(url, params).get("items", [])

    def get_scores(self):
        return self.employer_scores, self.employer_vacancy_links
