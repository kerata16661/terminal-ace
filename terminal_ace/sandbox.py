import subprocess
import docker
from docker.errors import NotFound

class DockerSandbox:
    def __init__(self, image: str):
        self.client = docker.from_env()
        self.image = image
        self.container = None

    def start(self):
        self.container = self.client.containers.run(
            self.image,
            detach=True,
            tty=True,
            stdin_open=True,
            working_dir="/workspace",
        )

    def execute(self, command: str) -> str:
        if not self.container:
            raise RuntimeError("Sandbox not started")
        exec_result = self.container.exec_run(
            f"bash -c '{command}'",
            workdir="/workspace",
        )
        return exec_result.output.decode("utf-8", errors="ignore")

    def observe(self) -> dict:
        pwd = self.execute("pwd").strip()
        ls = self.execute("ls -la").strip()
        git_status = self.execute("git status 2>/dev/null || echo 'not a repo'").strip()
        return {"pwd": pwd, "ls": ls, "git_status": git_status}

    def stop(self):
        if self.container:
            self.container.stop()
            self.container.remove()