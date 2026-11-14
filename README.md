# Books API

A REST API for discovering books and sharing opinions about them. Users can register, sign in, browse and search the book catalogue, and give each book a rating. The API uses a Model-View-Controller (MVC) structure and JWT-based authentication.

## Technology

- Python
- MVC architecture
- JWT authentication

## Core concepts

### Book

- `id`: unique identifier assigned by the API
- `title`: required book title
- `description`: optional summary
- `created_at`: timestamp assigned by the API
- `vote_count`: number of votes, calculated by the API
- `average_rating`: average rating, calculated by the API

### User

- `id`: unique identifier assigned by the API
- `email`: required, unique email address
- `name`: required display name
- `password`: required on registration; store only a secure password hash, never the plaintext password
- `role`: `USER` or `ADMIN`; new registrations always receive `USER`

### Roles and permissions

- `USER`: can browse and search books, vote, and add, list, edit, or delete comments they authored. Users cannot create, update, or delete books.
- `ADMIN`: can create, update, and delete books. Admins can also browse books, vote, and comment.

The role is assigned and enforced by the API; clients must never be trusted to select or change their own role. Public registration does not accept a `role` field. Create or promote an administrator only through a trusted, out-of-band administrative process.

### Vote

A vote is a rating submitted by an authenticated user for a book. Each vote belongs to one user and one book.

- `id`: unique identifier assigned by the API
- `user_id`: ID of the user who submitted the vote
- `book_id`: ID of the rated book
- `rating`: integer from `1` to `5` (1 = very poor, 5 = excellent)
- `created_at`: timestamp assigned by the API
- `updated_at`: timestamp updated when the user changes their rating

There can be only one vote per user for each book. A user can rate many books, and a book can receive votes from many users. The API calculates `vote_count` and `average_rating` from individual votes; clients do not set these aggregate values directly. If a book has no votes, its `vote_count` is `0` and its `average_rating` is `null`.

For example, if ratings for a book are `5`, `4`, and `2`, its `vote_count` is `3` and its `average_rating` is `3.67` (rounded to two decimal places).

### Comment

A comment is a text opinion about a book, written by an authenticated user. Each comment belongs to one user and one book. Unlike votes, a user can write multiple comments for the same book.

- `id`: unique identifier assigned by the API
- `user_id`: ID of the author
- `book_id`: ID of the book being discussed
- `text`: comment content
- `created_at`: timestamp assigned by the API
- `updated_at`: timestamp updated when the author edits the comment

Users can edit or delete only their own comments. A comment's author and book are set when it is created and cannot be changed by editing it.

## API conventions

- Base path: `/api/v1`
- Request and response bodies use JSON.
- IDs shown as `{book_id}` or `{user_id}` are path parameters, replaced with actual IDs such as `42`.
- Protected endpoints require `Authorization: Bearer <token>`. Obtain the token from `POST /api/v1/auth`.
- The API returns standard HTTP status codes: `200` for successful reads/updates, `201` for creation, `204` for successful deletion, `400` for invalid input, `401` for missing or invalid authentication, `403` for an authenticated user who is not allowed to modify a resource, `404` for a missing resource, and `409` for a duplicate email.

## Endpoints

### Books

#### `POST /api/v1/books`

Create a book. Requires authentication with the `ADMIN` role.

Request body:

```json
{
  "title": "The Hobbit",
  "description": "A hobbit goes on an unexpected journey."
}
```

`title` is required and must not be blank. `description` is optional. The API generates the book ID and timestamps, and initializes its vote aggregates.

#### `GET /api/v1/books`

List books. This endpoint does not require authentication.

Optional query parameters:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `page` | integer | `1` | Page number; must be at least `1`. |
| `per_page` | integer | `20` | Number of results per page; must be between `1` and `100`. |

Example: `GET /api/v1/books?page=1&per_page=10`

Each book in the response includes `vote_count` and `average_rating`.

#### `GET /api/v1/books/search?q={term}`

Search books by title or description. This endpoint does not require authentication.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `q` | string | Yes | Search text; whitespace is trimmed and an empty value is rejected. |
| `page` | integer | No | Page number, default `1`. |
| `per_page` | integer | No | Results per page, default `20`, maximum `100`. |

Example: `GET /api/v1/books/search?q=unexpected%20journey&page=1&per_page=10`

#### `GET /api/v1/books/{book_id}`

Get one book by its ID. Returns `404` if no book has that ID.

Example response:

```json
{
  "id": 42,
  "title": "The Hobbit",
  "description": "A hobbit goes on an unexpected journey.",
  "vote_count": 3,
  "average_rating": 3.67,
  "created_at": "2025-01-15T12:30:00Z"
}
```

#### `PATCH /api/v1/books/{book_id}`

Update a book. Requires authentication with the `ADMIN` role. Include only the fields to change; `title` must not be blank if provided.

Request body:

```json
{
  "description": "Bilbo Baggins joins a quest to reclaim a dwarf kingdom."
}
```

#### `DELETE /api/v1/books/{book_id}`

Delete a book. Requires authentication with the `ADMIN` role. Deleting a book also deletes its associated votes and comments. Returns `404` if no book has that ID.

### Votes

#### `PUT /api/v1/books/{book_id}/votes/me`

Create or replace the authenticated user's vote for a book. Requires authentication. The book ID is a path parameter; the rating is sent in the JSON body.

Request body:

```json
{
  "rating": 5
}
```

`rating` must be an integer from `1` through `5`. Calling this endpoint again for the same book updates that user's existing vote instead of creating a second vote. Returns `404` if the book does not exist.

Example response:

```json
{
  "book_id": 42,
  "rating": 5,
  "vote_count": 4,
  "average_rating": 4.0
}
```

In this example, the user has set their rating to `5`; the API returns the book's updated aggregate values.

#### `DELETE /api/v1/books/{book_id}/votes/me`

Remove the authenticated user's vote for a book. Requires authentication. The user can remove only their own vote. If they have not voted for that book, the API returns `404`. On success, returns `204 No Content`; the book's vote aggregates are recalculated.

### Comments

#### `GET /api/v1/books/{book_id}/comments`

List comments for a book, oldest first. This endpoint does not require authentication. Returns `404` if the book does not exist.

Optional query parameters:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `page` | integer | `1` | Page number; must be at least `1`. |
| `per_page` | integer | `20` | Number of results per page; must be between `1` and `100`. |

Each comment includes its `id`, `book_id`, `user_id`, author display name, `text`, `created_at`, and `updated_at`.

#### `POST /api/v1/books/{book_id}/comments`

Add a comment to a book. Requires authentication. The author is taken from the JWT, not from the request body.

Request body:

```json
{
  "text": "The characters felt believable, and I enjoyed the pacing."
}
```

`text` is required, must contain non-whitespace characters, and must not exceed 2,000 characters. Returns `404` if the book does not exist.

Example response:

```json
{
  "id": 101,
  "book_id": 42,
  "user_id": 7,
  "author_name": "Alex Reader",
  "text": "The characters felt believable, and I enjoyed the pacing.",
  "created_at": "2025-01-16T09:15:00Z",
  "updated_at": "2025-01-16T09:15:00Z"
}
```

#### `PATCH /api/v1/comments/{comment_id}`

Edit a comment. Requires authentication, and the authenticated user must be its author. The only editable field is `text`, with the same validation rules as when creating a comment. Returns `403` if the comment belongs to another user and `404` if it does not exist.

Request body:

```json
{
  "text": "The characters felt believable, and the pacing kept me engaged."
}
```

#### `DELETE /api/v1/comments/{comment_id}`

Delete a comment. Requires authentication, and the authenticated user must be its author. On success, returns `204 No Content`. Returns `403` if the comment belongs to another user and `404` if it does not exist.

### Users and authentication

#### `POST /api/v1/register`

Register a user.

Request body:

```json
{
  "email": "reader@example.com",
  "name": "Alex Reader",
  "password": "a-strong-password"
}
```

All fields are required. The email must not already be registered. The API assigns the `USER` role; do not send a `role` field during public registration. Never return the password or its stored hash in an API response.

#### `POST /api/v1/auth`

Authenticate a user and return a JWT.

Request body:

```json
{
  "email": "reader@example.com",
  "password": "a-strong-password"
}
```

Example response:

```json
{
  "access_token": "<jwt>",
  "token_type": "Bearer",
  "role": "USER"
}
```

Use the token on protected endpoints:

```http
Authorization: Bearer <jwt>
```

## Suggested initial scope

Start with registration, login, role-based authorization, book search, admin-only book creation/update/deletion, voting, and comments. Keep votes and comments as separate entities: votes are one 1–5 rating per user per book, while comments are text entries that users can add, list, edit, or delete according to the ownership rules above.
