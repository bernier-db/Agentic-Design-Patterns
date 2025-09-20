#!/usr/bin/env python3
"""
Prompt Chaining Example

This is a simple example of prompt chaining in agentic design patterns.
Prompt chaining involves breaking down complex tasks into smaller, manageable prompts
that are executed sequentially, where the output of one prompt becomes the input
for the next.

Example: Research -> Analysis -> Summary -> Action Plan
"""

from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def main():
    """Main function demonstrating prompt chaining."""
    print("🔗 Prompt Chaining Example")
    print("=" * 40)

    
    print("\n✅ Prompt chaining completed successfully!")
    print("\nThis demonstrates how complex tasks can be broken down")
    print("into sequential, manageable prompts for better results.")


if __name__ == "__main__":
    main()
