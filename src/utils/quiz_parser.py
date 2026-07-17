import json


def parse_quiz(text):

    try:

        return json.loads(text)

    except json.JSONDecodeError:

        return []