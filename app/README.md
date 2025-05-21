# Backend - FastAPI Vue Template

This directory contains the FastAPI backend for the FastAPI Vue Template project.

## 🚀 Features

- **FastAPI**: Modern, fast web framework for building APIs with Python
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM)
- **Pydantic**: Data validation and settings management
- **JWT Authentication**: Secure authentication with JSON Web Tokens
- **Dependency Injection**: Clean and testable code
- **Automatic API Documentation**: Swagger UI and ReDoc
- **Async Support**: High performance with async/await
- **Testing**: Comprehensive testing with pytest
- **Type Hints**: Improved code quality and IDE support

## 📋 Prerequisites

- Python ≥ 3.9
- Poetry ≥ 1.0.0
- Docker ≥ 20.10 (for containerized development)

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fastapivue-template.git
   cd fastapivue-template
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```

## 🚀 Development

Start the development server:
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8010
```

Or use the Makefile:
```bash
make run
```

### Available Commands

- `make install`: Install dependencies
- `make run`: Start the development server
- `make test`: Run tests
- `make lint`: Check code style
- `make format`: Format code
- `make clean`: Clean temporary files

## 📁 Project Structure

```
app/
├── api/                # API endpoints
│   ├── deps.py         # Dependency injection
│   └── routes/         # API route definitions
├── core/               # Core application components
│   ├── config.py       # Configuration management
│   └── security.py     # Security utilities
├── database/           # Database models and session
├── models/             # Pydantic models
├── repositories/       # Data access layer
├── schema/             # Schema definitions
├── tests/              # Test suite
└── main.py             # Application entry point
```

## 🔧 Configuration

The application uses environment variables for configuration. See `.env.example` for available options.

Key configuration options:
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for JWT token generation
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## 🧪 Testing

Run tests with pytest:
```bash
poetry run pytest
```

Or use the Makefile:
```bash
make test
```

## 📚 API Documentation

When the application is running, you can access:
- Swagger UI: http://localhost:8010/docs
- ReDoc: http://localhost:8010/redoc

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](../CONTRIBUTING.md) before submitting a pull request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
