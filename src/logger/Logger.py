from datetime import datetime

class FileWriter:
    def __init__(self, path: str):
        self.path = path

    def append(self, line: str) -> None:
        with open(self.path, "a") as file:
            file.write(line + "\n")

class Logger:
    """A simple logging tool"""

    LEVELS = {"OK", "INFO", "WARN", "ERROR"}

    def __init__(self, name: str, path: str, level: str = "INFO", name_length: int = 20, log_to_console: bool = True):
        self.name = name
        self.level = level
        self.name_length = name_length
        self._writer = FileWriter(path=path)
        self._log_to_console = log_to_console
        self._count = 0

    @property
    def level(self) -> str:
        return self._level
    
    @level.setter
    def level(self, value: str) -> None:
        if value.upper() not in self.LEVELS:
            raise ValueError(f"Invalid type: {value!r}")
        self
        
    def _format_name(self, name: str) -> str:
        if len(name) > self.name_length:
            result = f"[{name[:self.name_length - 3]}...]"
        elif len(name) < self.name_length:
            result = f"[{name}]{" " * (self.name_length - len(name))}"
        else:
            result = f"[{name}]"

        return result

    def _format_level(self, level: str) -> str:
        num_to_add = len(max(self.LEVELS, key=len)) - len(level)
        return f"[{level}]{" " * num_to_add}"

    def log(self, message: str, level: str | None = None) -> None:
        l = (level or self.level).upper()
        line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {self._format_name(self.name)} {self._format_level(l)} {message}"

        if self._log_to_console:
            print(line)

        self._writer.append(line)
        self._count += 1

    