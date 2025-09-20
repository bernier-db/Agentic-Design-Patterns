# Makefile for Agentic Design Patterns development environment

.PHONY: help build up down shell run debug test lint format clean logs pip-install pip-uninstall pip-list pip-update pip-sync

# Default target
help:
	@echo "Available commands:"
	@echo "  build     - Build the development environment"
	@echo "  up        - Start the development environment"
	@echo "  down      - Stop the development environment"
	@echo "  shell     - Enter the development container shell"
	@echo "  run       - Run a specific project (usage: make run PROJECT=project-name)"
	@echo "  debug     - Run a project in debug mode (usage: make debug PROJECT=project-name)"
	@echo "  test      - Run tests (usage: make test PROJECT=project-name)"
	@echo "  lint      - Run linting (usage: make lint PROJECT=project-name)"
	@echo "  format    - Format code (usage: make format PROJECT=project-name)"
	@echo "  clean     - Clean up containers and volumes"
	@echo "  logs      - Show container logs"
	@echo ""
	@echo "Package management commands:"
	@echo "  pip-install   - Install a package (usage: make pip-install PACKAGE=package-name)"
	@echo "  pip-uninstall - Uninstall a package (usage: make pip-uninstall PACKAGE=package-name)"
	@echo "  pip-list      - List installed packages"
	@echo "  pip-update    - Update a package (usage: make pip-update PACKAGE=package-name)"
	@echo "  pip-freeze    - Show current package versions"

# Build the development environment
build:
	./dev.sh build

# Start the development environment
up:
	./dev.sh up

# Stop the development environment
down:
	./dev.sh down

# Enter the development container shell
shell:
	./dev.sh shell

# Run a specific project
run:
	./dev.sh run $(PROJECT)

# Run a project in debug mode
debug:
	./dev.sh debug $(PROJECT)

# Run tests
test:
	./dev.sh test $(PROJECT)

# Run linting
lint:
	./dev.sh lint $(PROJECT)

# Format code
format:
	./dev.sh format $(PROJECT)

# Clean up containers and volumes
clean:
	./dev.sh clean

# Show container logs
logs:
	./dev.sh logs

# Package management commands
pip-install:
	docker-compose exec python-dev pip install $(PACKAGE)

pip-uninstall:
	docker-compose exec python-dev pip uninstall -y $(PACKAGE)

pip-list:
	docker-compose exec python-dev pip list

pip-update:
	docker-compose exec python-dev pip install --upgrade $(PACKAGE)

pip-freeze:
	docker-compose exec python-dev pip freeze
