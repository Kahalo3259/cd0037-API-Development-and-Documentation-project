import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, origins=['*'])

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow', 'Content-Type')

        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories_formatted = {}

        categories = Category.query.order_by(Category.id).all()

        """
        Loop through categories to create a dictionary of category IDs 
        where their values are the corresponding category type.
        """
        for category in categories:
            categories_formatted[category.id] = category.type

        return jsonify({
            'categories': categories_formatted
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.order_by(Question.id).all()

        """
        Determine the start and end indexes to paginate questions.
        """
        page = request.args.get('page', 1, type=int)

        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        """
        Create an array of questions where the indices are questions formatted into dictionaries.
        """
        questions_formatted = [question.format() for question in questions]

        category = request.args.get('category', None)

        categories_formatted = {}

        categories = Category.query.order_by(Category.id).all()

        """
        Loop through categories to create a dictionary of category IDs 
        where their values are the corresponding category type.
        """
        for category in categories:
            categories_formatted[category.id] = category.type

        return jsonify({
            'questions': questions_formatted[start:end],
            'total_questions': len(questions),
            'current_category': category.type,
            'categories': categories_formatted
        })
    """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.filter_by(id=id).one_or_none()

        """
        If the question does not exist, abort and respond with 404
        """
        if question is None:
            abort(404)

        question.delete()

        return jsonify({
            'deleted': id,
            'total_questions': len(Question.query.all())
        })
    """
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    """
    @app.route('/questions', methods=['POST'])  # Handles POST requests to /questions to determine if the request is to search or post a question.
    def handle_question():
        if 'searchTerm' not in request.get_json():
            return post_question()
        else:
            return search_question()

    def post_question():
        data = request.get_json()

        """
        If the question or answer is empty, abort response with 400.
        """
        if data['question'] == '' or data['answer'] == '':
            abort(400)

        """
        Create the question object.
        """
        question = Question(data['question'], data['answer'], data['category'], data['difficulty'])
        question.insert()

        return jsonify({
            'posted': question.id,
            'total_questions': len(Question.query.all())
        })
    """
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    """
    def search_question():
        data = request.get_json()

        questions = Question.query.filter(Question.question.contains(data['searchTerm']))

        questions_formatted = [question.format() for question in questions]

        """
        If there are no questions using the terms in search, abort response with 404.
        """
        if len(questions_formatted) == 0:
            abort(404)

        return jsonify({
            'questions': questions_formatted,
            'results': len(questions_formatted),
            'total_questions': len(Question.query.all())
        })
    """
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.
    """
    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_questions_by_category(id):
        """
        Run a query on the Question model using the category ID.
        """
        questions = Question.query.filter_by(category=id)

        questions_formatted = [question.format() for question in questions]

        """
        If there are no question with the category ID, abort response with 404.
        """
        if len(questions_formatted) == 0:
            abort(404)

        return jsonify({
            'category': Category.query.filter_by(id=id).one_or_none().type,
            'questions': questions_formatted,
            'results': len(questions_formatted),
            'total_questions': len(Question.query.all())
        })
    """
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        data = request.get_json()

        prev_questions = data['previous_questions']
        category_id = data['quiz_category']['id']

        category = Category.query.filter_by(id=category_id).one_or_none()

        """
        If there is no category, choose one at random.
        """
        if category is None:
            num_of_categories = len(Category.query.all())

            while category is None:
                category_id = random.randint(1, num_of_categories)
                category = Category.query.filter_by(id=category_id).one_or_none()

        questions = Question.query.filter_by(category=category.id).all()
        questions_remaining = len(questions)

        """
        Determine if there are any more questions left in the category.
        """
        for question in questions:
            if question.id in prev_questions:
                questions_remaining -= 1

        """
        If there are no more questions in the category, abort with 422.
        """
        if questions_remaining == 0:
            abort(422)

        index = 0

        try:
            question_id = prev_questions[len(prev_questions) - 1]
        except IndexError:
            question_id = None

        while question_id is None or question_id in prev_questions:
            index = random.randint(0, len(questions) - 1)
            question_id = questions[index].id

        question = questions[index]

        return jsonify({
            'question': question.format(),
            'category': category.format()
        })
    """
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 400,
            'message': 'Bad request!'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 404,
            'message': 'Resource was not found!'
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'error': 422,
            'message': 'Request could not be processed!'
        }), 422

    return app
