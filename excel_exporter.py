import pandas as pd


class ExcelExporter:
    def export(self, employer_scores, employer_vacancy_links, queries, filename="employer_data_with_links.xlsx"):
        columns = ["Имя работадателя", "Ссылка на него"]
        for query in queries:
            columns.append(f"{query}")
            columns.append(f"{query} Ссылка на вакансию")
        columns.append("TOTAL")
        data = []
        for (employer_id, employer_name), scores in employer_scores.items():
            row = [employer_name, f"https://hh.ru/employer/{employer_id}"]
            total_score = 0
            for query_index, score in enumerate(scores):
                row.append(score)
                vacancy_links = ", ".join(employer_vacancy_links[(employer_id, employer_name)][query_index])
                row.append(vacancy_links)
                total_score += score
            row.append(total_score)
            data.append(row)
        df = pd.DataFrame(data, columns=columns)
        with pd.ExcelWriter(filename) as writer:
            df.to_excel(writer, sheet_name="Вакансии", index=False)
