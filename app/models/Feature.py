import re
from sqlalchemy.orm.attributes import flag_modified

from app import db
from app.models.BaseModel import BaseModel
from sqlalchemy.dialects.postgresql import JSON

DATA_TYPES_MAPPER = {
    "String": {
        "SQL": "VARCHAR",
        "HTML": "text",
        "PYTHON": 'str'
    },
    "Integer": {
        "SQL": "INTEGER",
        "HTML": "number",
        "PYTHON": 'int'
    },
    "Boolean": {
        "SQL": "BOOLEAN",
        "HTML": "checkbox",
        "PYTHON": 'bool'
    },
    "Float": {
        "SQL": "FLOAT",
        "HTML": "number",
        "PYTHON": 'float'
    },
    "Picture": {
        "SQL": "VARCHAR",
        "HTML": "file",
        "PYTHON": 'str'
    },
}


def clean_column(column_name) -> str:
    return re.sub(r'\W+', ' ', column_name).lower().replace(" ", "_")


class Feature(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    subproject_id = db.Column(db.Integer, db.ForeignKey('sub_project.id'))
    columns = db.Column(JSON, default={"columns": []})
    store_table_name = f"feature_table_{id}"

    def save(self):
        db.session.add(self)
        flag_modified(self, "columns")
        db.session.commit()

    def make_db(self):
        sql = f" CREATE TABLE feature_table_{self.id} (\
            i_d serial PRIMARY KEY);"
        db.engine.execute(sql)

    def delete(self):
        sql = f'DROP TABLE if exists feature_table_{self.id};'
        db.engine.execute(sql)
        db.session.delete(self)
        db.session.commit()

    def add_column(self, column_name: str, data_type: str, description: str):
        name = clean_column(column_name)
        if not name:
            raise Exception(f"The column name [{name}] is invalid")
        sql = f"ALTER TABLE feature_table_{self.id} ADD COLUMN {name} \
        {DATA_TYPES_MAPPER[data_type]['SQL']}"

        db.engine.execute(sql)
        self.columns['columns'].append(
            {
                "column_name": name,
                "original_name": column_name,
                "description": description,
                "data_type": DATA_TYPES_MAPPER[data_type]
            })
        self.save()

    def delete_column(self, column_name):
        sql = f"ALTER TABLE feature_table_{self.id} DROP COLUMN if exists {column_name};"
        db.engine.execute(sql)
        new_columns = [item for item in self.columns['columns'] if item['column_name'] != column_name]
        self.columns['columns'] = new_columns
        self.save()

    def rename_column(self, column_name: str, new_name: str):
        sql = f"ALTER TABLE feature_table_{self.id}  RENAME COLUMN {column_name} TO {new_name};"
        db.engine.execute(sql)

    def get_column_data(self, column_name):
        return [x for x in self.columns['columns'] if x['column_name'] == column_name][0]

    def update_column(self, column_name, new_name, description):
        for column in self.columns['columns']:
            if column['column_name'] == column_name:
                column['description'] = description
                column['original_name'] = new_name
        self.columns = self.columns
        self.save()

    @staticmethod
    def execute_query(sql):
        return db.engine.execute(sql)

    def fetch_records(self):
        sql = f"SELECT * FROM feature_table_{self.id} LIMIT 10;"
        res = db.engine.execute(sql)
        return res

    def column_keys(self) -> dict:
        return {x['column_name']: x for x in self.columns['columns']}
