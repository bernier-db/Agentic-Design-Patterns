"""
Routing Example

This example demonstrates the **Routing** agentic design pattern through a coordinator agent that determines which handler should process the user's request.

"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableBranch, RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()


class RoutingWorkflow:
    """Routing Workflow"""

    def __init__(self, model: str = "gpt-4.1-nano", temperature: float = 0):
        try:
            self.llm = ChatOpenAI(model=model, temperature=temperature)
        except Exception as e:
            print(f"Error initializing LLM: {e}")
            exit(1)
        self.define_branches()
        self.coordinator_router_chain = self.create_coordinator_router_chain()
        self.delegation_branch = self.create_delegation_branch()

    def define_branches(self):
        """Define the branches for the routing workflow"""
        self.branches = {
            "weather": RunnablePassthrough.assign(
                output=lambda x: self.weather_handler(x["request"]["request"])
            ),
            "news": RunnablePassthrough.assign(
                output=lambda x: self.news_handler(x["request"]["request"])
            ),
            "stock_market": RunnablePassthrough.assign(
                output=lambda x: self.stock_market_handler(x["request"]["request"])
            ),
            "unclear": RunnablePassthrough.assign(
                output=lambda x: self.unclear_handler(x["request"]["request"])
            ),
        }

    def start_workflow(self):
        """Start the routing workflow"""
        request = self.prompt_for_input()
        return self.run_coordinator_agent(request)

    def run_coordinator_agent(self, request: str):
        """Run the coordinator agent"""
        agent: Runnable = (
            {
                "decision": self.coordinator_router_chain,
                "request": RunnablePassthrough(),
            }
            | self.delegation_branch
            | (lambda x: x["output"])
        )

        return agent.invoke({"request": request})

    def create_coordinator_router_chain(self) -> Runnable:
        """Create the coordinator router chain"""
        return self.build_coordinator_router_prompt() | self.llm | StrOutputParser()

    def build_coordinator_router_prompt(self) -> ChatPromptTemplate:
        """Build the coordinator router prompt"""
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Analyze the user's request and determine which handler should process it :
            - If the user is asking about the weather, output "weather".
            - If the user is asking about the news, output "news".
            - If the user is asking about the stock market, output "stock_market".
            - If the request is unclear or not related to the above topics, output "unclear".

            IMPORTANT: Only output one word: the name of the specialist. Possible values are: "weather", "news", "stock_market", "unclear".
            """,
                ),
                ("user", "{request}"),
            ]
        )

    def create_delegation_branch(self) -> RunnableBranch:
        """Create the delegation branch as a RunnableBranch"""
        return RunnableBranch(
            (lambda x: x["decision"].strip() == "weather", self.branches["weather"]),
            (lambda x: x["decision"].strip() == "news", self.branches["news"]),
            (
                lambda x: x["decision"].strip() == "stock_market",
                self.branches["stock_market"],
            ),
            self.branches["unclear"],
        )

    def weather_handler(self, request: str) -> str:
        """Handler for weather requests"""
        print("Passing request to weather handler")
        return f"Weather handler: {request}"

    def news_handler(self, request: str) -> str:
        """Handler for news requests"""
        print("Passing request to news handler")
        return f"News handler: {request}"

    def stock_market_handler(self, request: str) -> str:
        """Handler for stock market requests"""
        print("Passing request to stock market handler")
        return f"Stock market handler: {request}"

    def unclear_handler(self, request: str) -> str:
        """Handler for unclear requests"""
        print("Passing request to unclear handler")
        return f"Unclear handler: {request}. Please clarify."

    def prompt_for_input(self) -> str:
        """Prompt for input"""
        return input("Enter your request: ")


def main():
    workflow = RoutingWorkflow()
    result = workflow.start_workflow()
    print(result)


if __name__ == "__main__":
    main()
