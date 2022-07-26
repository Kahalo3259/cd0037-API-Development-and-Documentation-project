# Trivia API

## Welcome

Welcome to my Trivia API application! This repo was forked from the original repo to complete the Udacity "API Development and Documentation" course. Below you will see what calls you can access and what to expect in the response.

## Getting Started

To get started using the Trivia API, you must first install the dependencies. To do this, you can run the following command while in your virtual environment for Python. Make sure you are using Python 3.7+:

```bash
pip install -r requirements.txt
```

Once completed, you can setup the database. The following example is done using Postgres:
```bash
createdb trivia
```

Then insert the included .psql script into the database:
```bash
psql trivia < trivia.psql
```

Finally, to run the flask server, run:
```bash
flask run
```

Now you can run queries to the host:port that flask is running on to interact with the Trivia API!

### Endpoints & Responses

Here are the endpoints that you are able to run queries on and what the expected responses should be:

`GET /categories`

- Retrieve ALL categories as a json dictionary.

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }
}
```

---

`GET /questions?page=<int:page_number>`

- Retrieve ALL questions as a json dictionary, in addition to the total number of questions, the current selected category, and ALL categories in a similar format to `/categories` GET request. Results will display in pages of 10 by default.
- Parameters - Page number as an integer

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "Sports", 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    ...
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "total_questions": 18
}
```

---

`DELETE /questions/<int:id>`

- Delete a question with the specified ID. Returns the ID of the deleted question and the new total number of questions.
- Parameters - Question ID

```json
{
  "deleted": 25,
  "total_questions": 14
}
```

---

`POST /questions`

- Add a new question by sending the question, answer, difficulty & category. Returns the new question & the new total number of answers. If either the question or answer are empty, it will return 400.

- Request Body
```json
{
  "question": "Example Question",
  "answer": "Example Answer",
  "difficulty": 3,
  "category": 3
}
```

- Response Body
```json
{
  "posted": 25,
  "total_questions": 22
}
```

---

`POST /questions`

- Search for a question by sending a search term. Returns the questions matching the search term, total results & the total number of questions overall.

- Request Body
```json
{
  "searchTerm": "title",
}
```

- Response Body
```json
{
  "questions": [
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
    }
  ],
  "results": 2,
  "total_questions": 18
}
```

---

`GET /categories/<int:id>/questions`

- Retrieve all questions in the specified category using the category ID as the variable. Also includes the category being queried, the total number of results & the total questions overall.

```json
{
  "category": "History", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ], 
  "results": 4, 
  "total_questions": 18
}
```

---

`POST /quizzes`

- Retrieves a question base on the category & previous questions. If the category sent is 0, the API will choose a category at random. If the quiz is not random and the category has exhausted all questions before the turns for the quiz are complete, it will return 422.

- Request Body
```json
{
  "previous_questions": [3, 2, 5, 9],
  "quiz_category": 0
}
```

- Response Body
```json
{
  "question":
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
  "category":
    {
      "id": 4,
      "type": "History"
    }
}
```
