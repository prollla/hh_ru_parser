import pandas as pd

class ExcelExporter:
    def __init__(self, output_file="employer_data_with_links.xlsx"):
        self.output_file = output_file

    def export(self, employer_scores, all_vacancies, queries):
        """Экспортирует данные в Excel."""
        # Первая таблица: Баллы
        scores_data = []
        for (employer_id, employer_name), scores in employer_scores.items():
            total_score = sum(scores)
            scores_data.append([employer_name, f"https://hh.ru/employer/{employer_id}"] + scores + [total_score])

        scores_columns = ["Работодатель", "Ссылка на работодателя"] + queries + ["Total"]
        df_scores = pd.DataFrame(scores_data, columns=scores_columns)

        # Вторая таблица: Вакансии
        df_vacancies = pd.DataFrame(all_vacancies)

        # Сохранение в Excel
        with pd.ExcelWriter(self.output_file) as writer:
            df_scores.to_excel(writer, sheet_name="Баллы", index=False)
            df_vacancies.to_excel(writer, sheet_name="Все вакансии", index=False)

        print(f"Результаты сохранены в файл: {self.output_file}")
