# API Documentation

## Authentication

### Register User

**Endpoint:** `POST /api/v1/auth/register`

**Request Body:**

```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "password": "securepass123"
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2026-01-13T12:00:00Z",
  "updated_at": "2026-01-13T12:00:00Z"
}
```

### Login

**Endpoint:** `POST /api/v1/auth/login`

**Request Body (form-data):**

```
username: johndoe
password: securepass123
```

**Response:** `200 OK`

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## User Management

All user endpoints require authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_token>
```

### Get Current User

**Endpoint:** `GET /api/v1/users/me`

**Response:** `200 OK`

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2026-01-13T12:00:00Z",
  "updated_at": "2026-01-13T12:00:00Z"
}
```

### Update Current User

**Endpoint:** `PUT /api/v1/users/me`

**Request Body:**

```json
{
  "full_name": "John Smith",
  "password": "newpassword123"
}
```

**Response:** `200 OK`

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Smith",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2026-01-13T12:00:00Z",
  "updated_at": "2026-01-13T12:00:00Z"
}
```

## Item Management

### Create Item

**Endpoint:** `POST /api/v1/items`

**Request Body:**

```json
{
  "title": "My First Item",
  "description": "This is a test item"
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "title": "My First Item",
  "description": "This is a test item",
  "owner_id": 1,
  "is_active": true,
  "created_at": "2026-01-13T12:00:00Z",
  "updated_at": "2026-01-13T12:00:00Z"
}
```

### List Items

**Endpoint:** `GET /api/v1/items?skip=0&limit=100`

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "My First Item",
    "description": "This is a test item",
    "owner_id": 1,
    "is_active": true,
    "created_at": "2026-01-13T12:00:00Z",
    "updated_at": "2026-01-13T12:00:00Z"
  }
]
```

### Get Item

**Endpoint:** `GET /api/v1/items/{item_id}`

**Response:** `200 OK`

```json
{
  "id": 1,
  "title": "My First Item",
  "description": "This is a test item",
  "owner_id": 1,
  "is_active": true,
  "created_at": "2026-01-13T12:00:00Z",
  "updated_at": "2026-01-13T12:00:00Z"
}
```

### Update Item

**Endpoint:** `PUT /api/v1/items/{item_id}`

**Request Body:**

```json
{
  "title": "Updated Item Title",
  "description": "Updated description"
}
```

**Response:** `200 OK`

```json
{
  "id": 1,
  "title": "Updated Item Title",
  "description": "Updated description",
  "owner_id": 1,
  "is_active": true,
  "created_at": "2026-01-13T12:00:00Z",
  "updated_at": "2026-01-13T12:00:00Z"
}
```

### Delete Item

**Endpoint:** `DELETE /api/v1/items/{item_id}`

**Response:** `200 OK`

```json
{
  "message": "Item deleted successfully"
}
```

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Database constraint violation"
}
```

### 401 Unauthorized

```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden

```json
{
  "detail": "Not enough privileges"
}
```

### 404 Not Found

```json
{
  "detail": "Item not found"
}
```

### 422 Validation Error

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error"
}
```
