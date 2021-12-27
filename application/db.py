import redis
import json

def test_connection(r: redis.Redis) -> Exception:
    try:
        r.ping()
        print("connection OK")
    except:
        print("cannot connect to redis, something's fucked")

def is_db_populated(r: redis.Redis) -> Exception:
    if r.info("keyspace"):
        if r.info("keyspace")["db0"]["keys"] > 100000:
            print("db seems to be populated!")
            return True
    return False

def generate_data_for_redis():
    import csv
    import uuid
    import config
    
    rows = []
    with open(config.QUESTION_PATH, "r") as csv_file:
        quiz_file_reader = csv.DictReader(csv_file, delimiter=",")
        for row in quiz_file_reader:
            rows.append(json.dumps(
                {
                    "question": {
                        "questionId": uuid.uuid4(),
                        "category" :row["category"], 
                        "value": row["value"], 
                        "question": row["question"], 
                        "answer": row["answer"]
                    },
                    "timesPresented": 0,
                    "shitQuestion": False
                }))
    return rows
    
def init_db(r: redis.Redis) -> Exception:
    print("attempting to init db...")
    test_connection(r)
    if not is_db_populated(r):
        print("database is unpopulated... populating!")
        p = r.pipeline()
        for row in generate_data_for_redis():
            p.set(json.loads(row)["question"]["questionId"], row)
        p.execute()
        print(r.info("keyspace"))

def is_shit_question(question: str) -> bool:
    return True if json.loads(question)["shitQuestion"] == True else False

def get_random_question(r: redis.Redis) -> str:
    shitQuestion = True
    while shitQuestion:
        questionResp = r.get(r.randomkey())
        if is_shit_question(questionResp):
            print("got a shit question!")
            continue
        else:
            return questionResp
        
def get_question_by_id(question_id: str) -> str:
    #TODO: all of this
    return question_id
        
def report_shit_question(r: redis.Redis, question_id: str):
    resp = r.get(question_id)
    json_resp = json.loads(resp)
    json_resp["shitQuestion"] = True
    r.set(question_id, json.dumps(json_resp))
    return "ok"