import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('postgres:435s606S@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            
        
        
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEquals(res.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertTrue(data['categories'])

    def test_404_get_nonexisting_category(self):
        res = self.client().get('/categories/100')
        data = json.loads(res.data)
        
        self.assertEquals(res.status_code, 404)
        self.assertEquals(data['success'],False)
        self.assertEqual(data['message'], "Resource Not Found")
    
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEquals(res.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertEquals(data['current_category'], None)
        
    def test_404_get_non_existing_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        
        self.assertEquals(res.status_code, 404)
        self.assertEquals(data['success'],False)
        self.assertEqual(data['message'], "Resource Not Found")
        
    def test_delete_quesiton(self):
        # insert a question to delete
        test_question = Question('question', 'answer', '1','1')
        test_question.insert()
        id = test_question.id
        
        
        res = self.client().delete('/questions/' + str(id))
        data = json.loads(res.data)
        #check is question still exists
        question = Question.query.filter(Question.id == id).one_or_none()
        
        self.assertEquals(res.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertTrue(data['deleted'], '10')
        self.assertEqual(question, None)
    
    
        
    def test_404_delete_non_existing_question(self):
        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)
        
        self.assertEquals(res.status_code, 404)
        self.assertEquals(data['success'],False)
        self.assertEqual(data['message'], "Resource Not Found")
        
    def test_create_question(self):
        self.new_question = {
            'question': 'question',
            'answer': 'answer',
            'category': '1',
            'difficulty': 1
            }
        
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEquals(res.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        
    def test_400_create_question_with_no_input(self):
        self.bad_question_no_input = {
            'question': '',
            'answer': '',
            'category': '',
            'difficulty': ''
            }
        
        res = self.client().post('/questions', json= self.bad_question_no_input)
        data = json.loads(res.data)
        
        self.assertEquals(res.status_code, 400)
        self.assertEquals(data['success'],False)
        self.assertEqual(data['message'], "Bad Request")
        
    def test_422_create_question_with_wrong_data_fields(self):
        self.bad_question_wrong_input = {
            'question': 123,
            'answer': 123,
            'category': 'String',
            'difficulty': 'String'
            }
        
        res = self.client().post('/questions', json= self.bad_question_wrong_input)
        data = json.loads(res.data)
        
        self.assertEquals(res.status_code, 422)
        self.assertEquals(data['success'],False)
        self.assertEqual(data['message'], "Unprocessable Entity")
        
    def test_search_question(self):
        self.search_tag = {'searchTerm': 'String'}
        res = self.client().post('/questions/search', json=self.search_tag)
        data = json.loads(res.data)
        
        self.assertEquals(res.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertTrue(['questions'])
        self.assertTrue(['questions'])
        self.assertEquals(data['current_category'], None)
     
    def test_400_search_question_bad_request(self):
        self.search_tag = {}
        
        res = self.client().post('/questions/search', json=self.search_tag)
        data = json.loads(res.data)
        
        self.assertEquals(res.status_code, 400)
        self.assertEquals(data['success'],False)
        self.assertEqual(data['message'], "Bad Request")
    
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        
        self.assertEquals(res.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEquals(data['current_category'], 'Art')
        
    def test_404_questions_by_nonexistant_category(self):
        res = self.client().get('/categories/a/questions')
        data = json.loads(res.data)
        
        self.assertEquals(res.status_code, 404)
        self.assertEquals(data['success'],False)
        self.assertEqual(data['message'], "Resource Not Found")
            
        
    def test_play_quiz(self):
        self.body = {
            'previous_questions' : [],
            'quiz_category': {'type': 'Art', 'id': 1}
            }
        
        res = self.client().post('/quizzes', json=self.body)
        data = json.loads(res.data)
        
        self.assertEquals(res.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertTrue(data['question'])
        
    def test_400_play_quiz_no_json(self):
        self.body = {}
        
        res = self.client().post('/quizzes', json=self.body)
        data = json.loads(res.data)
        
        self.assertEquals(res.status_code, 400)
        self.assertEquals(data['success'],False)
        self.assertEqual(data['message'], "Bad Request")
        
        
        
    def test_404_play_quiz_no_category(self):
        self.body = {
            'previous_questions' : [],
            'quiz_category': {}
            }
        
        res = self.client().post('/quizzes', json=self.body)
        data = json.loads(res.data)
        
        self.assertEquals(res.status_code, 404)
        self.assertEquals(data['success'],False)
        self.assertEqual(data['message'], "Resource Not Found")
        
    
        
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()