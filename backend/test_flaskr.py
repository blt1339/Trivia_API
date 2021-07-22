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
        self.database_path = "postgres://{}:{}@{}/{}".format('student', 'student','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
        self.new_question = {
            'question': 'Who is the best catcher of all time?',
            'answer': 'Johnny Bench',
            'difficulty': 3,
            'category': '6'
        }


    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    # Test categories success
    def test_get_categories(self):

        # Get response and load the data
        res = self.client().get('/categories')
        data = json.loads(res.data)

        # Validate the response data 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))


    # Test question pagination success
    def test_get_paginated_questions(self):

        # Get response and load the data        
        res = self.client().get('/questions')
        data = json.loads(res.data)

        # Validate the response data 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    # Test invalid pagination - Eror 404
    def test_404_sent_requesting_beyond_valid_page(self):

        # Get response and load the data        
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        # Validate the response data 
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test delete success
    def test_delete_question(self):

        # Get response and load the data
        res = self.client().delete('/questions/13')
        data = json.loads(res.data)

        # Try to get the deleted question
        question = Question.query.filter(Question.id == 13).one_or_none()

        # Validate the response data 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)
        
    # Test invalid delete - Eror 422
    def test_422_if_question_does_not_exist(self):

        # Get response and load the data        
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        # Validate the response data 
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')    

    # Test new question success
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        # Validate the response data 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))

    # Test invalid new question - Error 422
    def test_422_if_question_creation_not_allowed(self):

        # Get response and load the data        
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        # Validate the response data 
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Test search success
    def test_get_question_search_with_results(self):

        # Get response and load the data        
        res = self.client().post('/questions/search', json={'searchTerm': 'Who'})
        data = json.loads(res.data)

        # Validate the response data 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 4)
    
    # Test search with no results
    def test_get_question_search_without_results(self):

        # Get response and load the data        
        res = self.client().post('/questions/search', json={'searchTerm': 'xxx'})
        data = json.loads(res.data)

        # Validate the response data 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)

    # Test list for a category success
    def test_get_question_category_with_results(self):

        # Get response and load the data
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        # Validate the response data  
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 3)
    
    # Test invalid list for a category - Error 404
    def test_get_question_category_without_results(self):

        # Get response and load the data
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        # Validate the response data 
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test for quiz play question success
    def test_get_quiz_play_question_with_results(self):

        # Get response and load the data
        res = self.client().post('/quizzes',json={'previous_questions': [9],
                                'quiz_category': {'type': 'History', 'id': '4'}})
        data = json.loads(res.data)

        # Validate the response data 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 4)
        self.assertNotEqual(data['question']['id'], 9)

    # Test for invalid quiz play - Error 404
    def test_get_quiz_play_question_without_results(self):

        # Get response and load the data
        res = self.client().post('/quizzes',json={})
        data = json.loads(res.data)

        # Validate the response data
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

if __name__ == "__main__":
    unittest.main()