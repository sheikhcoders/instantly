# Intelligent Conversation Agent System

This project implements an intelligent conversation agent system using FastAPI and the OpenAI API. The backend is built with a Domain-Driven Design (DDD) architecture, supporting intelligent dialogue, file operations, Shell command execution, and browser automation.

## Project Architecture

The project adopts Domain-Driven Design (DDD) architecture, clearly separating the responsibilities of each layer:

```
backend/
├── app/
│   ├── domain/          # Domain layer: contains core business logic
│   │   ├── models/      # Domain model definitions
│   │   ├── services/    # Domain services
│   │   ├── external/    # External service interfaces
│   │   └── prompts/     # Prompt templates
│   ├── application/     # Application layer: orchestrates business processes
│   │   ├── services/    # Application services
│   │   └── schemas/     # Data schema definitions
│   ├── interfaces/      # Interface layer: defines external system interfaces
│   │   └── api/
│   │       └── routes.py # API route definitions
│   ├── infrastructure/  # Infrastructure layer: provides technical implementation
│   └── main.py          # Application entry
├── Dockerfile           # Docker configuration file
├── run.sh               # Production environment startup script
├── dev.sh               # Development environment startup script
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Core Features

*   **Session Management**: Create and manage conversation session instances
*   **Real-time Conversation**: Implement real-time conversation through Server-Sent Events (SSE)
*   **Tool Invocation**: Support for various tool calls, including:
    *   Browser automation operations (using Playwright)
    *   Shell command execution and viewing
    *   File read/write operations
    *   Web search integration
*   **Sandbox Environment**: Use Docker containers to provide isolated execution environments
*   **VNC Visualization**: Support remote viewing of the sandbox environment via WebSocket connection

## Requirements

*   Python 3.9+
*   Docker 20.10+
*   MongoDB 4.4+
*   Redis 6.0+

## Installation and Configuration

1.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application**:
    *   Development: `./dev.sh`
    *   Production: `./run.sh`
