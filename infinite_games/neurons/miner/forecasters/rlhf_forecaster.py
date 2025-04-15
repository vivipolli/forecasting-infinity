from typing import Dict, List, Optional
import json
import os
from datetime import datetime
import numpy as np

from forecasting_tools import BinaryQuestion, QuestionState, TemplateBot

from neurons.miner.forecasters.base import BaseForecaster
from neurons.miner.models.event import MinerEvent
from neurons.validator.utils.logger.logger import InfiniteGamesLogger

class RLHFForecaster(BaseForecaster):
    def __init__(
        self,
        event: MinerEvent,
        logger: InfiniteGamesLogger,
        extremize: bool = False,
        feedback_weight: float = 0.3,
        min_feedback_count: int = 3,
        use_feedback: bool = True,
    ):
        super().__init__(event, logger, extremize)
        self.bot = TemplateBot(
            research_reports_per_question=1,
            predictions_per_research_report=5,
        )
        self.feedback_weight = feedback_weight
        self.min_feedback_count = min_feedback_count
        self.use_feedback = use_feedback
        self.feedback_file = "feedback_data.json"
        self._load_feedback_data()

    def _load_feedback_data(self) -> None:
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'r') as f:
                self.feedback_data = json.load(f)
        else:
            self.feedback_data = {}

    def _save_feedback_data(self) -> None:
        with open(self.feedback_file, 'w') as f:
            json.dump(self.feedback_data, f, indent=2)

    def _get_feedback_for_event(self, event_id: str) -> Optional[Dict]:
        return self.feedback_data.get(event_id)

    def _calculate_weighted_agreement_score(self, feedback: Dict) -> float:
        votes = feedback.get('votes', [])
        if not votes:
            return 0.5

        # Calculate base agreement score
        agreement_scores = []
        weights = []

        for vote in votes:
            # Base weight is 1.0
            weight = 1.0
            
            # Adjust weight based on user reputation if available
            if 'user_reputation' in vote and vote['user_reputation'] is not None:
                weight *= vote['user_reputation']
            
            # Adjust weight based on recency (more recent votes have higher weight)
            if 'timestamp' in vote:
                vote_time = datetime.fromisoformat(vote['timestamp'])
                time_diff = (datetime.now() - vote_time).total_seconds() / (24 * 3600)  # days
                weight *= np.exp(-0.1 * time_diff)  # Exponential decay

            weights.append(weight)
            agreement_scores.append(1.0 if vote['agrees'] else 0.0)

        # Calculate weighted average
        if sum(weights) == 0:
            return 0.5
            
        return np.average(agreement_scores, weights=weights)

    def _calculate_adjusted_probability(
        self, 
        base_probability: float, 
        feedback: Optional[Dict]
    ) -> float:
        if not self.use_feedback or not feedback:
            return base_probability

        total_feedback = len(feedback.get('votes', []))
        if total_feedback < self.min_feedback_count:
            return base_probability

        agreement_score = self._calculate_weighted_agreement_score(feedback)
        return (1 - self.feedback_weight) * base_probability + self.feedback_weight * agreement_score

    async def _run(self) -> float:
        question = BinaryQuestion(
            question_text=self.event.get_description(),
            background_info=None,
            resolution_criteria=None,
            fine_print=None,
            id_of_post=0,
            state=QuestionState.OPEN,
        )

        try:
            reports = await self.bot.forecast_questions([question])
            base_probability = reports[0].prediction

            event_id = self.event.get_event_id()
            feedback = self._get_feedback_for_event(event_id)
            
            final_probability = self._calculate_adjusted_probability(base_probability, feedback)
            return final_probability

        except Exception as e:
            self.logger.error(f"Error forecasting question with RLHF: {e}")
            return 0.5

    def add_feedback(
        self, 
        event_id: str, 
        agrees: bool, 
        comment: Optional[str] = None,
        user_id: Optional[str] = None,
        user_reputation: Optional[float] = None
    ) -> None:
        if event_id not in self.feedback_data:
            self.feedback_data[event_id] = {
                'votes': [],
                'comments': []
            }

        self.feedback_data[event_id]['votes'].append({
            'timestamp': datetime.now().isoformat(),
            'agrees': agrees,
            'user_id': user_id,
            'user_reputation': user_reputation
        })

        if comment:
            self.feedback_data[event_id]['comments'].append({
                'timestamp': datetime.now().isoformat(),
                'text': comment,
                'user_id': user_id
            })

        self._save_feedback_data() 