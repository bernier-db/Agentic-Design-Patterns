# Prompt Chaining

This project demonstrates the **Prompt Chaining** agentic design pattern.

## Overview

Prompt chaining involves breaking down complex tasks into smaller, manageable prompts that are executed sequentially. The output of one prompt becomes the input for the next, creating a chain of reasoning and action.

## Pattern Benefits

- **Modularity**: Complex tasks are broken into manageable pieces
- **Traceability**: Each step in the chain can be monitored and debugged
- **Flexibility**: Individual steps can be modified without affecting the entire chain
- **Reusability**: Chain steps can be reused in different combinations

## Example Chain

```
Research → Analysis → Summary → Action Plan
```

1. **Research**: Gather information about the topic
2. **Analysis**: Process and analyze the gathered data
3. **Summary**: Create a concise summary of findings
4. **Action Plan**: Generate actionable recommendations

## Running the Example

```bash
# From the project root
./dev.sh run "Prompt Chaining"

# Or using Make
make run PROJECT="Prompt Chaining"
```

## Implementation Notes

This is a simple demonstration. In a real implementation, you would:

- Use actual AI/LLM calls for each step
- Implement error handling and retry logic
- Add validation between steps
- Store intermediate results
- Implement parallel processing where possible
