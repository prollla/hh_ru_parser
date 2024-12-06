import json
from employer_data import EmployerData
from excel_exporter import ExcelExporter


def load_config(config_file="input.json"):
    with open(config_file, "r") as file:
        return json.load(file)


def main():
    config = load_config()
    queries = config["queries"]
    area = config["area"]
    output_file = config["output_file"]
    employer_data = EmployerData(queries, area)
    employer_data.collect_employers()
    employer_scores, employer_vacancy_links = employer_data.get_scores()
    exporter = ExcelExporter()
    exporter.export(employer_scores, employer_vacancy_links, queries, output_file)


if __name__ == "__main__":
    main()
