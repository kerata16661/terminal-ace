from unittest.mock import MagicMock, patch
from terminal_ace.config import Config

def test_agent_initialization():
    config = Config()
    with patch("terminal_ace.agent.DockerSandbox") as mock_sandbox:
        mock_sandbox.return_value = MagicMock()
        from terminal_ace.agent import TerminalAceAgent
        agent = TerminalAceAgent(config)
        assert agent is not None
        assert agent.config == config