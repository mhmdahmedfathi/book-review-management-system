# Book Review and Management System

This is a Django-based web application that allows users to publish books, review books published by others, and manage their own books. The system includes features like book publishing, reviewing, updating, and deleting books, as well as pagination for listing books.

---

## Features

### Book Management
- **Publish a Book**: Authenticated users can publish a book by providing details such as title, author, description, and cover image.
- **List All Books**: Retrieve a list of all books published by users.
- **Retrieve a Specific Book**: Fetch details of a specific book by its ID.
- **Update a Book**: Users can update the details of books they have published.
- **Delete a Book**: Users can delete books they have published.

### Review and Comment System
- **Post a Review/Comment**: Users can post reviews or comments on books published by other users. They cannot review their own books.
- **List Reviews for a Book**: Retrieve all reviews for a specific book.
- **Edit a Review/Comment**: Users can edit their own reviews or comments.
- **Delete a Review/Comment**: Users can delete their own reviews or comments.

### Pagination
- The system supports pagination for listing books, making it easier to handle large datasets.

---

## Technologies Used
- **Backend**: Django, Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Authentication**: Django's built-in authentication system.
- **Pagination**: DRF's built-in pagination classes.

---

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- Django 4.0 or higher
- Django REST Framework

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mhmdahmedfathi/book-review-management-system.git
   cd book-review-management-system
   ```

### If you wish to use your machine to run this application, here is the steps:

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the API**:
   - Open your browser or use a tool like Postman to interact with the API.
   - The API will be available at `http://127.0.0.1:8000/`.

### If you wish to use docker to run this application:


2. **Build and Run the Docker Container**:
   ```bash
    docker compose up --build
    ```

3. **Access the API**:
    - Open your browser or use a tool like Postman to interact
    - The API will be available at `http://localhost:8000/`.
    
---

## API Endpoints

### Book Management
- **List All Books**: `GET /books/`
- **Publish a Book**: `POST /books/`
- **Retrieve a Specific Book**: `GET /books/<int:id>/`
- **Update a Book**: `PATCH /books/<int:id>/`
- **Delete a Book**: `DELETE /books/<int:id>/`

### Review and Comment System
- **Post a Review**: `POST /books/<int:book_id>/reviews/`
- **List Reviews for a Book**: `GET /books/<int:book_id>/reviews/`
- **Edit a Review**: `PATCH /reviews/<int:review_id>/`
- **Delete a Review**: `DELETE /reviews/<int:review_id>/`

---

## Pagination
The system supports pagination for listing books. You can use the following query parameters:
- **PageNumberPagination**: `?page=<page_number>`

Example:
- `GET /books/?page=2` (Returns the second page of books)

---

## Testing
To run the tests, use the following command:
```bash
python manage.py test
```