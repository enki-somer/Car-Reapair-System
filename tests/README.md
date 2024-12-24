# Test Suite Documentation

## Overview

This directory contains unit tests for the auto parts inventory management system. The tests cover core functionality including inventory management, sales tracking, worker management, and reporting.

## Test Structure

- `conftest.py`: Test configuration and database setup
- `test_inventory.py`: Tests for inventory management
- `test_parts.py`: Tests for parts management
- `test_reports.py`: Tests for attendance and worker reports
- `test_sales.py`: Tests for sales operations
- `test_sales_reports.py`: Tests for sales reporting
- `test_workers.py`: Tests for worker management

## Running Tests

### Running All Tests

````

# Testing Guidelines and Maintenance Plan

## Test Organization

Tests are organized into the following categories:
- Unit tests: Test individual components
- Integration tests: Test component interactions
- UI tests: Test user interface functionality
- System tests: Test complete workflows

## Test Maintenance Guidelines

### When Adding New Features
1. Write tests **before** implementing the feature (TDD approach)
2. Create test cases that cover:
   - Happy path (expected usage)
   - Edge cases
   - Error conditions
   - UI interactions (if applicable)

### When Fixing Bugs
1. Create a test that reproduces the bug
2. Fix the bug
3. Verify the test passes
4. Add regression tests to prevent recurrence

### Regular Maintenance Tasks
- Run full test suite weekly
- Review test coverage monthly
- Update test data quarterly
- Clean up deprecated tests during major versions

## Test Coverage Requirements
- Minimum 80% code coverage for new features
- Critical paths must have 100% coverage
- UI components must have basic interaction tests

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/

# Run specific test category
pytest tests/unit/
pytest tests/integration/
pytest tests/ui/
````

## Continuous Integration

Tests are automatically run on:

- Every pull request
- Daily on main branch
- Before each release

## Test Data Management

- Test data is stored in `tests/fixtures/`
- Update test data when database schema changes
- Keep test data minimal but comprehensive

## Documentation Requirements

For each new test:

1. Clear description of what is being tested
2. Setup requirements
3. Expected outcomes
4. Any special considerations

Example:

```python
def test_part_creation():
    """
    Test creating a new auto part.

    Setup:
    - Clean database
    - Admin user logged in

    Expected:
    - Part is created with correct attributes
    - Creation is logged
    - UI is updated

    Notes:
    - Requires test database
    - Mock external API calls
    """
```
