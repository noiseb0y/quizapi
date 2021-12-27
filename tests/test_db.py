# from inspect import ClassFoundException
import fakeredis
import unittest
from application import db

class Test_test_connection(unittest.TestCase):
    def setUp(self) -> None:
        self.r = fakeredis.FakeRedis()
        
    def test_connection_OK(self):
        self.r.connected = True
        self.assertEqual(db.test_connection(self.r),None)
    
    def test_connection_BAD(self):
        self.r.connected = False
        self.assertRaises(Exception, db.test_connection(self.r)) 
        
class Test_is_shit_question(unittest.TestCase):
    def test_shit_question_true(self):
        self.question = """{\"question\": {\"questionId\": 361776, \"category\": \"fill in the state\", 
        \"value\": \"600\", \"question\": \"A blues-rock quartet:  ____ Shakes\", \"answer\": \"Alabama\"}, 
        \"timesPresented\": 0, \"shitQuestion\": true}"""
        self.assertTrue(db.is_shit_question(self.question))
        
    def test_shit_question_false(self):
        self.question = """{\"question\": {\"questionId\": 361776, \"category\": \"fill in the state\", 
        \"value\": \"600\", \"question\": \"A blues-rock quartet:  ____ Shakes\", \"answer\": \"Alabama\"}, 
        \"timesPresented\": 0, \"shitQuestion\": false}"""
        self.assertFalse(db.is_shit_question(self.question))
    
class Test_report_shit_question(unittest.TestCase):

    def setUp(self) -> None:
        self.r = fakeredis.FakeRedis()
        self.question = """{\"question\": {\"questionId\": 361776, \"category\": \"fill in the state\", 
        \"value\": \"600\", \"question\": \"A blues-rock quartet:  ____ Shakes\", \"answer\": \"Alabama\"}, 
        \"timesPresented\": 0, \"shitQuestion\": false}"""
        self.r.set("361776", self.question) 
        
    def test_report_shit_question_ok(self):
        import json
        db.report_shit_question(self.r, "361776")
        self.assertEqual(json.loads(self.r.get("361776"))["shitQuestion"], True, "awesome!")
        
        

if __name__ == "__main__":
    unittest.main()
