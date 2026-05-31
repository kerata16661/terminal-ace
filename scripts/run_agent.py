from terminal_ace.agent import TerminalAceAgent
from terminal_ace.config import Config

config = Config()
agent = TerminalAceAgent(config)
result = agent.run("List all files in the current directory and print today's date.")
print("Result:", result)