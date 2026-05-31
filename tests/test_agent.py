from terminal_ace.agent import TerminalAceAgent
from terminal_ace.config import Config

def test_agent_initialization():
    config = Config()
    agent = TerminalAceAgent(config)
    assert agent is not None