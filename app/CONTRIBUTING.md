# Contributing to the Backend

Thank you for your interest in contributing to the backend of our FastAPI Vue Template project! This document provides guidelines specifically for the FastAPI backend.

## Development Setup

1. Ensure you have the required prerequisites:
   - Python ≥ 3.9
   - Poetry ≥ 1.0.0
   - An IDE with Python support (VS Code or PyCharm recommended)

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Set up pre-commit hooks (optional but recommended):
   ```bash
   pre-commit install
   ```

## Code Style and Standards

We follow PEP 8 style guidelines with some modifications. Our code style is enforced using:

- **Black**: For code formatting
- **isort**: For import sorting
- **flake8**: For linting

Run formatting:
```bash
make format
```

Run linting:
```bash
make lint
```

## API Development Guidelines

- Use the appropriate HTTP methods (GET, POST, PUT, DELETE) for CRUD operations
- Use meaningful route names that reflect the resource being accessed
- Use Pydantic models for request and response validation
- Document all endpoints with docstrings and appropriate tags
- Include appropriate status codes in responses
- Handle errors gracefully and return meaningful error messages

Example endpoint:
```python
@router.get("/{item_id}", response_model=schemas.Item, status_code=200)
async def read_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Get an item by ID.
    
    Args:
        item_id: The ID of the item to retrieve
        db: Database session
        current_user: The authenticated user
        
    Returns:
        The item if found
        
    Raises:
        HTTPException: If item not found or user doesn't have permission
    """
    item = crud.get_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user_owns_item(db, user_id=current_user.id, item_id=item_id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return item
```

## Testing

We use pytest for testing. All new features should include tests.

1. Write tests in the `tests` directory
2. Run tests:
   ```bash
   make test
   ```

### Test Guidelines

- Write unit tests for all new functions and methods
- Write integration tests for API endpoints
- Use fixtures for common test setup
- Mock external dependencies
- Aim for at least 80% test coverage

Example test:
```python
def test_read_item(client, test_db, test_user, test_item):
    # Arrange
    login_response = client.post("/auth/login", json={
        "username": test_user.username,
        "password": "testpassword"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Act
    response = client.get(f"/items/{test_item.id}", headers=headers)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_item.id
    assert data["name"] == test_item.name
```

## Database Migrations

We use Alembic for database migrations.

1. After changing models, generate a new migration:
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   ```

2. Apply migrations:
   ```bash
   alembic upgrade head
   ```

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure they pass
5. Submit a pull request

Before submitting, ensure:
- All tests pass
- Code is properly formatted
- New features include tests
- Documentation is updated if necessary

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Pytest Documentation](https://docs.pytest.org/)

Thank you for contributing to our backend!
