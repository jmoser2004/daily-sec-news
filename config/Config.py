import yaml
import copy
from typing import Dict
from src.logger import Logger

class Config:
    def __init__(self, path: str, logger: Logger | None = None):
        self.config = None
        self.base = None
        self.logger = logger

        try:
            with open(file=path, mode="r") as file:
                self.config = yaml.safe_load(file)
            
            self.base = copy.deepcopy(self.config)
        except FileNotFoundError:
            if self.logger is not None:
                self.logger.log(message=f"Path {path} not found", level="ERROR")
        except PermissionError:
            if self.logger is not None:
                self.logger.log(message=f"Permission denied for path {path}", level="ERROR")
        except Exception as e:
            if self.logger is not None:
                self.logger.log(message=f"Error: {e}", level="ERROR")

    def set_base(self, new_base: str) -> bool:
        yml_branches = new_base.split(":")
        temp_config = copy.deepcopy(self.base)

        try:
            for branch in yml_branches:
                temp_config = temp_config[branch]
            self.config = temp_config
            return True
        except KeyError:
            if self.logger is not None:
                self.logger.log(message=f"A branch in {new_base} does not exist", level="ERROR")
            return False
        except TypeError:
            if self.logger is not None:
                self.logger.log(message=f"Cannot index all the way into {new_base}", level="ERROR")
            return False
        except Exception as e:
            if self.logger is not None:
                self.logger.log(message=f"Error: {e}", level="ERROR")
            return False
        
    def get_config(self, path: str | None = None, relative: bool = True) -> Dict | None:
        if path is None:
            if self.config is not None:
                return self.config
            if self.logger is not None:
                self.logger.log(message=f"Config at default path is None", level="WARN")
            return None
        
        yml_branches = path.split(":")

        if relative:
            temp_config = copy.deepcopy(self.config)
        else:
            temp_config = copy.deepcopy(self.base)
        
        try:
            for branch in yml_branches:
                temp_config = temp_config[branch]
            return temp_config
        except KeyError:
            if self.logger is not None:
                self.logger.log(message=f"A branch in {path} does not exist", level="ERROR")
            return False
        except TypeError:
            if self.logger is not None:
                self.logger.log(message=f"Cannot index all the way into {path}", level="ERROR")
            return False
        except Exception as e:
            if self.logger is not None:
                self.logger.log(message=f"Error: {e}", level="ERROR")
            return False