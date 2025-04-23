from typing import List
from datetime import datetime, timedelta, timezone
from neurons.miner.models.event import MinerEvent, MinerEventStatus

def get_mock_events() -> List[MinerEvent]:
    return [
        MinerEvent(
            event_id="btc_100k_2024",
            market_type="BINARY",
            probability=0.65,
            description="Bitcoin price prediction: Will Bitcoin reach $100,000 by the end of 2024? Bitcoin has shown strong performance in 2024 with ETF approvals and halving event approaching",
            cutoff=datetime.now(timezone.utc) + timedelta(days=365),
            status=MinerEventStatus.UNRESOLVED
        ),
        MinerEvent(
            event_id="eth_merge_success",
            market_type="BINARY",
            probability=0.75,
            description="Ethereum upgrade impact: Will Ethereum's next major upgrade (Dencun) reduce gas fees by more than 50%? Ethereum's Dencun upgrade introduces proto-danksharding and aims to significantly reduce L2 transaction costs",
            cutoff=datetime.now(timezone.utc) + timedelta(days=180),
            status=MinerEventStatus.UNRESOLVED
        ),
        MinerEvent(
            event_id="ai_agent_2024",
            market_type="BINARY",
            probability=0.45,
            description="AI development capability: Will an AI agent be able to autonomously complete a full software development task by end of 2024? Recent advances in AI coding assistants show promising capabilities in software development",
            cutoff=datetime.now(timezone.utc) + timedelta(days=365),
            status=MinerEventStatus.UNRESOLVED
        ),
        MinerEvent(
            event_id="defi_hack_2024",
            market_type="BINARY",
            probability=0.35,
            description="DeFi security: Will total DeFi hacks in 2024 be less than $500M? DeFi security has improved but still faces significant challenges",
            cutoff=datetime.now(timezone.utc) + timedelta(days=365),
            status=MinerEventStatus.UNRESOLVED
        ),
        MinerEvent(
            event_id="nft_revival",
            market_type="BINARY",
            probability=0.55,
            description="NFT market growth: Will NFT trading volume in Q2 2024 exceed Q1 2024 by more than 50%? NFT market shows signs of recovery with new use cases emerging",
            cutoff=datetime.now(timezone.utc) + timedelta(days=90),
            status=MinerEventStatus.UNRESOLVED
        )
    ] 