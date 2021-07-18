# Backend - Full Stack Trivia API 
Trivia api is a web application that storage of trivia questions that can then be utilized to take a trivia quiz.

The app allows one to:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.
### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server
From within the backend directory

To run the server, execute:

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
#### Frontend
From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
The first time you run the tests, omit the dropdb command. 
## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 

#### GET /categories
- General:
    - Returns all of the cateories, success value, and total number of categories

- Sample: curl http://127.0.0.1:5000/categories
```
  "categories": {       
    "1": "Science",     
    "2": "Art",
    "3": "Geography",   
    "4": "History",     
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
```

#### GET /questions
- General:
    - Returns a list of question objects, success value, and total number of questions
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
    - Also returns list of categories and total number of questions


- Sample: curl http://127.0.0.1:5000/questions?page=2
```
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
      "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?"     
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as 
what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"    
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 19
```
#### GET /categories/<int:id>/questions
- General:
    - Gets questions for a category
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
    - Also returns the category being shown and total number of questions
- Sample: curl http://127.0.0.1:5000/categories/3/questions
```
  "current_category": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in 
Africa?"
    },
    {
      "answer": "The Palace of Versailles",    
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would 
you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in 
which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 19
```
#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, difficulty, & category
- Sample: curl http://127.0.0.1:5000/questions -X POST 
-H "Content-Type: application/json" -d '{ "question": "Who is the greatest catcher of all time?", "answer": "Johnny Bench", "difficulty": 3, "category": "6" }'
```
  "created": 27,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks 
his third straight Oscar nomination, in 1996?" 
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of 
her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"        
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
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
      "question": "Which country won the first 
ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",    
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in 
Africa?"
    },
    {
      "answer": "The Palace of Versailles",    
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would 
you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 21
```
#### DELETE  /questions/<int:id>
- General:
    - Deletes a question by id
- Sample: curl http://127.0.0.1:5000/questions/27 -X DELETE
```
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks 
his third straight Oscar nomination, in 1996?" 
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of 
her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"        
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
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
      "question": "Which country won the first 
ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",    
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in 
Africa?"
    },
    {
      "answer": "The Palace of Versailles",    
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would 
you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 20
```

#### POST /questions/search
- General:
    - Returns questions that has the search substring
    - Also returns the chosen category if one is chosen and the total questions with the search substring

 - Sample: curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Who"}'
```
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"        
    },
    {
      "answer": "George Washington Carver",    
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?" 
    }
  ],
  "success": true,
  "total_questions": 3
```
#### POST /quizzes
- General:
    - Allows users to play take a quiz.  The number of questions asked is 5 or if the number of questions inthe category is less than 5 than all of the questions for the category are utilized once.

- Sample: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [3], "quiz_category": {"type": "Sports", "id": "6"}}'
```
  "question": {
    "answer": "Uruguay",
    "category": 6,
    "difficulty": 4,
    "id": 11,
    "question": "Which country won the first ever 
soccer World Cup in 1930?"
  },
  "success": true
```
## Authors
- Beverly Thompson worked on the API and test script to integrate with the frontend
- Udacity provided the starter files for the project including the frontend