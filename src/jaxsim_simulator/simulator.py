import jaxsim
import jaxsim.api as js
import logging
from typing import List

class Simulator:
    def __init__(
        self,
        model: js.model.JaxSimModel = None,
        data: js.data.JaxSimModelData = None,
    ) -> None:
        pass

    def run(
        self,
        dt: float = 0.001,
    ) -> None:
        pass

    def save_outputs() -> None:
        pass

    def close() -> None:
        pass
