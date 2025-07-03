# Testing Documentation

This document provides comprehensive information about testing in the VesselHarbor project, covering both backend and frontend testing approaches, frameworks, and patterns.

## Backend Testing

The backend uses pytest for testing. Tests are located in the `app/tests` directory.

### Testing Framework

- **pytest**: The main testing framework
- **pytest-asyncio**: For testing asynchronous code
- **SQLAlchemy**: For database testing with in-memory SQLite

### Test Structure

Backend tests follow a standard structure:

1. **Test Files**: Named with the pattern `test_*.py`
2. **Test Functions**: Named with the pattern `test_*`
3. **Fixtures**: Defined in `conftest.py` for common test setup
4. **Assertions**: Standard pytest assertions

### Test Categories

The backend tests cover various aspects of the application:

1. **Authentication Tests** (`test_auth.py`): Tests for login, token refresh, and authentication flows
2. **User Management Tests** (`test_users.py`): Tests for user creation, retrieval, updating, and deletion
3. **Environment Tests** (`test_environments.py`): Tests for environment management
4. **Element Tests** (`test_elements.py`): Tests for element creation and management
5. **Group Tests** (`test_groups.py`): Tests for group management
6. **Organization Tests** (`test_organization_users.py`): Tests for organization-user relationships
7. **Policy Tests** (`test_policy_deletion.py`): Tests for policy management
8. **Tag Tests** (`test_tag_auto_deletion.py`): Tests for tag management
9. **Audit Log Tests** (`test_audit_logs.py`): Tests for audit logging
10. **Access Schedule Tests** (`test_access_schedule.py`): Tests for access scheduling
11. **Storage Tests** (`test_storage_pool_from_volumes.py`, `test_volume_physical_host.py`): Tests for storage management
12. **Model Tests** (`test_model_import.py`): Tests for model imports and relationships

### Example Test

```python
def test_create_user(test_client, test_db):
    """Test creating a new user."""
    response = test_client.post(
        "/users",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "securepassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["email"] == "test@example.com"
    
    # Verify user was created in the database
    user = test_db.query(User).filter(User.email == "test@example.com").first()
    assert user is not None
    assert user.username == "testuser"
```

### Running Tests

To run the backend tests:

```bash
# Run all tests
cd app
poetry run pytest

# Run specific test file
poetry run pytest tests/test_users.py

# Run specific test function
poetry run pytest tests/test_users.py::test_create_user

# Run with coverage
poetry run pytest --cov=app
```

Alternatively, use the Makefile:

```bash
make backend-test
make backend-coverage
```

## Frontend Testing

The frontend uses Vitest for unit testing and Playwright for end-to-end testing.

### Unit Testing (Vitest)

Unit tests are located in the `frontend/tests` directory.

#### Testing Framework

- **Vitest**: Fast Vite-native testing framework
- **Vue Test Utils**: For testing Vue components
- **jsdom**: For DOM simulation

#### Test Structure

Frontend unit tests follow a standard structure:

1. **Test Files**: Named with the pattern `*.test.ts` or `*.spec.ts`
2. **Test Suites**: Defined with `describe()`
3. **Test Cases**: Defined with `it()` or `test()`
4. **Assertions**: Using `expect()`

#### Example Unit Test

```typescript
import { describe, it, expect } from 'vitest'

// A simple utility function to test
function sum(a: number, b: number): number {
  return a + b
}

describe('Basic Test Suite', () => {
  it('should add two numbers correctly', () => {
    expect(sum(1, 2)).toBe(3)
  })

  it('should handle negative numbers', () => {
    expect(sum(-1, -2)).toBe(-3)
  })

  it('should handle zero', () => {
    expect(sum(0, 0)).toBe(0)
  })
})
```

#### Running Unit Tests

```bash
# Run tests in watch mode
cd frontend
pnpm test

# Run tests once (for CI)
pnpm test:ci
```

Alternatively, use the Makefile:

```bash
make frontend-test
```

### End-to-End Testing (Playwright)

End-to-end tests are configured in `frontend/playwright.config.ts`.

#### Testing Framework

- **Playwright**: Modern end-to-end testing framework
- **Playwright Test**: Test runner for Playwright

#### Running E2E Tests

```bash
# Run e2e tests
cd frontend
pnpm test:e2e

# Run e2e tests in development mode
pnpm test:e2e:dev

# Run e2e tests with UI
pnpm test:eui:dev

# Record new tests
pnpm test:record:dev
```

Alternatively, use the Makefile:

```bash
make frontend-test-e2e
make frontend-test-e2e-ui
make frontend-test-record
```

## Test Coverage

Both backend and frontend tests include coverage reporting.

### Backend Coverage

Backend coverage is generated using pytest-cov and can be viewed as an HTML report:

```bash
make backend-coverage
```

### Frontend Coverage

Frontend coverage is generated by Vitest and can be viewed in the terminal or as an HTML report:

```bash
cd frontend
pnpm test:coverage
```

## Continuous Integration

Tests are automatically run in the CI pipeline for every pull request and push to the main branch. The CI pipeline includes:

1. Running backend tests with coverage
2. Running frontend unit tests
3. Running frontend end-to-end tests
4. Linting and type checking

## Best Practices

### Backend Testing

1. Use fixtures for common setup
2. Test both success and error cases
3. Mock external dependencies
4. Use parameterized tests for similar test cases
5. Keep tests isolated and independent
6. Use meaningful test names that describe the behavior being tested

### Frontend Testing

1. Focus on component behavior, not implementation details
2. Test user interactions
3. Mock API calls
4. Test edge cases and error states
5. Keep tests simple and focused
6. Use data-testid attributes for test selectors
