import pandas as pd


class ExcelExporter:
    def export(self, employer_scores, employer_vacancy_links, queries, areas, filename):
        columns = ["Имя работадателя", "Ссылка на него"]
        for area in areas:
            for query in queries:
                columns.append(f"{query} ({area})")
                columns.append(f"{query} ({area}) Ссылки на вакансии")
        columns.append("TOTAL")
        data = []
        for (employer_id, employer_name), scores_by_area in employer_scores.items():
            row = [employer_name, f"https://hh.ru/employer/{employer_id}"]
            total_score = 0
            for area in areas:
                for query_index, query in enumerate(queries):
                    score = scores_by_area[area][query_index]
                    vacancy_links = ", ".join(employer_vacancy_links[(employer_id, employer_name)][area][query_index])

                    # Заполняем ячейки
                    row.append(score)
                    row.append(vacancy_links)
                    total_score += score
            row.append(total_score)
            data.append(row)
        df = pd.DataFrame(data, columns=columns)
        with pd.ExcelWriter(filename) as writer:
            df.to_excel(writer, sheet_name="Вакансии", index=False)
