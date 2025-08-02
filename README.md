# SujhavMitra – Flask Backend

**SujhavMitra** is a recommendation system backend built with Flask that provides personalized book and movie recommendations using machine learning models. The system includes user authentication, JWT-based authorization, and content-based filtering algorithms.

---

## 🚀 Features

- **User Management**: Registration, login, profile updates, and deletion
- **JWT Authentication**: Secure token-based authentication with role-based access control
- **Book Recommendations**: Content-based filtering using similarity scores
- **Movie Recommendations**: ML-powered movie suggestions based on user preferences
- **Popular Content**: Trending books and movies for discovery
- **MySQL Database**: Persistent user data storage
- **RESTful APIs**: Clean and consistent API endpoints

---

## 🛠️ Tech Stack

- **Backend Framework**: Flask (Python)
- **Database**: MySQL
- **Authentication**: JWT (JSON Web Tokens)
- **Password Security**: bcrypt
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Data Storage**: Pickle files for ML models

---

## 📁 Project Structure

```
SujhavMitra/backend/
├── app.py                              # Main Flask application
├── requirements.txt                    # Python dependencies
├── README.md                          # This documentation
│
├── configs/
│   └── config.py                      # Database and JWT configuration
│
├── controller/
│   ├── user_controller.py             # User management endpoints
│   ├── book_recommend_controller.py   # Book recommendation endpoints
│   └── movie_recommend_controller.py  # Movie recommendation endpoints
│
├── model/
│   ├── user_model.py                  # User data operations
│   ├── auth_model.py                  # Authentication logic
│   ├── book_recommend_model.py        # Book recommendation engine
│   └── movie_recommend_model.py       # Movie recommendation engine
│
├── models/                            # Trained ML models (pickle files)
│   ├── books.pkl
│   ├── popular_books_df.pkl
│   ├── similarity_scores.pkl
│   ├── book_user_matrix.pkl
│   ├── movie_list.pkl
│   └── similarity_movies.pkl
│
└── data/                              # Raw datasets
    ├── books.csv
    └── movies.csv
```

---

## 🚀 Setup and Installation

### Prerequisites

- Python 3.7+
- MySQL Server
- Git

### 1. Clone the Repository

```bash
git lfs install
git clone <repository-url>
cd SujhavMitra/backend
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

1. Create a MySQL database for the project
2. Update `configs/config.py` with your database credentials:

```python
dbconfig = {
    "host": "localhost",
    "port": 3306,
    "username": "your_username",
    "password": "your_password",
    "database": "sujhavmitra_db"
}

JWT_SECRET = "your_jwt_secret_key"
```

3. Create required tables:

```sql
-- Users table
CREATE TABLE sm_users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id INT DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Accessibility table for role-based access
CREATE TABLE accessibility_view (
    id INT PRIMARY KEY AUTO_INCREMENT,
    endpoint VARCHAR(255) NOT NULL,
    role_id INT NOT NULL
);

-- Sample data for accessibility
INSERT INTO accessibility_view (endpoint, role_id) VALUES
('/user/all', 1),           -- Admin only
('/user/updateProfile', 3), -- Regular users
('/user/deleteprofile/<id>', 3); -- Regular users
```

### 5. Prepare Data Files

Ensure the following files are in place:

- `data/books.csv` - Book dataset
- `data/movies.csv` - Movie dataset
- `models/*.pkl` - Pre-trained ML models

### 6. Run the Application

```bash
python app.py
# or
flask run
```

The server will start at: `http://127.0.0.1:5000/`

---

## 📚 API Documentation

### Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### 👤 User Management

#### 1. User Registration

```http
POST /user/signup
Content-Type: application/x-www-form-urlencoded

name=John Doe
email=john@example.com
phone=+1234567890
password=securepassword123
```

**Response:**

```json
{
  "message": "User registered successfully"
}
```

#### 2. User Login

```http
POST /user/login
Content-Type: application/x-www-form-urlencoded

email=john@example.com
password=securepassword123
```

**Response:**

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### 3. Get All Users (Admin Only)

```http
GET /user/all
Authorization: Bearer <admin_token>
```

#### 4. Update User Profile

```http
PATCH /user/updateProfile
Authorization: Bearer <user_token>
Content-Type: application/x-www-form-urlencoded

name=Updated Name
phone=+1987654321
```

#### 5. Delete User Profile

```http
DELETE /user/deleteprofile/<user_id>
Authorization: Bearer <user_token>
```

### 📖 Book Recommendations

#### 1. Get Popular Books

```http
GET /recommend/book
```

**Response:**

```json
{
  "popular_books": [
    {
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "isbn": "9780743273565",
      "publishdate": 1925,
      "publisher": "Scribner",
      "imageurl": "https://example.com/image.jpg"
    }
  ]
}
```

#### 2. Get Book Recommendations

```http
GET /recommend/book?title="The Great Gatsby"
```

**Response:**

```json
{
  "recommendations": [
    {
      "title": "To Kill a Mockingbird",
      "author": "Harper Lee",
      "isbn": "9780061120084",
      "publishdate": 1960,
      "publisher": "J.B. Lippincott & Co.",
      "imageurl": "https://example.com/image.jpg"
    }
  ]
}
```

### 🎬 Movie Recommendations

#### 1. Get Popular Movies

```http
GET /recommend/movie
```

**Response:**

```json
{
  "popular_movie": [
    {
      "id": 550,
      "title": "Fight Club",
      "overview": "An insomniac office worker...",
      "genres": ["Drama", "Thriller"],
      "cast": ["Brad Pitt", "Edward Norton"],
      "crew": "David Fincher"
    }
  ]
}
```

#### 2. Get Movie Recommendations

```http
GET /recommend/movie?title="Fight Club"
```

**Response:**

```json
{
  "recommendations": [
    {
      "id": 807,
      "title": "Se7en",
      "overview": "Two homicide detectives...",
      "genres": ["Crime", "Mystery", "Thriller"],
      "cast": ["Morgan Freeman", "Brad Pitt"],
      "crew": "David Fincher"
    }
  ]
}
```

---

## 🔐 Security Features

### Password Security

- **bcrypt Hashing**: All passwords are hashed using bcrypt with salt
- **Minimum Length**: 6-character minimum password requirement
- **Secure Storage**: Passwords never stored in plain text

### JWT Authentication

- **Secure Tokens**: HS256 algorithm for token signing
- **Token Expiry**: 24-hour token lifespan
- **Role-based Access**: Different permission levels for users and admins

### Input Validation

- **Email Validation**: Regex-based email format checking
- **Phone Validation**: Basic phone number format validation
- **SQL Injection Prevention**: Parameterized queries throughout

---

## 🤖 Machine Learning Models

### Book Recommendation Engine

- **Algorithm**: Content-based filtering using TF-IDF vectorization
- **Features**: Book titles, authors, and metadata
- **Similarity Metric**: Cosine similarity
- **Model Files**:
  - `books.pkl` - Complete book dataset
  - `similarity_scores.pkl` - Precomputed similarity matrix
  - `book_user_matrix.pkl` - User-item interaction matrix

### Movie Recommendation Engine

- **Algorithm**: Content-based filtering
- **Features**: Movie genres, cast, crew, and overview
- **Similarity Metric**: Cosine similarity
- **Model Files**:
  - `movie_list.pkl` - Complete movie dataset
  - `similarity_movies.pkl` - Precomputed similarity matrix

---

## 🐛 Error Handling

The API returns appropriate HTTP status codes and error messages:

### Common Error Responses

#### 400 Bad Request

```json
{
  "error": "Email and password are required"
}
```

#### 401 Unauthorized

```json
{
  "ERROR": "INVALID_TOKEN"
}
```

#### 403 Forbidden

```json
{
  "ERROR": "ACCESS_DENIED"
}
```

#### 404 Not Found

```json
{
  "error": "Movie not found"
}
```

#### 500 Internal Server Error

```json
{
  "error": "Database connection not established"
}
```

---

## 🧪 Testing

### Manual Testing with cURL

1. **Register a new user:**

```bash
curl -X POST http://127.0.0.1:5000/user/signup \
  -d "name=Test User" \
  -d "email=test@example.com" \
  -d "phone=+1234567890" \
  -d "password=password123"
```

2. **Login and get token:**

```bash
curl -X POST http://127.0.0.1:5000/user/login \
  -d "email=test@example.com" \
  -d "password=password123"
```

3. **Get book recommendations:**

```bash
curl "http://127.0.0.1:5000/recommend/book?title=The Great Gatsby"
```

---

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Move sensitive configuration to environment variables
2. **HTTPS**: Use SSL/TLS in production
3. **Database**: Use connection pooling for better performance
4. **Logging**: Implement comprehensive logging
5. **Rate Limiting**: Add API rate limiting
6. **CORS**: Configure CORS for frontend integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Error**

   - Check MySQL server is running
   - Verify database credentials in `config.py`
   - Ensure database exists

2. **Import Errors**

   - Activate virtual environment
   - Install all requirements: `pip install -r requirements.txt`

3. **Model Files Missing**

   - Ensure all `.pkl` files are in the `models/` directory
   - Check file permissions

4. **JWT Token Issues**
   - Verify JWT_SECRET is set in config
   - Check token expiry (24 hours)
   - Ensure proper Authorization header format

### Getting Help

- Check the console output for detailed error messages
- Verify all file paths and dependencies
- Ensure MySQL server is accessible
- Review API endpoint URLs and request formats

---

**Sujhav Mitra! 🎉**
