# Contributing to FinSentrix

Thank you for your interest in contributing to FinSentrix! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/finsentrix.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Push to your fork: `git push origin feature/your-feature-name`
6. Create a Pull Request

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Coding Standards

### Python Code

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints
- Write docstrings for all public functions and classes
- Keep functions small and focused
- Use meaningful variable and function names

### TypeScript/JavaScript Code

- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use TypeScript for type safety
- Write JSDoc comments for public functions
- Use meaningful variable and function names

## Testing

- Write tests for all new features
- Ensure all tests pass before submitting a PR
- Maintain or improve test coverage
- Run tests locally before pushing:
  ```bash
  pytest
  ```

## Documentation

- Update documentation for any new features
- Keep docstrings up to date
- Update README.md if necessary
- Add examples for new features

## Pull Request Process

1. Ensure your code passes all tests
2. Update documentation
3. Update CHANGELOG.md
4. Submit PR with a clear description
5. Address any review comments

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- feat: new feature
- fix: bug fix
- docs: documentation changes
- style: formatting, missing semi-colons, etc.
- refactor: code refactoring
- test: adding or modifying tests
- chore: maintenance

## Review Process

- PRs will be reviewed by maintainers
- Address all review comments
- Be responsive to feedback
- Keep PRs focused and manageable

## Questions?

Feel free to open an issue for any questions or concerns. 