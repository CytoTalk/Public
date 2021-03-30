from app.models.Entity import Entity, EntityField, EntityRecord
import pandas as pd


def create_entity(title: str, description: str = None) -> Entity:
    entity = Entity(title=title, description=description)
    entity.save()
    return entity


def create_entity_field(entity_id: int, title: str, description: str = None) -> EntityField:
    field = EntityField(entity_id=entity_id, title=title, description=description)
    field.save()
    return field


def store_records(batch_id: str, field_id: int, value) -> EntityRecord:
    record = EntityRecord(
        batch_id=batch_id,
        entity_field_id=field_id,
        value=value)
    record.save()
    return record


class HandleExcel:
    df = None
    entity = None

    def __init__(self, file_path, project_title, project_description):
        self.df = pd.read_excel(file_path)
        self.entity = create_entity(title=project_title, description=project_description)

    def store_columns(self):
        for column in self.df.columns.to_list():
            create_entity_field(self.entity.id, title=column, description="Dummy data")

    def store_records(self):
        last_record = EntityRecord.query.order_by(EntityRecord.id.desc()).first()
        batch_id = 0 if not last_record else last_record.batch_id
        for row in self.df.itertuples():
            batch_id = batch_id + 1
            for key, column in enumerate(self.entity.fields):
                store_records(batch_id=batch_id, field_id=column.id, value=row[key])
