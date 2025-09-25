#!/usr/bin/env python3
"""
Prompt Chaining Example

This demonstrates a complete prompt chaining workflow for content creation:
1. Generate 5 topic ideas based on user's general interest
2. Generate detailed outline based on selected topic
3. Write draft sections for each outline point with context
4. Review and refine the complete draft

This pattern breaks down complex content creation into manageable, sequential steps.
"""

from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from dotenv import load_dotenv

load_dotenv()


class PromptChainingWorkflow:
    """Implements a complete prompt chaining workflow for content creation."""

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.7):
        """Initialize the workflow with LLM configuration."""
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.json_parser = JsonOutputParser()
        self.str_parser = StrOutputParser()

    def generate_topic_ideas(self, user_interest: str) -> List[str]:
        """Prompt 1: Generate 5 topic ideas"""
        prompt = ChatPromptTemplate.from_template(
            """
        Generate exactly 5 creative and engaging topic ideas based on this field of interest: {interest}
        
        Return the topics as a JSON array of strings. Each topic should be:
        - Specific and actionable
        - Interesting to the target audience
        - Suitable for creating detailed content
        
        Format: ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]
        """
        )

        chain = prompt | self.llm | self.json_parser
        topics = chain.invoke({"interest": user_interest})

        print("\n📝 Generated Topics:")
        for i, topic in enumerate(topics, 1):
            print(f"{i}. {topic}")

        return topics

    def select_topic(self, topics: List[str], auto_select: bool = False) -> str:
        """Allow user to select a topic or automatically choose the best one."""
        if auto_select:
            # Automatically select the first topic
            selected = topics[0]
            print(f"\n🤖 Auto-selected topic: {selected}")
            return selected

        while True:
            try:
                choice = input(f"\nSelect a topic (1-{len(topics)}): ").strip()
                index = int(choice) - 1
                if 0 <= index < len(topics):
                    selected = topics[index]
                    print(f"\n✅ Selected: {selected}")
                    return selected
                else:
                    print(f"Please enter a number between 1 and {len(topics)}")
            except ValueError:
                print("Please enter a valid number")

    def generate_outline(self, topic: str) -> List[str]:
        """Prompt 2: Generate detailed outline based on selected topic."""
        prompt = ChatPromptTemplate.from_template(
            """
        Create a detailed, comprehensive outline for an article about: {topic}
        
        The outline should include:
        - Introduction section
        - 3-5 main content sections with specific subtopics
        - Conclusion section
        
        Return as a JSON array of strings, where each string is a section heading.
        Each section should be substantial enough to write 2-3 paragraphs about.
        
        Format: ["Section 1", "Section 2", "Section 3", ...]
        """
        )

        chain = prompt | self.llm | self.json_parser
        outline = chain.invoke({"topic": topic})

        print("\n📋 Generated Outline:")
        for i, section in enumerate(outline, 1):
            print(f"{i}. {section}")

        return outline

    def write_draft_sections(self, topic: str, outline: List[str]) -> str:
        """Prompts 3-4: Write draft sections for each outline point with context."""
        complete_draft = ""

        for i, section in enumerate(outline):
            print(f"\n✍️  Writing section {i+1}/{len(outline)}: {section}")

            # Build context from previous sections
            context = (
                f"Topic: {topic}\n\nPrevious sections:\n{complete_draft}"
                if complete_draft
                else f"Topic: {topic}"
            )

            prompt = ChatPromptTemplate.from_template(
                """
            Write a detailed draft section for: {section}
            
            Context:
            {context}
            
            Requirements:
            - Write 2-3 substantial paragraphs
            - Maintain consistency with previous sections
            - Use engaging, informative tone
            - Include specific examples or details where appropriate
            - Ensure smooth transition from previous content
            
            Focus on this section only, but ensure it flows naturally with the overall piece.
            """
            )

            chain = prompt | self.llm | self.str_parser
            section_content = chain.invoke({"section": section, "context": context})

            # Add section to complete draft
            complete_draft += f"\n## {section}\n\n{section_content}\n"

        return complete_draft

    def review_and_refine(self, topic: str, draft: str) -> str:
        """Prompt 5: Review and refine the complete draft for coherence, tone, and grammar."""
        print("\n🔍 Reviewing and refining the complete draft...")

        prompt = ChatPromptTemplate.from_template(
            """
        Review and refine this complete article draft about: {topic}
        
        Draft:
        {draft}
        
        Please improve the article by:
        1. Ensuring smooth transitions between sections
        2. Maintaining consistent tone throughout
        3. Fixing any grammar or style issues
        4. Improving clarity and flow
        5. Adding or enhancing examples where helpful
        6. Ensuring the conclusion ties everything together
        
        Return the refined version of the complete article.
        """
        )

        chain = prompt | self.llm | self.str_parser
        refined_draft = chain.invoke({"topic": topic, "draft": draft})

        return refined_draft

    def run_complete_workflow(
        self, user_interest: str, auto_select: bool = False
    ) -> Dict[str, Any]:
        """Run the complete prompt chaining workflow."""
        print("🔗 Prompt Chaining Workflow")
        print("=" * 50)

        try:
            # Step 1: Generate topic ideas
            print(f"\n📝 Step 1: Generating topic ideas for '{user_interest}'...")
            topics = self.generate_topic_ideas(user_interest)

            # Step 2: Select topic
            print("\n🎯 Step 2: Topic selection...")
            selected_topic = self.select_topic(topics, auto_select)

            # Step 3: Generate outline
            print("\n📋 Step 3: Creating detailed outline...")
            outline = self.generate_outline(selected_topic)

            # Step 4: Write draft sections
            print("\n✍️  Step 4: Writing draft sections...")
            draft = self.write_draft_sections(selected_topic, outline)

            # Step 5: Review and refine
            print("\n🔍 Step 5: Reviewing and refining...")
            final_draft = self.review_and_refine(selected_topic, draft)

            print("\n✅ Workflow completed successfully!")

            return {
                "user_interest": user_interest,
                "generated_topics": topics,
                "selected_topic": selected_topic,
                "outline": outline,
                "draft": draft,
                "final_draft": final_draft,
            }

        except Exception as e:
            print(f"\n❌ Error in workflow: {str(e)}")
            raise


def main():
    """Main function demonstrating the prompt chaining workflow."""
    workflow = PromptChainingWorkflow()

    # Get user input
    user_interest = input("Enter your field of interest: ").strip()
    if not user_interest:
        user_interest = "artificial intelligence"
        print(f"Using default interest: {user_interest}")

    # Ask if user wants auto-selection
    auto_mode = input("Auto-select best topic? (y/n): ").strip().lower() == "y"

    # Run the complete workflow
    result = workflow.run_complete_workflow(user_interest, auto_mode)

    # Display final result
    print("\n🎯 Final Article:")
    print("=" * 50)
    print(result["final_draft"])

    print("\n📊 Workflow Summary:")
    print(f"• Interest: {result['user_interest']}")
    print(f"• Selected Topic: {result['selected_topic']}")
    print(f"• Outline Sections: {len(result['outline'])}")
    print(f"• Final Word Count: {len(result['final_draft'].split())} words")


if __name__ == "__main__":
    main()
