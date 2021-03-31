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


def store_records(batch_id: str, column_id: int, value):
    record = ExcelRecord(
        batch_id=batch_id,
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
        for column in self.df.columns.to_list():
            create_columns(self.category.id, title=column, description="")

    def store_records(self):
        last_record = ExcelRecord.query.order_by(ExcelRecord.id.desc()).first()
        batch_id = 0 if not last_record else last_record.batch_id
        for row in self.df.itertuples():
            batch_id = batch_id + 1
            for key, column in enumerate(self.category.columns):
                store_records(batch_id=batch_id, column_id=column.id, value=row[key])
