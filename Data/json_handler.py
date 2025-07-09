import json


def get_db_config():
    with open("config.json", "r", encoding="utf-8") as js:
        config = json.load(js)
    user = config['user']
    password = config["password"]
    host = config["host"]
    database = config["database"]
    query = "SELECT * FROM complaints"
    return user, password, host, database, query