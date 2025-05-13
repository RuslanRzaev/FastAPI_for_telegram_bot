import json
from sqlalchemy.engine import Result

def result_to_json(result: Result):
    result = [dict(row) for row in result.fetchall()]
    return json.dumps(result)