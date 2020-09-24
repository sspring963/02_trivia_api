# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. 

## Tasks

There are `TODO` comments throughout project. Start by reading the READMEs in:

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

We recommend following the instructions in those files in order. This order will look familiar from our prior work in the course.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom. 

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. 

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency. 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. 

## API Reference

### Getting Started
-Base URL: This app can only be run locally and is not hosted as a base URL. The Backend app is hosted at http://127.0.0.1:5000/ 
-Authentication: This version does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

{
	'success': False,
        'error': 400,
        'message': "Bad Request"
}

The api will return three types when requests fail:
-400: Bad Request
-404: Not Found
-422: Unprocessable Entity

### Endpoints

GET '/categories'
- General: Fetches a dictionary of all categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Sample: curl http://127.0.0.1:5000/categories
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}

GET '/questions'
- General: Fetches a list of questions, a dictionary of categories, a number of questions, and current category defaulted to None. Questions are paginated in groups of ten.
- Request Arguments: None
- Sample: curl http://127.0.0.1:5000/questions

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }], 
  "success": true, 
  "total_questions": 2
}

DELETE '/questions/<int:id>'
-General: Deletes the question specified by id. Returns the id of the deleted question.
-Request arguments: Question id
-Sample: curl http://127.0.0.1:5000/questions/1 -X DELETE

{
      "deleted": 1, 
      "success": true
}

POST '/questions'
-General: Creates a new question that is added to Questions. Returns the new question id, new list of questions, and new total number of questions.
-Request arguments: answer, category, difficulty, question
-Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d "{ \"question\": \"What do fish breathe?\", \"answer\": \"water\", \"difficulty\": 1, \"category\": \"1\" }"

{
  "created": 55,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    }
  ],
  "success": true,
  "total_questions": 23
}


POST '/questions/search'
-General: Brings back a list of questions that contain the search term in the question. Returns current_category deafulted to None and total questions.
-Request arguments: searchTerm
-Sample: curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d "{ \"searchTerm\" : \"movie\"}"

{
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "success": true,
  "total_questions": 1
}

GET '/categories/<int:id>/questions'
- General: Brings back a list of questions based on category. Returns total questions and current category.
- Request arguments: Category id
- Sample: curl http://127.0.0.1:5000/categories/5/questions
{
  "current_category": "Entertainment",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}

POST '/quizzes'
- General: Returns a random question from one category or from all that was not a previous question
- Request arguments: previous_questions, quiz_category
- Sample: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d "{\"previous_questions\":[],\"quiz_category\":{\"type\":\"Geography\",\"id\":\"3\"}}" 

{
  "question": {
    "answer": "Lake Victoria", 
    "category": 3, 
    "difficulty": 2, 
    "id": 13, 
    "question": "What is the largest lake in Africa?"
  }, 
  "success": true
}

[View the README.md within ./frontend for more details.](./frontend/README.md)
