from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import AgentAction, AgentFinish
from typing import List, Union, Dict, Any
import re
import json
from abc import ABC, abstractmethod
from config import OPENAI_API_KEY, MODEL_NAME, AGENT_CONFIG

class BaseAgent(ABC):
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.llm = ChatOpenAI(
            temperature=0,
            openai_api_key=OPENAI_API_KEY,
            model_name=MODEL_NAME
        )
        self.tools = self._get_tools()
        self.prompt = self._create_prompt()
        self.output_parser = self._create_output_parser()
        self.agent = self._create_agent()
        self.agent_executor = self._create_agent_executor()

    @abstractmethod
    def _get_tools(self) -> List[Tool]:
        """Return list of tools available to the agent"""
        pass

    @abstractmethod
    def _create_prompt(self) -> StringPromptTemplate:
        """Create the prompt template for the agent"""
        pass

    def _create_output_parser(self):
        """Create parser for the agent's output"""
        class AgentOutputParser:
            def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
                if "Final Answer:" in text:
                    return AgentFinish(
                        return_values={"output": text.split("Final Answer:")[-1].strip()},
                        log=text
                    )

                regex = r"Action: (.*?)[\n]*Action Input: (.*)"
                match = re.search(regex, text, re.DOTALL)
                
                if not match:
                    raise ValueError(f"Could not parse agent output: {text}")

                action = match.group(1).strip()
                action_input = match.group(2).strip()

                return AgentAction(
                    tool=action,
                    tool_input=action_input.strip(" ").strip('"'),
                    log=text
                )

        return AgentOutputParser()

    def _create_agent(self) -> LLMSingleActionAgent:
        """Create the agent"""
        return LLMSingleActionAgent(
            llm_chain=LLMChain(llm=self.llm, prompt=self.prompt),
            output_parser=self.output_parser,
            stop=["\nObservation:"],
            allowed_tools=[tool.name for tool in self.tools]
        )

    def _create_agent_executor(self) -> AgentExecutor:
        """Create the agent executor"""
        return AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=self.tools,
            verbose=AGENT_CONFIG['verbose'],
            max_iterations=AGENT_CONFIG['max_iterations']
        )

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results"""
        try:
            result = await self.agent_executor.arun(input_data)
            return self._format_output(result)
        except Exception as e:
            return {
                'status': 'error',
                'agent': self.agent_name,
                'error': str(e)
            }

    def _format_output(self, result: str) -> Dict[str, Any]:
        """Format the agent's output"""
        try:
            return {
                'status': 'success',
                'agent': self.agent_name,
                'result': json.loads(result) if isinstance(result, str) else result
            }
        except json.JSONDecodeError:
            return {
                'status': 'success',
                'agent': self.agent_name,
                'result': result
            }

    @abstractmethod
    async def handle_callback(self, message: Dict[str, Any]) -> None:
        """Handle callbacks from other agents"""
        pass
