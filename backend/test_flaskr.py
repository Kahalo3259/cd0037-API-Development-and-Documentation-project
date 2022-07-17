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
        self.database_path = "postgresql://postgres:@{}/{}".format('localhost:5432', self.database_name)
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(data['current_category'])
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)

    def test_post_question(self):
        res = self.client().post('/questions', json={'question': 'test', 'answer': 'test', 'category': 1, 'difficulty': 3})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['total_questions'], len(Question.query.all()))

    def test_delete_question(self):
        last = Question.query.order_by(Question.id.desc()).first().id
        res = self.client().delete('/questions/' + str(last))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(data['deleted'], last)
        self.assertEqual(data['total_questions'], len(Question.query.all()))

    def test_search_with_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), len(Question.query.filter(Question.question.contains('title')).all()))
        self.assertEqual(data['results'], len(Question.query.filter(Question.question.contains('title')).all()))
        self.assertEqual(data['total_questions'], len(Question.query.all()))

    def test_search_without_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'magical'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), len(Question.query.filter_by(category=3).all()))
        self.assertTrue(data['results'])
        self.assertEqual(data['results'], len(Question.query.filter_by(category=3).all()))
        self.assertEqual(data['total_questions'], len(Question.query.all()))

    """
    Test to attempt to upload an invalid question.
    """
    def test_post_question_400(self):
        res = self.client().post('/questions', json={'question': '', 'answer': '', 'category': 1, 'difficulty': 3})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    """
    Simulate quiz using a selected category.
    """
    def test_quiz_by_category(self):
        id = 3
        type = Category.query.filter_by(id=id).one_or_none().type
        turns = len(Question.query.filter_by(category=id).all())

        previous_questions = []

        while turns > 0:
            res = self.client().post('/quizzes', json={'previous_questions': previous_questions, 'quiz_category': {'type': type, 'id': id}})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['question'])
            self.assertTrue(data['category'])

            previous_questions.append(data['question']['id'])
            turns -= 1

    """
    Simulate a quiz selecting random.
    """
    def test_random_quiz(self):
        turns = 5

        previous_questions = []

        while turns > 0:
            res = self.client().post('/quizzes', json={'previous_questions': previous_questions, 'quiz_category': {'type': '', 'id': 0}})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['question'])
            self.assertTrue(data['category'])

            previous_questions.append(data['question']['id'])
            turns -= 1

    """
    Simulate a quiz where a category is selected, and the turns are more than the available number of questions.
    """
    def test_quiz_422(self):
        id = 3
        type = Category.query.filter_by(id=id).one_or_none().type
        turns = len(Question.query.filter_by(category=id).all())

        previous_questions = []

        while turns > 0:
            res = self.client().post('/quizzes', json={'previous_questions': previous_questions,
                                                       'quiz_category': {'type': type, 'id': id}})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['question'])
            self.assertTrue(data['category'])

            previous_questions.append(data['question']['id'])
            turns -= 1

        res = self.client().post('/quizzes', json={'previous_questions': previous_questions, 'quiz_category': {'type': type, 'id': id}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()