"""
Tool Use Workflow

This workflow demonstrates the Tool Use agentic design pattern using langchain.
"""

import json
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool as langchain_tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

class ToolUseWorkflow:
    """Tool Use Workflow"""
    
    _messages = []

    def __init__(self):
        """Initialize the workflow with LLM configuration."""
        try:
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        except Exception as e:
            print(f"Error initializing LLM: {e}")
            exit(1)

    def run(self):
        """Run the workflow."""
        print("🔗 Tool Use Workflow")
        prompt = self.define_agent_prompt()
        llm_with_tools = self.llm.bind_tools([self.search_database])
        result = (prompt | llm_with_tools).invoke({"input": "What are the books about the Great Gatsby?"})
        self._messages.append(result)

        for tool_call in result.tool_calls:
            # View tool calls made by the model
            print(f"Tool: {tool_call['name']}")
            print(f"Args: {tool_call['args']}")
            if tool_call['name'] == 'search_database':
                result = self.search_database(tool_call['args']['query'])
                self._messages.append(("tool", {
                    "name": tool_call['name'],
                    "args": tool_call['args'],
                    "result": result
                }))
                print(f"Result: {result}")

        final_response = llm_with_tools.invoke(self._messages)

        print(f"{'-' * 10} Workflow completed {'-' * 10}")
        print(f"Result: {final_response}")

    def define_agent_prompt(self):
        """Define the agent."""
        self._messages.append(("system", "You are a helpful assistant that can search a database of books."))
        self._messages.append(("user", "{input}"))
        return ChatPromptTemplate.from_messages(self._messages)

    @langchain_tool
    def search_database(self, query: str) -> str:
        # Docstring and type hints are important for the agent to understand the tool properly
        """
        Fake tool that would search a database of books using the query
        Args:
            query: The query to search the database for
        Returns:
            A list of dictionaries with the title and author of the books.
            Properties:
                title: The title of the book
                author: The author of the book
        """

        print(f"{'-' * 10} Tool called - Searching database for: {query} {'-' * 10}")
        fake_results = [
            {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
            {"title": "1984", "author": "George Orwell"},
            {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
        ]
        return json.dumps(fake_results)



if __name__ == "__main__":
    workflow = ToolUseWorkflow()
    workflow.run()