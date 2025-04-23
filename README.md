# New Generation ERP System

A modern Enterprise Resource Planning (ERP) system built with FastAPI and Vue.js, designed to streamline business operations and improve efficiency.

## Features

- **User Management**: Comprehensive user authentication and role-based access control
- **Order Processing**: Complete order lifecycle management from creation to fulfillment
- **Inventory Management**: Real-time tracking of products and stock levels
- **Supplier Management**: Maintain supplier information and relationships
- **Financial Management**: 
  - Account management
  - Transaction tracking
  - Budget control
  - Financial reporting (Balance Sheet, Income Statement, Cash Flow)

## Tech Stack

### Backend
- FastAPI (Python)
- SQLAlchemy (ORM)
- Alembic (Database Migrations)
- PostgreSQL (Database)

### Frontend
- Vue.js 3
- TypeScript
- Element Plus (UI Components)
- Vuex (State Management)
- Vue Router

## Project Structure

```
├── src/
│   ├── api/           # API endpoints
│   ├── models/        # Database models
│   ├── scripts/       # Utility scripts
│   └── tests/         # Test files
├── frontend/          # Vue.js frontend
├── alembic/           # Database migrations
└── requirements.txt   # Python dependencies
```

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/NewGenerationERP.git
cd NewGenerationERP
```

2. Set up the backend:
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the API server
python -m src.api.main
```

3. Set up the frontend:
```bash
cd frontend
npm install
npm run serve
```

4. Access the application:
- API Documentation: http://localhost:8082/docs
- Web Interface: http://localhost:8080

## Development Status

- [x] Backend API implementation
- [x] Database schema and migrations
- [x] Basic CRUD operations
- [x] Frontend development
- [ ] User authentication
- [ ] Financial reporting
- [ ] Data visualization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 