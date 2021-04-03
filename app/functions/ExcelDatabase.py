import pandas as pd


class ExcelDatabase:
    df: pd = None

    def __init__(self, file_path: str):
        self.df = pd.read_excel(file_path)

    def respond(self, result):
        return result.to_dict('records')

    def query(self, criteria: str):
        result = self.df.query(criteria)
        return self.respond(result)
