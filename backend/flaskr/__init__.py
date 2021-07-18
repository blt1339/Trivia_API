import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
CATEGORIES_PER_PAGE = 10

def paginate_categories(request,selection):
  start = (page - 1) * CATEGORIES_PER_PAGE
  end = start + CATEGORIES_PER_PAGE

  categories = [category.format() for category in selection]
  current_categories = categories[start:end]
  print(current_categories)
  dict_current_categories = {}
  for category in current_categories:

    dict_current_categories[category['id']] = category['type']
    
  return dict_current_categories

def paginate_questions(request,selection):
  page = request.args.get('page',1,type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
    
  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO:Done Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  @TODO:Done Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: Done 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def retrieve_categories():
    selection = Category.query.order_by(Category.id).all()
    
    # Define the categories for the drop down
    cat = Category.query.all()
    categories = {}
    for category in cat:
      categories[category.id] = category.type

    if len(categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories':categories,
      'total_categories':len(Category.query.all())
    })

  '''
  @TODO: Done
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: Done 
  At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def retrieve_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    # get all categories and add to dict
    categories = Category.query.all()
    categories_dict = {}
    for category in categories:
      categories_dict[category.id] = category.type
    
    if len(current_questions) == 0:
      abort(404)
    
    return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(Question.query.all()),
          'categories': categories_dict,
          'current_category': None
          })

  '''
  @TODO: Done
  Create an endpoint to DELETE question using a question ID. 

  TEST: Done
  When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    question = Question.query.filter(Question.id == question_id).one_or_none()

    if question is None:
      abort(422)

    try:
      question.delete()
      
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
      
      return jsonify({
        'success': True,
        'questions':current_questions,
        'total_questions':len(Question.query.all())
        })

    except:
      abort(422)
  '''
  @TODO: Done
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST:Done 
  When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)    
    # search = body.get('search', None)

    try:
      question = Question(question=new_question, answer=new_answer, category=new_category,difficulty=new_difficulty)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      })

    except:
      abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():


    body = request.get_json()
    search_term = body.get('searchTerm', None)
    
    if not search_term:
      abort(422)
    
    try:
      search_results = Question.query.filter(
        Question.question.ilike(f'%{search_term}%')).all()

      if not search_results:
        abort(422)

      paginated_questions = paginate_questions(request, search_results)
        
      return jsonify({
        'success': True,
        'questions': paginated_questions,
        'total_questions': len(search_results),
        'current_category': None
        })
    except:
      abort(422)
  '''
  @TODO: Done
  Create a GET endpoint to get questions based on category. 

  TEST: Done
  In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions_by_category(id):
    print(id)
    print('------------')
    # Get the category
    search_category = Category.query.filter(Category.id == int(id)).one_or_none()

    if search_category is None:
      abort(400)

    # Get the questions for the category
    #selection = Question.query.filter(Question.category == search_category.id).all()
    #selection = Question.query.filter(Question.category == id).all()
    selection = Question.query.filter_by(category=id).all()

    current_questions = paginate_questions(request, selection)

    # return the results
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'current_category': search_category.type
      })

  '''
  @TODO: Done
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_questions():
    quiz = request.get_json()
    quiz_previous_questions = quiz.get('previous_questions')
    quiz_category = quiz.get('quiz_category')

    questions_unasked = []

    if quiz_category['id'] == 0:
      quiz_questions = Question.query.all()
    else:
      quiz_questions = Question.query.filter_by(category=quiz_category['id']).all()

    if quiz_questions is None :
      abort(404)

    for question in quiz_questions:

      if question.id not in quiz_previous_questions:
        questions_unasked.append(question.format())
    
    # If there are no more questions than force it to end
    if len(questions_unasked) == 0:
      current_question = ''
    else:
      current_question = random.choice(questions_unasked)
    
    return jsonify({
      'success':True,
      'question':current_question
    })


  '''
  @TODO: Done
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error): 
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad Request"
        }), 400

  @app.errorhandler(404)
  def not_found(error): 
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
        }), 404

  @app.errorhandler(422)
  def unprocessable_entity(error): 
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

  return app

    