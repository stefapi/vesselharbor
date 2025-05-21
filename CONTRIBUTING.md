# Contributing to FastAPI Vue Template

Thank you for your interest in contributing to the FastAPI Vue Template project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- Be respectful and inclusive
- Be patient and welcoming
- Be thoughtful
- Be collaborative
- When disagreeing, try to understand why

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with the following information:

1. Clear, descriptive title
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Screenshots (if applicable)
6. Environment details (OS, browser, etc.)

### Suggesting Features

We welcome feature suggestions! Please create an issue with:

1. Clear, descriptive title
2. Detailed description of the proposed feature
3. Any relevant examples or mockups
4. Explanation of why this feature would be useful

### Pull Requests

Follow these steps to submit a pull request:

1. Fork the repository
2. Create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality:
   ```bash
   # Backend tests
   cd app
   poetry run pytest
   
   # Frontend tests
   cd frontend
   pnpm test:ci
   ```
5. Commit your changes with a clear message:
   ```bash
   git commit -m "Add: brief description of your changes"
   ```
6. Push to your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
7. Create a pull request against the `main` branch

## Development Setup

Please refer to the [Project Guidelines](.junie/guidelines.md) for detailed setup instructions.

## Coding Standards

### Backend (Python)

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all functions, classes, and modules
- Keep functions small and focused
- Use meaningful variable names

### Frontend (Vue/TypeScript)

- Follow the Vue.js Style Guide (Priority A and B rules)
- Use TypeScript for type safety
- Use composition API for new components
- Use PascalCase for component names
- Use kebab-case for custom events

## Testing Guidelines

### Backend Testing

- Write unit tests for all new functionality
- Aim for high test coverage (at least 80%)
- Use pytest fixtures for common test setup
- Mock external dependencies

### Frontend Testing

- Write unit tests for complex components and utilities
- Write end-to-end tests for critical user flows
- Test both success and error scenarios

## Git Workflow

### Branch Naming

- `feature/` - for new features
- `bugfix/` - for bug fixes
- `docs/` - for documentation changes
- `refactor/` - for code refactoring
- `test/` - for adding or modifying tests

### Commit Messages

Follow the conventional commits specification:

- `feat:` - a new feature
- `fix:` - a bug fix
- `docs:` - documentation changes
- `style:` - formatting changes
- `refactor:` - code refactoring
- `test:` - adding or modifying tests
- `chore:` - maintenance tasks

Example:
```
feat: add user authentication API
```

## Additional Resources

For more detailed information, please refer to the documentation in the `.junie` directory:

- [API Endpoints](.junie/api-endpoints.md)
- [Architecture](.junie/architecture.md)
- [Project Guidelines](.junie/guidelines.md)

Thank you for contributing to the FastAPI Vue Template project!
