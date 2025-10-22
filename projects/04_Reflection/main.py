"""
Reflection Workflow

This workflow demonstrates the Reflection agentic design pattern through 
a complete reflection process.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class ReflectionWorkflow:
    """Reflection Workflow"""

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.1):
        """Initialize the workflow with LLM configuration."""
        try:
            self.llm = ChatOpenAI(model=model, temperature=temperature)
        except Exception as e:
            print(f"Error initializing LLM: {e}")
            exit(1)

    def run_workflow(self):
        """Run the workflow."""
        print("🔗 Reflection Workflow")
        return self.run_reflection_loop()

    def run_reflection_loop(self):
        task_prompt = """
            Your task is to write a 10 questions questionnaire about the renaissance.
            It should test understanding of the period and not only recall facts.

            The questions should be in the following format:
            Question {number}: {question}

            The answers should be in the following format:
            Answer {number}: {answer}
            """
        
        max_iteration = 3
        current_questionnaire = ""
        message_history = [HumanMessage(content=task_prompt)]
        
        for i in range(max_iteration):
            print("\n" + "=" *25 + f"Reflexion loop: Iteration {i+1}" + "=" *25)

            if(i == 0):
                print("\n >>> Stage 1: Generating initial questionnaire")
                response = self.llm.invoke(message_history)
                current_questionnaire = response.content
            else:
                print("\n >>> Stage 1: Refining questionnaire based on previous critiques")
                message_history.append(HumanMessage(content="Please refine the questionnaire using the critique provided"))
                response = self.llm.invoke(message_history)
                current_questionnaire = response.content 

            print("\n--- Generated Questionnaire (v" + str(i+1) + ") ---\n")

            print("\n>>>Stage 2: Reflecting on the generated questionnaire...")

            reflector_prompt = [SystemMessage(content="""
                    You are a historian and an expert in the Renaissance.
                    Your role is to perform a meticulous questionnaire review.
                    Critically evaluate the provided questionnaire based  on the original task requirements.
                    Look for questions that are not relevant to the Renaissance, are based on fact recalls and not understanding, to hard for a high school level knowledge, and areas for improvement.
                    Focus on critiquing, not rewriting, fixing nor answering the question. You are here to comment on how areas of improvement.
                    Be precise on which questions to improve and how to improve them.

                    ## Output
                    If the questionnaire meets all requirements, respond with the single phrase 'RESULT_IS_PERFECT'.
                    Otherwise, provide a bulleted list of your critique.
            """),
            HumanMessage(content=f"Original Task:\n{task_prompt}\n\nQuestionnaire to review:\n{current_questionnaire}")
            ]

            critique_response = self.llm.invoke(reflector_prompt)
            critique = critique_response.content

            if("RESULT_IS_PERFECT" in critique):
                print("\n---Critique---\nNo further critique found. The questionnaire is satisfactory.")
                break

            print("\n--- Critique ---\n" + critique)
            message_history.append(HumanMessage(content=f"Critique of the previous questionnaire:\n{critique}"))

        print("\n" + "=" *25 + "Final result" + "=" *25)
        print("\nFinal refined questionnaire after the reflection process:\n")
        print(current_questionnaire)
        

if __name__ == "__main__":
    workflow = ReflectionWorkflow()
    workflow.run_workflow()