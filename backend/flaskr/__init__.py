import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from dotenv import load_dotenv
import werkzeug
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    load_dotenv()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        "SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv(
        "SQLALCHEMY_TRACK_MODIFICATIONS")
    app.app_context().push()
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=['GET'])
    def getCategories():
        try:
            categories = Category.query.all()
            formatted_categories = {
                category.id: category.type for category in categories}

            # Check if there are no categories
            if categories is None:
                abort(404)
            return jsonify({
                'success': True,
                'categories': formatted_categories
            })
        except Exception as error:
            print(error)
            abort(500)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def getQuestions():
        try:
            # Retrieve all questions
            selection = Question.query.order_by(Question.id).all()

            # Paginate questions
            selected_questions = paginate_questions(request, selection)

            # Check if there are no questions in the current page
            if not selected_questions:
                abort(404)

            # Retrieve total number of questions
            total_questions = len(selection)

            # Retrieve all categories
            all_categories = Category.query.all()
            formatted_categories = {
                category.id: category.type for category in all_categories}

            return jsonify({
                'success': True,
                'questions': selected_questions,
                'total_questions': total_questions,
                'categories': formatted_categories
            })

        except Exception as error:
            print(error)
            abort(400)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:Q_id>', methods=['DELETE'])
    def deleteQuestion(Q_id):
        try:
            # Retrieve the question by ID
            deleted_question = Question.query.get(Q_id)

            # Check if the question donesn't exists
            if deleted_question is None:
                abort(404)

            # Delete the question
            deleted_question.delete()

            return jsonify({
                'success': True,
                'questions_id': deleted_question.id
            })

        except Exception as error:
            print(error)
            abort(404)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=['POST'])
    def newQuestion():
        try:
            # Extracting data from the request JSON
            body = request.get_json()
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_category = body.get('category', None)
            new_difficulty = body.get('difficulty', None)

            # Check if any of the required fields is missing
            if any(value is None for value in [body, new_question, new_answer, new_category, new_difficulty]):
                abort(422)

            # Create a new Question instance
            new_question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty
            )

            # Insert the new question into the database
            new_question.insert()

            # Retrieve the updated list of questions after insertion
            all_questions = Question.query.order_by(Question.id).all()
            paginated_questions = paginate_questions(request, all_questions)

            return jsonify({
                'success': True,
                'created': new_question.id,
                'questions': paginated_questions,
                'total_questions': len(all_questions)
            })

        except Exception as error:
            print(error)
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/search", methods=['POST'])
    def searchQuestions():
        try:
            # Extracting search term from the request JSON
            body = request.get_json()
            search_term = body.get('searchTerm')

            # Querying questions that match the search term using case-insensitive comparison
            matching_questions = Question.query.filter(
                Question.question.ilike(f'%'+search_term+'%')).all()

            if matching_questions:
                paginated_questions = paginate_questions(
                    request, matching_questions)

                return jsonify({
                    'success': True,
                    'questions': paginated_questions,
                    'total_questions': len(matching_questions)
                })
            else:
                abort(404)
        except werkzeug.exceptions.NotFound:
            abort(404)
        except Exception as error:
            print(error)
            abort(500)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:C_id>/questions")
    def questionsinCategory(C_id):
        try:
            # Check if the category with the specified ID exists
            category = Question.query.filter_by(category=C_id).all()
            if len(category) > 0:
                # Query questions in the specified category
                questions_in_category = Question.query.filter_by(
                    category=C_id).all()
                # Paginate the questions in the category
                paginated_questions = paginate_questions(
                    request, questions_in_category)
                print('in ')
                category_type = Category.query.get(C_id).type

                return jsonify({
                    'success': True,
                    'questions': paginated_questions,
                    'total_questions': len(questions_in_category),
                    'current_category': category_type
                })
            else:
                abort(404)
        except werkzeug.exceptions.NotFound:
            abort(404)
        except Exception as error:
            print(error)
            abort(500)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def start_quiz():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')
            tempQuestList = []
            
            for q in previous_questions:
                tempQuestList.append(Question.query.get(q).question)
            #print(tempQuestList)
            # Check if the quiz_category is missing
            if not quiz_category:
                abort(422)
            # Determine the questions based on the quiz category
            if quiz_category['id'] == 0 :
                category_id = int(quiz_category['id']) 
                questions = Question.query.filter(
                    Question.question.not_in(tempQuestList)
                ).all()
                #print (questions)
            else:
                category_id = int(quiz_category['id'])
                questions = Question.query.filter(
                    Question.category == category_id,
                    Question.question.not_in(tempQuestList) 
                ).all()
                

            # Select a random question from the filtered set
            selected_question = random.choice(
                questions).format() if questions else None
          

            return jsonify({
                'success': True,
                'question': selected_question
            })

        except Exception as error:
            print(error)
            abort(404)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            'error': 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "success": False,
            'error': 404,
            "message": "Page not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_resource(error):
        return jsonify({
            "success": False,
            'error': 422,
            "message": "Unprocessable resource"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "Internal server error"
        }), 500

    @app.errorhandler(405)
    def invalid_method(error):
        return jsonify({
            "success": False,
            'error': 405,
            "message": "Invalid method!"
        }), 405

    return app
