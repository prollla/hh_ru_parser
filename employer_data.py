from collections import defaultdict
from utils import fetch_json


class EmployerData:
    def __init__(self, queries, areas):
        self.queries = queries
        self.areas = areas
        self.employer_scores = defaultdict(lambda: {area: [0] * len(queries) for area in areas})
        self.employer_vacancy_links = defaultdict(lambda: {area: [[] for _ in range(len(queries))] for area in areas})

    def collect_employers(self):
        for area in self.areas:
            for query_index, query in enumerate(self.queries):
                pages = self._fetch_pages(query, area)
                for page in range(pages):
                    vacancies = self._fetch_vacancies(query, area, page)
                    for vacancy in vacancies:
                        employer = vacancy["employer"]
                        employer_id, employer_name = employer["id"], employer["name"]
                        self.employer_scores[(employer_id, employer_name)][area][query_index] += 1
                        self.employer_vacancy_links[(employer_id, employer_name)][area][query_index].append(
                            vacancy["alternate_url"])

    def _fetch_pages(self, query, area):
        url = "https://api.hh.ru/vacancies"
        params = {"text": query, "area": area,
                  "per_page": 100}
        response = fetch_json(url, params)
        return response.get("pages", 1)

    def _fetch_vacancies(self, query, area, page):
        url = "https://api.hh.ru/vacancies"
        params = {"text": query, "area": area, "per_page": 100, "page": page}
        response = fetch_json(url, params)
        return response.get("items", [])

    def get_scores(self):
        return self.employer_scores, self.employer_vacancy_links


