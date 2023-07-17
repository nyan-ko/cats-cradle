from abc import ABC, abstractmethod

from services.request_map import RequestMapResult

class ControllerABC(ABC):
    """ Interface for defining a controller.
    """
    
    @abstractmethod
    def request_map(self) -> RequestMapResult:
        pass