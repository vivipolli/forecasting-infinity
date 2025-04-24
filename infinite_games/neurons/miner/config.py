from bittensor_wallet import Wallet
from neurons.validator.utils.config import IfgamesEnvType

class MinerConfig:
    def __init__(
        self,
        env: IfgamesEnvType = "test",
        wallet_name: str = "miner",
        wallet_hotkey: str = "miner",
        network: str = "test",
        netuid: int = 155
    ):
        self.env = env
        self.network = network
        self.netuid = netuid
        self.wallet = Wallet(name=wallet_name, hotkey=wallet_hotkey)
        self.feedback_weight = 0.1  # Base adjustment for each feedback
        self.max_feedback_adjustment = 0.3  # Maximum adjustment allowed
        self.min_feedback_count = 3 