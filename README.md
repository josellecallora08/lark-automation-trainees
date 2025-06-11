# Gradify - Assessment System

A robust Python-based assessment system designed to handle evaluation of realizations and trainees through an asynchronous task processing architecture.

## System Overview

Gradify is an assessment system that processes two main types of evaluations:
- **Evaluate Realizations (ER)**: Handles realization assessments
- **Evaluate Trainees (ET)**: Manages trainee evaluations

The system uses an asynchronous task queue architecture to process assessments efficiently and reliably.

## Project Structure

```
gradify/
├── app/                    # Main application code
│   ├── common/            # Shared utilities and base classes
│   ├── config/            # Configuration settings
│   ├── dtos/              # Data Transfer Objects
│   ├── enums/             # Enumeration definitions
│   ├── interfaces/        # Interface definitions
│   ├── services/          # Business logic services
│   ├── src/               # Source code
│   ├── stores/            # Data storage implementations
│   └── exceptions/        # Custom exception definitions
├── data/                  # Data storage directory
├── logs/                  # Application logs
├── storage/              # File storage
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
└── docker-compose.yml   # Docker Compose configuration
```

## Dependencies

The system relies on several key Python packages:

- **Data Processing**: pandas, polars
- **AI/ML**: groq
- **Data Validation**: pydantic
- **Async Operations**: asyncio, websockets
- **HTTP Client**: httpx, requests
- **Environment Management**: python-dotenv
- **Date/Time**: pytz, python-dateutil

## Setup and Installation

### Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py --server-task [er|et]
   ```

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t gradify .
   ```

2. Run using Docker Compose:
   ```bash
   docker-compose up
   ```

## Architecture

### Core Components

1. **Task Queue System**
   - Asynchronous processing of assessment tasks
   - Handles both realization and trainee evaluations
   - Implements worker pattern for task processing

2. **Handlers**
   - `EvaluateRealization`: Processes realization assessments
   - `EvaluateTrainees`: Manages trainee evaluations

3. **Context Management**
   - `AppContext`: Manages application-wide state and resources
   - `Worker`: Handles task synchronization and processing

### Running Modes

The system supports two main running modes:
- `er`: Evaluate Realizations mode
- `et`: Evaluate Trainees mode

## Development

### Adding New Features

1. Create appropriate DTOs in `app/dtos/`
2. Implement handlers in `app/src/handlers/`
3. Add necessary services in `app/services/`
4. Update configuration in `app/config/`

### Best Practices

1. Follow the established project structure
2. Use type hints and docstrings
3. Implement proper error handling
4. Write tests for new features
5. Update documentation as needed

## Configuration

The system uses environment variables for configuration. Create a `.env` file with the following variables:

```env
# Add your environment variables here
```

## Logging

Logs are stored in the `logs/` directory. The system uses structured logging for better debugging and monitoring.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

[Add support information here] 