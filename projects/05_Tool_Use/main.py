"""
Tool Use Workflow

This workflow demonstrates the Tool Use agentic design pattern using langchain.
"""

import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
    BaseMessage,
)
from dotenv import load_dotenv
from tools import search_database

load_dotenv()


class ToolUseWorkflow:
    """Tool Use Workflow"""

    _conversation_messages: list[BaseMessage] = []

    def __init__(self):
        """Initialize the workflow with LLM configuration."""
        try:
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
            self.llm = self.llm.bind_tools([search_database])
        except Exception as e:
            print(f"Error initializing LLM: {e}")
            exit(1)

    def run(self):
        """Run the workflow."""
        print("--- Running Tool Use Workflow ---\n")

        result = self._start_conversation()

        self._handle_tools_calls(result.tool_calls)

        final_response_message = self.llm.invoke(self._conversation_messages)

        final_response = final_response_message.content

        print(f"{'-' * 10} Workflow completed {'-' * 10}")
        print(f"Result: {final_response}")

    def _start_conversation(self):
        """Start the conversation."""
        self._conversation_messages.append(
            SystemMessage(
                content="You are an assistant that can search a database of books."
            )
        )
        self._conversation_messages.append(
            HumanMessage(
                content="How many copies of the book 'The Great Gatsby' are in the database?"
            )
        )
        result = self.llm.invoke(self._conversation_messages)
        self._conversation_messages.append(result)
        return result

    def _handle_tools_calls(self, tool_calls: list[dict]):
        """Handle tool calls."""
        for tool_call in tool_calls:
            self._handle_tool_call(tool_call)

    def _handle_tool_call(self, tool_call: dict):
        """Handle a tool call."""
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        if tool_name == "search_database":
            tool_result = search_database.invoke(tool_args)
            self._conversation_messages.append(
                ToolMessage(
                    content=json.dumps(tool_result), tool_call_id=tool_call["id"]
                )
            )
            print(f"Tool result: {tool_result}")
        else:
            print(f"Unknown tool: {tool_name}")


if __name__ == "__main__":
    workflow = ToolUseWorkflow()
    workflow.run()
