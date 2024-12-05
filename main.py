import json
from employer_data import EmployerData
from vacancy_data import VacancyData
from excel_exporter import ExcelExporter


def load_settings(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        queries = data.get("queries", [])
        area = data.get("area")
        output_file = data.get("output_file", "employer_data_with_links.xlsx")

        if not queries or area is None:
            print("Ошибка: Проверьте, что файл содержит поля 'queries', 'area' и 'output_file'.")
            return [], None, None

        return queries, area, output_file
    except FileNotFoundError:
        print(f"Файл {file_path} не найден. Проверьте путь.")
        return [], None, None
    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON из файла {file_path}. Убедитесь, что формат корректен.")
        return [], None, None


def main():
    # Путь к JSON-файлу с настройками
    settings_file = "input.json"  # Укажите путь к вашему JSON-файлу

    # Загрузка параметров из файла
    queries, area, output_file = load_settings(settings_file)

    if not queries or area is None or not output_file:
        print("Не удалось загрузить настройки. Завершение работы.")
        return

    print(f"Параметры загружены: запросы={queries}, регион={area}, файл вывода={output_file}")

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

