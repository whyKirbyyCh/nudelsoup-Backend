# nudelsoup-Backend

## starting application
`uvicorn main:app --reload`


## Layout
project/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # Main entry point for the application
│   ├── core/                   # Core configuration files
│   │   ├── __init__.py
│   │   ├── config.py           # Application configuration (settings)
│   │   └── database.py         # Database setup and connection
│   │
│   ├── models/                 # Database models
│   │   ├── __init__.py
│   │   └── item.py             # Example model file
│   │
│   ├── schemas/                # Pydantic models for request/response validation
│   │   ├── __init__.py
│   │   └── item.py             # Example schema file
│   │
│   ├── routers/                # API route handlers
│   │   ├── __init__.py
│   │   └── items.py            # Example router file
│   │
│   ├── crud/                   # CRUD operations
│   │   ├── __init__.py
│   │   └── item.py             # CRUD logic for items
│   │
│   ├── tests/                  # Unit and integration tests
│   │   ├── __init__.py
│   │   └── test_items.py       # Example test file
│   │
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       └── helpers.py          # Example helper functions
│
├
