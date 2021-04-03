from app import db
from app.models.Category import Category
from app.models.Excel import ExcelColumn, ExcelRecord
import pandas as pd


# def create_entity(title: str, description: str = None) -> Entity:
#     entity = Entity(title=title, description=description)
#     entity.save()
#     return entity


def create_columns(category_id: int, title: str, description: str = None):
    column = ExcelColumn(category_id=category_id, title=title, description=description)
    column.save()
    return column


def store_records(batch_id: int, column_id: int, category_id: int, value):
    record = ExcelRecord(
        batch_id=batch_id,
        category_id=category_id,
        column_id=column_id,
        value=value)
    record.save()


class HandleExcel:
    df = None
    category = None

    def __init__(self, file_path, category: Category):
        self.df = pd.read_excel(file_path)
        self.category = category

    def store_columns(self):
        print(f"all coluns =={len(self.df.columns.to_list())}")
        for column in self.df.columns.to_list():
            create_columns(self.category.id, title=column, description="")

    def store_records(self):
        last_record = ExcelRecord.query.order_by(ExcelRecord.id.desc()).first()
        batch_id = 0 if not last_record else last_record.batch_id
        for row in self.df.itertuples():
            batch_id = batch_id + 1
            for key, column in enumerate(self.category.columns):
                store_records(batch_id=batch_id, column_id=column.id, category_id=self.category.id, value=row[key + 1])

    @staticmethod
    def handle_query(query):
        records = ExcelRecord.query.filter_by(**query)
        df = pd.read_sql(records.statement, db.session.bind)
        df.drop(['CREATED_AT', 'UPDATED_AT', 'category_id', 'id'], axis=1, inplace=True)
        records = []
        for batch, df_batch in df.groupby('batch_id'):
            if batch == 10: break
            df_batch.drop(['batch_id', 'column_id'], axis=1, inplace=True)
            records.append(df_batch.to_dict('list')['value'])
        return records
