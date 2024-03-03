# API Documentation Final Project

## Trivia App

## Base path
http://localhost:5000

## Endpoints

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

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

`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "total_questions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "History"
}
```

---

`GET '/categories/${id}/questions'`

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: `id` - integer
- Returns: An object with questions for the specified category, total questions, and current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "total_questions": 100,
  "current_category": "History"
}
```

---

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.

---

`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

```json
{
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
 }
```

- Returns: a single new question object

```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
}
```

---

`POST '/questions'`

- Sends a post request in order to add a new question
- Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

- Returns: Does not return any new data

---

`POST '/questions'`

- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```

- Returns: any array of questions, a number of total_questions that met the search term and the current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "total_questions": 100,
  "current_category": "Entertainment"
}
```

## Error Handling

- Error code 400:
```json
{
            "success": False,
            'error': 400,
            "message": "Bad request"
}
```

- Error code 404:
```json
{
            "success": False,
            'error': 404,
            "message": "Page not found"
}
```

- Error code 422:
```json
{
            "success": False,
            'error': 422,
            "message": "Unprocessable resource"
}
```

- Error code 500:
```json
{
            "success": False,
            'error': 500,
            "message": "Internal server error"
}
```

- Error code 405:
```json
{
            "success": False,
            'error': 405,
            "message": "Invalid method!"
}
```