# FastAPI Backend Starter

A production-ready FastAPI backend starter template with PostgreSQL, SQLAlchemy, Alembic migrations, and Docker support.

## 🚀 Features

- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL 17.5** - Robust, open-source database
- **SQLAlchemy ORM** - Python SQL toolkit and Object-Relational Mapping
- **Alembic** - Database migration tool for SQLAlchemy
- **Docker & Docker Compose** - Containerized development environment
- **Role-Based Access Control** - User roles with Superuser protection
- **Password Hashing** - Secure password storage with bcrypt
- **Pydantic** - Data validation using Python type annotations
- **Black & Flake8** - Code formatting and linting
- **Pytest** - Testing framework
- **Makefile** - Convenient development commands

## 📋 Requirements

- Python 3.8.18
- Docker & Docker Compose
- Make (optional, for using Makefile commands)

## 🛠️ Quick Start

### Using Docker (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   git clone <your-repo-url>
   cd vibe-coding-01
   ```

2. **Copy environment variables:**
   ```bash
   cp env.example .env
   ```

3. **Start the application:**
   ```bash
   make run
   # or
   docker-compose up --build
   ```

4. **Access the application:**
   - API: http://localhost:8001
   - Interactive API docs: http://localhost:8001/docs
   - Alternative docs: http://localhost:8001/redoc

### Local Development (Without Docker)

1. **Install Python dependencies:**
   ```bash
   make install
   # or
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL database:**
   - Install PostgreSQL 17.5
   - Create database: `fastapi_db`
   - Update `.env` with your database credentials

3. **Run database migrations:**
   ```bash
   make migrate
   # or
   alembic upgrade head
   ```

4. **Start the application:**
   ```bash
   make run-local
   # or
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📁 Project Structure

```
vibe-coding-01/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # Database operations
│   └── routers/
│       ├── __init__.py
│       ├── health.py        # Health check endpoints
│       └── users.py         # User CRUD endpoints
├── alembic/                 # Database migrations
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── tests/                   # Test files
│   ├── __init__.py
│   ├── test_main.py
│   └── test_users.py
├── docker-compose.yml       # Docker services
├── Dockerfile              # App container
├── requirements.txt        # Python dependencies
├── Makefile               # Development commands
├── alembic.ini           # Alembic configuration
├── .flake8               # Linting configuration
├── pyproject.toml        # Project configuration
└── README.md
```

## 🔧 Available Commands

### Makefile Commands

```bash
make help          # Show all available commands
make run           # Start application with Docker Compose
make format        # Format code with black and lint with flake8
make test          # Run tests
make migrate       # Run database migrations
make clean         # Clean up Docker containers and volumes
make install       # Install Python dependencies locally
make run-local     # Run application locally (without Docker)
```

### Manual Commands

```bash
# Database migrations
alembic upgrade head                    # Apply migrations
alembic revision --autogenerate -m "message"  # Create new migration

# Code formatting and linting
black app/ tests/ --line-length 88
flake8 app/ tests/ --max-line-length 88

# Testing
pytest tests/ -v

# Docker
docker-compose up --build              # Start services
docker-compose down -v                 # Stop and remove volumes
```

## 🗄️ Database

### Models

The application includes a `User` model with the following fields:
- `id` - Primary key
- `email` - Unique email address
- `username` - Unique username
- `full_name` - Optional full name
- `is_active` - Boolean flag for user status
- `created_at` - Timestamp when user was created
- `updated_at` - Timestamp when user was last updated

### Migrations

Create a new migration:
```bash
make migrate-create
# or
alembic revision --autogenerate -m "Your migration message"
```

Apply migrations:
```bash
make migrate
# or
alembic upgrade head
```

## 🧪 Testing

Run tests:
```bash
make test
# or
pytest tests/ -v
```

The test suite includes:
- Health check endpoint tests
- User CRUD operation tests
- Duplicate email/username validation tests

## 📡 API Endpoints

### Health Check
- `GET /health` - Returns application health status

### Users
- `GET /users/` - Get all users (with pagination and role info)
- `POST /users/` - Create a new user (requires role_id)
- `GET /users/{user_id}` - Get a specific user with role
- `PUT /users/{user_id}` - Update a user
- `DELETE /users/{user_id}` - Delete a user

### Roles
- `GET /roles/` - Get all roles (with pagination)
- `POST /roles/` - Create a new role
- `GET /roles/{role_id}` - Get a specific role
- `PUT /roles/{role_id}` - Update a role (except Superuser)
- `DELETE /roles/{role_id}` - Delete a role (except Superuser)

### Interactive Documentation
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## 🔧 Configuration

Environment variables (see `env.example`):

```bash
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/fastapi_db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fastapi_db
DB_USER=postgres
DB_PASSWORD=password

# Application Configuration
APP_NAME=FastAPI Backend
DEBUG=True
```

## 🐳 Docker Services

### App Service
- **Image**: Built from local Dockerfile
- **Port**: 8001 (mapped from container port 8000)
- **Environment**: Configured via environment variables
- **Dependencies**: Waits for database to be healthy

### Database Service
- **Image**: postgres:17.5
- **Port**: 9005 (mapped from container port 5432)
- **Database**: fastapi_db
- **User**: postgres
- **Password**: password
- **Health Check**: Built-in PostgreSQL health check

## 🚀 Production Deployment

For production deployment:

1. **Update environment variables** with production values
2. **Use production database** (not the Docker PostgreSQL)
3. **Set `DEBUG=False`**
4. **Use a production WSGI server** like Gunicorn
5. **Set up proper logging and monitoring**
6. **Use environment-specific Docker Compose files**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Format code: `make format`
6. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Troubleshooting

### Common Issues

1. **Database connection errors**: Ensure PostgreSQL is running and credentials are correct
2. **Port conflicts**: Change ports in `docker-compose.yml` if 8000 or 5432 are in use
3. **Migration errors**: Check that all models are imported in `alembic/env.py`
4. **Permission errors**: Ensure Docker has proper permissions

### Getting Help

- Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
- Review [SQLAlchemy documentation](https://docs.sqlalchemy.org/)
- Check [Alembic documentation](https://alembic.sqlalchemy.org/)

## 👥 Role Management

### Default Roles
The system automatically creates two default roles on startup:

1. **Superuser** - Full system access (protected from deletion/modification)
2. **User** - Standard user role

### Default Superuser Account
A default administrator account is created automatically:
- **Username**: `admin`
- **Email**: `admin@example.com`
- **Password**: `admin123`
- **Role**: Superuser

⚠️ **Important**: Change the default password in production!

### Role-Based Data Structure

#### Users Table
- `id` - Primary key
- `email` - Unique email address
- `username` - Unique username
- `full_name` - Optional full name
- `password_hash` - Hashed password (bcrypt)
- `is_active` - Account status
- `role_id` - Foreign key to roles table
- `created_at` - Account creation timestamp
- `updated_at` - Last update timestamp

#### Roles Table
- `id` - Primary key
- `name` - Unique role name
- `created_at` - Role creation timestamp
- `updated_at` - Last update timestamp

### Role Protection
- **Superuser role** cannot be deleted or modified
- **Superuser role** is automatically created on startup
- All users must have a valid role assigned

### Creating Users with Roles
```json
POST /users/
{
  "email": "user@example.com",
  "username": "newuser",
  "full_name": "New User",
  "password": "securepassword",
  "role_id": 2
}
```

### Creating Custom Roles
```json
POST /roles/
{
  "name": "Manager"
}
```

## 🔄 Next Steps

- Add JWT authentication
- Implement role-based permissions
- Add password reset functionality
- Implement API rate limiting
- Add request/response logging
- Set up monitoring and health checks
- Add more comprehensive error handling
- Implement caching strategies
- Add API versioning
