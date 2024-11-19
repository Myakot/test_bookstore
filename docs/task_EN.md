Task: Book Store API

Create a small application that simulates the operation of a book store, working with two objects: books and authors.

Book Object:

1. id (int)
2. title (str)
3. author (id)
4. count (int) - remaining books in stock

Author Object:

1. id (int)
2. first_name (str)
3. last_name (str)

The application should implement the following API:

1. `GET /api/books` - returns a list of books
2. `POST /api/books` - creates a new book
3. `PUT /api/books/{id}` - edits a book
4. `POST /api/books/{id}/buy` - API for buying a book, decreases the count if it's positive or returns an error
5. `GET /api/authors` - returns a list of authors, with a list of their books (only titles) for each author
6. `POST /api/authors` - creates a new author
7. `PUT /api/authors/{id}` - edits an author

Additionally, implement:

1. Filtering books by author
2. Pagination for books

When implementing certain features, consider that our store sells millions of books.