import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

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
  setup_db(app)
  CORS(app, resources={r"/api/*": {"origins": "*"}})
  
  
  

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
      response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
      return response
      
      
  @app.route('/')
  def home():
      return jsonify({
          'success': True
          })
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories', methods=['GET'])
  def get_categories():
      categories = Category.query.all()
      formatted_categories = {category.id: category.type for category in categories}
      
      if len(formatted_categories) == 0:
          abort(404)
      
      return jsonify({
          'success': True,
          'categories': formatted_categories
          })
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  
  @app.route('/questions', methods=['GET'])
  def get_questions():
      selection = Question.query.all()
      questions = [question.format() for question in selection]
      formatted_questions = paginate_questions(request, selection)
      categories = Category.query.all()
      formatted_categories = {category. id: category.type for category in categories}
     
      if len(formatted_questions) == 0:
          abort(404)
    
      return jsonify({
        'success': True,
        'questions': formatted_questions,
        'total_questions': len(questions),
        'categories' : formatted_categories,
        'current_category': None   
        })
  

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
      
      question_to_delete = Question.query.filter(Question.id == id).one_or_none()
      
      if not question_to_delete:
          abort(404)
      
      try:
          question_to_delete.delete()
          
          return jsonify({
              'success': True,
              'deleted':id
              })
              
      except:
          abort(422)
      
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
      body = request.get_json()
      
      if body.get('question') == '' or body.get('answer') == '' or body.get('difficulty') == '' or body.get('category') == '':
          abort(400)
          
      new_question = body.get('question')
      new_answer =  body.get('answer')
      new_category = body.get('category')
      new_difficulty = body.get('difficulty')
      
      try:
          new_question = Question(question = new_question, answer= new_answer, category = new_category,
                              difficulty = new_difficulty)
          new_question.insert()
          
          selection = Question.query.all()
          formatted_questions = paginate_questions(request, selection)
          
          return jsonify({
              'success': True,
              'created':new_question.id,
              'questions':formatted_questions,
              'total_questions':len(selection)
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
      tag = request.get_json()
      
      if not tag.get('searchTerm'):
          abort(400)
          
      search = "%" + tag.get('searchTerm', None) +"%"
      
      try:
          questions_query = Question.query.filter(Question.question.ilike(search)).all()
          formatted_questions = [question.format() for question in questions_query]
          
          return jsonify({
              'success': True,
              'questions': formatted_questions,
              'total_questions': len(formatted_questions),
              'current_category': None
              })
      except:
          abort(422)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions_by_category(id):
      
      
      if not id:
          abort(400)
     
      category = Category.query.filter(Category.id == id).first()
      if not category:
          abort(404)
          
      try:
          questions = Question.query.filter(Question.category == category.id).all()
          formatted_questions = [question.format() for question in questions]
          
          return jsonify({
              'success': True,
              'questions': formatted_questions,
              'total_questions': len(formatted_questions),
              'current_category': category.type
              })
      except:
          abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
      body = request.get_json()
      
      if not body:
          abort(400)
          
      quiz_category = body.get('quiz_category')
      previous_questions = body.get('previous_questions')
      
      if not (quiz_category or previous_questions):
          abort(404)
      try: 
          if quiz_category['type'] == 'click':
            questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
          else:
            questions = Question.query.filter(Question.category == int(quiz_category['id']),
                                            Question.id.notin_(previous_questions)).all()
          
          formatted_questions = [question.format() for question in questions]    
          if formatted_questions:
            quiz_question = formatted_questions[random.randint(0, len(formatted_questions) - 1)]
          else:
            quiz_question = None
                   
          return jsonify({
            'success': True,
            'question': quiz_question
                })
      except:
          abort(422)
      
      
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def not_found(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad Request"
        }), 400
    
  @app.errorhandler(404)
  def bad_request(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Resource Not Found"
        }), 404
    
  @app.errorhandler(422)
  def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Unprocessable Entity"
        }), 422
    
  @app.errorhandler(500)
  def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "Internal Server Error"
        }), 500  
  
  return app

    