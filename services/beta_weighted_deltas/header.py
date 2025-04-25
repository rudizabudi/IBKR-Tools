class Header:
    def __init__(self,  symbol: str = None, **kwargs):
        self.symbol = symbol
        self.beta = None

    def set_beta(self, beta: float):
        self.beta = beta

    def generate_name(self) -> str:
        return self.symbol

    def get_beta(self) -> float:
        return self.beta
