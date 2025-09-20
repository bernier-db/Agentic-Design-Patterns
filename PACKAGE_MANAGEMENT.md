# Package Management Guide

Simple and straightforward package management for the Agentic Design Patterns development environment.

## The Simple Way

**Just use Docker commands directly** - it's the most transparent and reliable method:

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

## Convenient Shortcuts

If you prefer shorter commands, use the Make shortcuts:

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

## Managing Requirements Files

### Global Dependencies (`requirements.txt`)
- Core packages used across all projects
- Installed automatically when building the container

### Development Dependencies (`requirements-dev.txt`)
- Tools for development, testing, and code quality
- Installed automatically when building the container

### Project-Specific Dependencies
- Packages specific to individual projects
- Stored in project directories as `requirements.txt`

## Best Practices

### 1. Install Packages
```bash
# Install a new package
docker-compose exec python-dev pip install requests

# Update requirements file
docker-compose exec python-dev pip freeze > requirements.txt
```

### 2. Project-Specific Packages
```bash
# Install for a specific project
docker-compose exec python-dev pip install fastapi

# Create project requirements
docker-compose exec python-dev pip freeze > projects/MyProject/requirements.txt
```

### 3. Development Dependencies
```bash
# Install development tools
docker-compose exec python-dev pip install pytest black flake8

# Update dev requirements
docker-compose exec python-dev pip freeze > requirements-dev.txt
```

### 4. Rebuild After Changes
```bash
# After adding new dependencies, rebuild the container
./dev.sh build
```

## Troubleshooting

### Package Not Found After Installation
```bash
# Rebuild the container
./dev.sh build
```

### Update All Packages
```bash
# Update pip first
docker-compose exec python-dev pip install --upgrade pip

# Update from requirements
docker-compose exec python-dev pip install --upgrade -r requirements.txt
docker-compose exec python-dev pip install --upgrade -r requirements-dev.txt
```

### Clean Installation
```bash
# Remove all packages and reinstall
./dev.sh clean
./dev.sh build
```

## Why This Approach?

- **Simple**: Direct Docker commands are easy to understand
- **Transparent**: You see exactly what's happening
- **Reliable**: No complex scripts that can break
- **Standard**: Uses standard pip commands everyone knows
- **Flexible**: Easy to customize for specific needs

## Summary

**Use Docker commands directly** for package management. It's simple, reliable, and transparent. The Make shortcuts are just conveniences - the underlying Docker commands are what actually matter.

```bash
# The essential commands you need:
docker-compose exec python-dev pip install <package>
docker-compose exec python-dev pip uninstall <package>
docker-compose exec python-dev pip list
docker-compose exec python-dev pip freeze
```