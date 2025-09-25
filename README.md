# Agentic Design Patterns

A multi-project repository for exploring and implementing agentic design patterns using Python. \
These design patterns come from the book (Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems)[https://www.amazon.ca/Agentic-Design-Patterns-Hands-Intelligent/dp/3032014018] by Antonio Gulli


## Development Environment
You can use docker to run and setup the project, or directly run it on your machine.

### Quick Start

1. **Build the development environment:**
   ```bash
   ./dev.sh build
   # or
   make build
   ```

2. **Start the development environment:**
   ```bash
   ./dev.sh up
   # or
   make up
   ```

3. **Enter the development container:**
   ```bash
   ./dev.sh shell
   # or
   make shell
   ```

### Available Commands

#### Using the shell script (`dev.sh`):

```bash
# Environment management
./dev.sh build              # Build the development environment
./dev.sh up                 # Start the development environment
./dev.sh down               # Stop the development environment
./dev.sh shell              # Enter the development container shell

# Project management
./dev.sh list               # List available projects
./dev.sh run <project>      # Run a specific project
./dev.sh debug <project>    # Run a project in debug mode
./dev.sh test [project]     # Run tests (optionally for specific project)
./dev.sh lint [project]     # Run linting (optionally for specific project)
./dev.sh format [project]   # Format code (optionally for specific project)

# Utilities
./dev.sh logs               # Show container logs
./dev.sh clean              # Clean up containers and volumes
./dev.sh help               # Show help message
```

#### Using Make:

```bash
make build                   # Build the development environment
make up                      # Start the development environment
make down                    # Stop the development environment
make shell                   # Enter the development container shell
make run PROJECT=<name>      # Run a specific project
make debug PROJECT=<name>    # Run a project in debug mode
make test PROJECT=<name>     # Run tests (optionally for specific project)
make lint PROJECT=<name>     # Run linting (optionally for specific project)
make format PROJECT=<name>   # Format code (optionally for specific project)
make clean                   # Clean up containers and volumes
make logs                    # Show container logs
```

### VS Code Integration

This repository includes VS Code dev container configuration. To use it:

1. Install the "Dev Containers" extension in VS Code
2. Open the repository in VS Code
3. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) and select "Dev Containers: Reopen in Container"
4. VS Code will build and start the container with all necessary extensions and configurations

### Project Structure

Each project should be in its own directory under `projects/` with one of the following entry points:
- `main.py`
- `run.py`
- `app.py`

Example project structure:
```
projects/
└── Prompt Chaining/
    ├── main.py
    ├── README.md
    ├── requirements.txt
    └── tests/
        └── test_main.py
```

Repository structure:
```
Agentic Design Patterns/
├── dev.sh                    # Development script
├── docker-compose.yml        # Docker orchestration
├── Dockerfile               # Development container
├── Makefile                 # Convenient shortcuts
├── requirements.txt         # Global dependencies
├── requirements-dev.txt     # Development dependencies
├── pip-manager.py           # Package management
├── scripts/                 # Utility scripts
├── projects/               # All agentic patterns
│   └── Prompt Chaining/    # Example pattern
└── .devcontainer/          # VS Code integration
```

### Debugging

To debug a project:

1. Start the development environment: `./dev.sh up`
2. Run the project in debug mode: `./dev.sh debug <project>`
3. Attach your debugger to `localhost:5678`

The debugger will wait for a client connection before starting execution.

### Database Support

If your project needs a database, you can start the PostgreSQL service:

```bash
docker-compose --profile database up -d postgres
```

The database will be available at `localhost:5432` with:
- Database: `agentic_patterns`
- Username: `dev`
- Password: `dev123`

### Dependencies

- **Core dependencies** are defined in `requirements.txt`
- **Development dependencies** are defined in `requirements-dev.txt`
- **Project-specific dependencies** can be added to individual project directories

### Package Management

Simple and straightforward package management using Docker commands:

#### Direct Docker Commands (Recommended):

```bash
# Install packages
docker-compose exec python-dev pip install requests
docker-compose exec python-dev pip install pytest

# Uninstall packages
docker-compose exec python-dev pip uninstall requests

# List packages
docker-compose exec python-dev pip list

# Update packages
docker-compose exec python-dev pip install --upgrade requests

# Show current environment
docker-compose exec python-dev pip freeze
```

#### Convenient Make Shortcuts:

```bash
# Install packages
make pip-install PACKAGE=requests
make pip-install PACKAGE=pytest

# Uninstall packages
make pip-uninstall PACKAGE=requests

# List packages
make pip-list

# Update packages
make pip-update PACKAGE=requests

# Show current environment
make pip-freeze
```

#### Managing Requirements Files:

```bash
# Update global requirements
docker-compose exec python-dev pip freeze > requirements.txt

# Update development requirements
docker-compose exec python-dev pip freeze > requirements-dev.txt

# Create project-specific requirements
docker-compose exec python-dev pip freeze > projects/MyProject/requirements.txt
```

### Ports

The development environment exposes the following ports:
- `5678`: Python debugger
- `8000`: Web applications
- `8888`: Jupyter notebooks
- `5432`: PostgreSQL database (when using database profile)

### Environment Variables

The following environment variables are set in the container:
- `PYTHONPATH=/workspace`
- `PYTHONUNBUFFERED=1`
- `PYTHONDONTWRITEBYTECODE=1`

### Troubleshooting

1. **Container won't start**: Check if ports are already in use
2. **Permission issues**: The container runs as a non-root user (`dev`)
3. **Dependencies not found**: Make sure to rebuild the container after changing requirements files
4. **Debugger not connecting**: Ensure port 5678 is not blocked by firewall
5. **Script not executable**: Run `chmod +x dev.sh` if you get permission errors