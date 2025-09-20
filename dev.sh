#!/bin/bash

# Development script for Agentic Design Patterns repository.
# Provides easy commands to manage Docker development environment and run projects.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$PROJECT_ROOT/docker-compose.yml"
CONTAINER_NAME="agentic-design-patterns-dev"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_command() {
    echo -e "${BLUE}[CMD]${NC} $1"
}

# Function to run commands
run_command() {
    local cmd="$1"
    local check_error="${2:-true}"
    
    print_command "$cmd"
    
    if [ "$check_error" = "true" ]; then
        eval "$cmd"
    else
        eval "$cmd" || true
    fi
}

# Function to check if container is running
is_container_running() {
    docker-compose -f "$COMPOSE_FILE" ps python-dev | grep -q "Up"
}

# Function to ensure container is running
ensure_container_running() {
    if ! is_container_running; then
        print_warning "Container is not running. Starting it now..."
        up
    fi
}

# Build the development environment
build() {
    print_status "Building development environment..."
    run_command "docker-compose -f '$COMPOSE_FILE' build"
    print_status "✅ Development environment built successfully!"
}

# Start the development environment
up() {
    print_status "Starting development environment..."
    run_command "docker-compose -f '$COMPOSE_FILE' up -d"
    print_status "✅ Development environment started!"
    print_status "📝 Use './dev.sh shell' to enter the container"
    print_status "🔧 Use './dev.sh run <project>' to run a specific project"
}

# Stop the development environment
down() {
    print_status "Stopping development environment..."
    run_command "docker-compose -f '$COMPOSE_FILE' down"
    print_status "✅ Development environment stopped!"
}

# Enter the development container shell
shell() {
    ensure_container_running
    print_status "Entering development container..."
    run_command "docker-compose -f '$COMPOSE_FILE' exec python-dev bash" false
}

# Run a specific project or command in the container
run() {
    local project_path="$1"
    local command="$2"
    
    if [ -z "$project_path" ]; then
        print_status "Available projects:"
        list_projects
        return
    fi
    
    local project_dir="$PROJECT_ROOT/projects/$project_path"
    if [ ! -d "$project_dir" ]; then
        print_error "Project '$project_path' not found!"
        return 1
    fi
    
    ensure_container_running
    
    # Convert host path to container path
    local container_project_dir="/workspace/projects/$project_path"
    
    if [ -n "$command" ]; then
        print_status "Running command in project: $project_path"
        run_command "docker-compose -f '$COMPOSE_FILE' exec -w '$container_project_dir' python-dev $command" false
    else
        # Try to find main.py or run.py
        local main_files=("main.py" "run.py" "app.py")
        local main_file=""
        
        for file in "${main_files[@]}"; do
            if [ -f "$project_dir/$file" ]; then
                main_file="$file"
                break
            fi
        done
        
        if [ -z "$main_file" ]; then
            print_error "No main file found in '$project_path'. Please specify a command."
            return 1
        fi
        
        print_status "Running project: $project_path"
        run_command "docker-compose -f '$COMPOSE_FILE' exec -w '$container_project_dir' python-dev python $main_file" false
    fi
}

# Run a project in debug mode
debug() {
    local project_path="$1"
    local port="${2:-5678}"
    
    if [ -z "$project_path" ]; then
        print_error "Project name is required for debug mode!"
        return 1
    fi
    
    local project_dir="$PROJECT_ROOT/projects/$project_path"
    if [ ! -d "$project_dir" ]; then
        print_error "Project '$project_path' not found!"
        return 1
    fi
    
    ensure_container_running
    
    print_status "Starting debug session for project: $project_path"
    print_status "🔧 Debug port: $port"
    print_status "📝 Attach your debugger to localhost:$port"
    
    # Convert host path to container path
    local container_project_dir="/workspace/projects/$project_path"
    
    # Find main file
    local main_files=("main.py" "run.py" "app.py")
    local main_file=""
    
    for file in "${main_files[@]}"; do
        if [ -f "$project_dir/$file" ]; then
            main_file="$file"
            break
        fi
    done
    
    if [ -z "$main_file" ]; then
        print_error "No main file found in '$project_path'"
        return 1
    fi
    
    run_command "docker-compose -f '$COMPOSE_FILE' exec -w '$container_project_dir' python-dev python -m debugpy --listen 0.0.0.0:$port --wait-for-client $main_file" false
}

# Run tests for a project or all projects
test() {
    local project_path="$1"
    
    ensure_container_running
    
    if [ -n "$project_path" ]; then
        local project_dir="$PROJECT_ROOT/projects/$project_path"
        if [ ! -d "$project_dir" ]; then
            print_error "Project '$project_path' not found!"
            return 1
        fi
        
        local test_dir="$project_dir/tests"
        if [ ! -d "$test_dir" ]; then
            print_error "No tests directory found in '$project_path'"
            return 1
        fi
        
        print_status "Running tests for project: $project_path"
        local container_project_dir="/workspace/projects/$project_path"
        run_command "docker-compose -f '$COMPOSE_FILE' exec -w '$container_project_dir' python-dev python -m pytest tests" false
    else
        print_status "Running tests for all projects..."
        run_command "docker-compose -f '$COMPOSE_FILE' exec python-dev python -m pytest" false
    fi
}

# Run linting for a project or all projects
lint() {
    local project_path="$1"
    
    ensure_container_running
    
    if [ -n "$project_path" ]; then
        local project_dir="$PROJECT_ROOT/projects/$project_path"
        if [ ! -d "$project_dir" ]; then
            print_error "Project '$project_path' not found!"
            return 1
        fi
        
        print_status "Running linting for project: $project_path"
        local container_project_dir="/workspace/projects/$project_path"
        run_command "docker-compose -f '$COMPOSE_FILE' exec -w '$container_project_dir' python-dev python -m flake8 ." false
    else
        print_status "Running linting for all projects..."
        run_command "docker-compose -f '$COMPOSE_FILE' exec python-dev python -m flake8 ." false
    fi
}

# Format code for a project or all projects
format_code() {
    local project_path="$1"
    
    ensure_container_running
    
    if [ -n "$project_path" ]; then
        local project_dir="$PROJECT_ROOT/projects/$project_path"
        if [ ! -d "$project_dir" ]; then
            print_error "Project '$project_path' not found!"
            return 1
        fi
        
        print_status "Formatting code for project: $project_path"
        local container_project_dir="/workspace/projects/$project_path"
        run_command "docker-compose -f '$COMPOSE_FILE' exec -w '$container_project_dir' python-dev python -m black ." false
    else
        print_status "Formatting code for all projects..."
        run_command "docker-compose -f '$COMPOSE_FILE' exec python-dev python -m black ." false
    fi
}

# List all available projects
list_projects() {
    local projects=()
    
    # Find all directories in the projects/ directory that contain Python main files
    if [ -d "$PROJECT_ROOT/projects" ]; then
        while IFS= read -r -d '' dir; do
            local dirname=$(basename "$dir")
            if [[ "$dirname" != "." && "$dirname" != ".." && ! "$dirname" =~ ^\..*$ ]]; then
                projects+=("$dirname")
            fi
        done < <(find "$PROJECT_ROOT/projects" -maxdepth 1 -type d -name ".*" -prune -o -type d -print0)
    fi
    
    # Filter projects that have main files
    local valid_projects=()
    for project in "${projects[@]}"; do
        local project_dir="$PROJECT_ROOT/projects/$project"
        if [ -d "$project_dir" ]; then
            local main_files=("main.py" "run.py" "app.py")
            for file in "${main_files[@]}"; do
                if [ -f "$project_dir/$file" ]; then
                    valid_projects+=("$project")
                    break
                fi
            done
        fi
    done
    
    if [ ${#valid_projects[@]} -gt 0 ]; then
        print_status "Available projects:"
        for project in "${valid_projects[@]}"; do
            echo "  📁 $project"
        done
    else
        print_warning "No projects found. Create a directory in projects/ with main.py, run.py, or app.py"
    fi
}

# Show container logs
logs() {
    run_command "docker-compose -f '$COMPOSE_FILE' logs -f" false
}

# Clean up containers and volumes
clean() {
    print_status "Cleaning up containers and volumes..."
    run_command "docker-compose -f '$COMPOSE_FILE' down -v --remove-orphans"
    run_command "docker system prune -f"
    print_status "✅ Cleanup completed!"
}

# Show help
show_help() {
    echo "Development manager for Agentic Design Patterns"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Available commands:"
    echo "  build                    Build the development environment"
    echo "  up                       Start the development environment"
    echo "  down                     Stop the development environment"
    echo "  shell                    Enter the development container shell"
    echo "  run <project> [command]   Run a specific project (optional command)"
    echo "  debug <project> [port]    Run a project in debug mode (default port: 5678)"
    echo "  test [project]            Run tests (optionally for specific project)"
    echo "  lint [project]            Run linting (optionally for specific project)"
    echo "  format [project]          Format code (optionally for specific project)"
    echo "  list                      List available projects"
    echo "  logs                     Show container logs"
    echo "  clean                    Clean up containers and volumes"
    echo "  help                     Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build                 # Build the development environment"
    echo "  $0 up                    # Start the development environment"
    echo "  $0 shell                 # Enter the container shell"
    echo "  $0 run \"Prompt Chaining\" # Run the Prompt Chaining project"
    echo "  $0 debug \"My Project\"    # Debug My Project on port 5678"
    echo "  $0 test \"My Project\"     # Test My Project"
    echo "  $0 lint                  # Lint all projects"
    echo "  $0 format \"My Project\"   # Format My Project code"
}

# Main function
main() {
    local command="${1:-help}"
    
    case "$command" in
        "build")
            build
            ;;
        "up")
            up
            ;;
        "down")
            down
            ;;
        "shell")
            shell
            ;;
        "run")
            run "$2" "$3"
            ;;
        "debug")
            debug "$2" "$3"
            ;;
        "test")
            test "$2"
            ;;
        "lint")
            lint "$2"
            ;;
        "format")
            format_code "$2"
            ;;
        "list")
            list_projects
            ;;
        "logs")
            logs
            ;;
        "clean")
            clean
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"

