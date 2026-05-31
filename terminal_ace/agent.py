from typing import Optional
from .sandbox import DockerSandbox
from .config import Config

SYSTEM_PROMPT = """You are a terminal agent. For each step, output:
THINK: <your reasoning>
COMMAND: <single bash command>
or FINAL_ANSWER: <answer>

Always observe the environment after each command.
If a command fails, analyze the error and fix it.
"""

class TerminalAceAgent:
    def __init__(self, config: Config):
        self.config = config
        self.sandbox = DockerSandbox(config.sandbox_image)
        self.history = []

    def run(self, instruction: str) -> str:
        self.sandbox.start()
        state = self.sandbox.observe()
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.history.append({"role": "user", "content": f"Instruction: {instruction}\nState: {state}"})

        for step in range(self.config.max_steps):
            # Model API'sine sorgu yapılacak (şimdilik mock)
            response = self._call_model(self.history)
            action = self._parse_action(response)

            if action["type"] == "command":
                output = self.sandbox.execute(action["content"])
                state = self.sandbox.observe()
                self.history.append({"role": "assistant", "content": response})
                self.history.append({"role": "user", "content": f"Command output: {output}\nNew state: {state}"})
                if output.strip() and "error" not in output.lower():
                    # Basit başarı kontrolü, task bitince FINAL_ANSWER dönecek
                    pass
            elif action["type"] == "final":
                self.sandbox.stop()
                return action["content"]

        self.sandbox.stop()
        return "Task not completed within max steps."

    def _call_model(self, messages):
        # TODO: Gerçek model API entegrasyonu
        return "FINAL_ANSWER: Hello World"

    def _parse_action(self, text):
        if "FINAL_ANSWER:" in text:
            return {"type": "final", "content": text.split("FINAL_ANSWER:")[-1].strip()}
        if "COMMAND:" in text:
            return {"type": "command", "content": text.split("COMMAND:")[-1].strip()}
        return {"type": "unknown", "content": text}