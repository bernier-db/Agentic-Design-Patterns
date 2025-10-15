from dotenv import load_dotenv
import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, Runnable

load_dotenv()

class LoggingWrapper(Runnable):
    """Wrapper class to add logging to chain execution."""
    
    def __init__(self, chain, chain_name: str):
        super().__init__()
        self.chain = chain
        self.chain_name = chain_name
    
    async def ainvoke(self, input_data, config=None):
        print(f"🚀 Starting {self.chain_name} chain...")
        try:
            result = await self.chain.ainvoke(input_data, config)
            print(f"✅ Completed {self.chain_name} chain")
            print(f"Result: {result}")
            return result
        except Exception as e:
            print(f"❌ Error in {self.chain_name} chain: {e}")
            print(f"Result: {result}")
            raise
    
    def invoke(self, input_data, config=None):
        print(f"🚀 Starting {self.chain_name} chain...")
        try:
            result = self.chain.invoke(input_data, config)
            print(f"✅ Completed {self.chain_name} chain")
            return result
        except Exception as e:
            print(f"❌ Error in {self.chain_name} chain: {e}")
            raise

class ParallelizationWorkflow:
    """Parallelization Workflow"""

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.7):
        """Initialize the workflow with LLM configuration."""
        try:
            self.llm = ChatOpenAI(model=model, temperature=temperature)
            self.str_parser = StrOutputParser()
        except Exception as e:
            print(f"Error initializing LLM: {e}")
            exit(1)

        asyncio.run(self.run_workflow())


    async def run_workflow(self):
        """Run the parallelization workflow."""
        print("🔗 Parallelization Workflow")
        print("Enter a comment :")
        comment = input("Comment: ")
        
        try:
            result = await self.build_parrallel_chain().ainvoke({"comment": comment})
            print("\n----- Result -----\n")
            print(result)
            
        except Exception as e:
            print(f"Error in workflow: {str(e)}")
            raise

    def build_parrallel_chain(self) :
        """Build the parallelization chain."""

        chains = self.define_independant_chains()
        map_chain = RunnableParallel({
            "sentiment": chains[0],
            "criteria": chains[1],
            "response": chains[2],
            "key_points": chains[3],
            "comment": RunnablePassthrough(),
        })
        
        synthesis_promp = ChatPromptTemplate.from_messages([
            ("system", """Based on the following information:
            Sentiment {sentiment}
            Criteria {criteria}
            Response {response}
            Key points {key_points}

            Synthesize the relationship between the sentiment, criteria and response in a short and concise manner.
            """),
            ("user", "{comment}"),
        ])
        return map_chain | synthesis_promp | self.llm | self.str_parser

    def define_independant_chains(self):
        """Define the independant chains for the parallelization workflow."""
        chains = []
        
        # Sentiment analysis chain
        sentiment_analysis_chain = (
            ChatPromptTemplate.from_messages([
                ("system", "Analyze the sentiment of the following comment:"),
                ("user", "{comment}"),
            ])
            | self.llm 
            | self.str_parser
        )
        chains.append(LoggingWrapper(sentiment_analysis_chain, "Sentiment Analysis"))

        # Criteria validation chain
        criteria_validation_chain = (
            ChatPromptTemplate.from_messages([
                ("system", """Validate if the following comment meets these criterias: 
                    - The comment must be objective
                    - The comment must be constructive
                    - The comment must be helpful
                    - The comment must be relevant
                """),
                ("user", "{comment}"),
            ])
            | self.llm 
            | self.str_parser
        )
        chains.append(LoggingWrapper(criteria_validation_chain, "Criteria Validation"))

        # Response generation chain
        terms_chain = (
            ChatPromptTemplate.from_messages([
                ("system", "Generate a diplomatic response to the following comment:"),
                ("user", "{comment}"),
            ])
            | self.llm
            | self.str_parser
        )
        chains.append(LoggingWrapper(terms_chain, "Response Generation"))

        # Key points extraction chain
        key_points_extraction_chain = (
            ChatPromptTemplate.from_messages([
                ("system", "Extract the key points from the following comment:"),
                ("user", "{comment}"),
            ])
            | self.llm
            | self.str_parser
        )
        chains.append(LoggingWrapper(key_points_extraction_chain, "Key Points Extraction"))

        return chains

if __name__ == "__main__":
    ParallelizationWorkflow()
