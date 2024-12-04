from employer_data import EmployerData
from vacancy_data import VacancyData
from excel_exporter import ExcelExporter


def main():
    # Настройки
    queries = ["ASP.NET", "Vue", "React"]
    area = 26
    output_file = "employer_data_with_links.xlsx"

    # Шаг 1: Сбор данных о работодателях
    employer_data = EmployerData(queries, area)
    employer_data.collect_employers()
    employer_scores = employer_data.get_scores()

    # Шаг 2: Сбор всех вакансий
    vacancy_data = VacancyData(employer_scores)
    vacancy_data.collect_all_vacancies()
    all_vacancies = vacancy_data.get_all_vacancies()

    # Шаг 3: Экспорт данных в Excel
    exporter = ExcelExporter(output_file)
    exporter.export(employer_scores, all_vacancies, queries)


if __name__ == "__main__":
    main()
