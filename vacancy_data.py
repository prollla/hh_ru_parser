from utils import fetch_json


class VacancyData:
    def __init__(self, employer_scores):
        self.employer_scores = employer_scores
        self.all_vacancies = []

    def collect_all_vacancies(self):
        for (employer_id, employer_name) in self.employer_scores.keys():
            vacancies = self._fetch_all_vacancies(employer_id)
            for vacancy in vacancies:
                self.all_vacancies.append({
                    "Работодатель": employer_name,
                    "Ссылка на работодателя": f"https://hh.ru/employer/{employer_id}",
                    "Название вакансии": vacancy["name"],
                    "Ссылка на вакансию": vacancy["alternate_url"],
                })

    def _fetch_all_vacancies(self, employer_id):
        url = "https://api.hh.ru/vacancies"
        params = {"employer_id": employer_id, "per_page": 100}
        vacancies = []
        page = 0

        while True:
            params["page"] = page
            data = fetch_json(url, params)
            vacancies.extend(data.get("items", []))

            if page >= data.get("pages", 1) - 1:
                break
            page += 1

        return vacancies

    def get_all_vacancies(self):
        return self.all_vacancies
