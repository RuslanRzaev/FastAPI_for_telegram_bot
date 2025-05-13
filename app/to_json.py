import json
from sqlalchemy.engine import Result
from sqlalchemy.orm import class_mapper


def obj_to_dict(obj):
    return {column.name: getattr(obj, column.name)
            for column in class_mapper(obj.__class__).columns}


def result_to_json(result):
    result_list = [obj_to_dict(row) for row in result.fetchall()]
    return json.loads(json.dumps(result_list, ensure_ascii=False))