# Prompt Chaining

This project demonstrates the **Prompt Chaining** agentic design pattern through a complete content creation workflow.

## Overview

Prompt chaining involves breaking down complex tasks into smaller, manageable prompts that are executed sequentially. The output of one prompt becomes the input for the next, creating a chain of reasoning and action.

## Pattern Benefits

- **Modularity**: Complex tasks are broken into manageable pieces
- **Traceability**: Each step in the chain can be monitored and debugged
- **Flexibility**: Individual steps can be modified without affecting the entire chain
- **Reusability**: Chain steps can be reused in different combinations
- **Context Preservation**: Each step builds upon previous results

## Implementation: Content Creation Workflow

This implementation demonstrates a complete 5-step prompt chaining workflow for content creation:

### Step 1: Topic Generation
**Prompt**: Generate 5 topic ideas based on user's general interest
- Takes user's field of interest as input
- Generates 5 creative, actionable topic ideas
- Returns structured JSON array of topics

### Step 2: Topic Selection
**Processing**: Allow user to select one idea or automatically choose the best one
- Interactive selection with validation
- Auto-selection mode for automated workflows
- Returns selected topic for next step

### Step 3: Outline Generation
**Prompt**: Generate detailed outline based on selected topic
- Creates comprehensive article structure
- Includes introduction, main sections, and conclusion
- Returns structured outline as JSON array

### Step 4: Draft Writing
**Prompts**: Write draft sections for each outline point with context
- Iteratively writes each section
- Provides previous sections as context for continuity
- Maintains consistent tone and flow
- Returns complete draft

### Step 5: Review and Refinement
**Prompt**: Review and refine complete draft for coherence, tone, and grammar
- Analyzes entire article for improvements
- Ensures smooth transitions between sections
- Fixes grammar and style issues
- Returns polished final article

## Architecture

The implementation uses a `PromptChainingWorkflow` class that encapsulates:

- **LLM Configuration**: Configurable model and temperature settings
- **Individual Methods**: Each prompt step as a separate, testable method
- **Result Tracking**: Complete workflow results with intermediate outputs

## Running the Example

### Interactive Mode
```bash
# From the project root
python projects/01_Prompt_Chaining/main.py
```

### Demo Mode
```bash
# Run the demo script
python projects/01_Prompt_Chaining/demo.py
```

### Using Development Scripts
```bash
# From the project root
./dev.sh run "Prompt Chaining"

# Or using Make
make run PROJECT="Prompt Chaining"
```

## Testing

Run the comprehensive test suite:

```bash
cd projects/Prompt_Chaining
python -m pytest tests/test_main.py -v
```

## Key Features

- **Well-Encapsulated**: Each method has a single responsibility
- **Testable**: Comprehensive unit tests with mocking
- **User-Friendly**: Clear progress indicators and error messages
- **Flexible**: Supports both interactive and automated modes
- **Robust**: Error handling and input validation

## Configuration

The workflow can be configured with different models and parameters:

```python
workflow = PromptChainingWorkflow(
    model="gpt-4o-mini",  # or "gpt-3.5-turbo"
    temperature=0.7       # creativity level
)
```

## Example Output

The workflow produces:
- Generated topic ideas
- Selected topic
- Detailed outline
- Complete draft
- Refined final article
- Workflow summary with metrics
