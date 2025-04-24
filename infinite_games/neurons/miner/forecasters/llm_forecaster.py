from forecasting_tools import BinaryQuestion, QuestionState, TemplateBot
from neurons.validator.if_games.client import IfGamesClient

from neurons.miner.forecasters.base import BaseForecaster
from neurons.miner.models.event import MinerEvent
from neurons.validator.utils.logger.logger import InfiniteGamesLogger
from neurons.miner.services.expert_feedback_adjuster import ExpertFeedbackAdjuster


class LLMForecaster(BaseForecaster):
    def __init__(
        self, 
        event: MinerEvent, 
        logger: InfiniteGamesLogger,
        if_games_client: IfGamesClient,
        extremize: bool = False
    ):
        super().__init__(event, logger, extremize)
        self.bot = TemplateBot(
            research_reports_per_question=1,
            predictions_per_research_report=5,
        )
        self.if_games_client = if_games_client
        self.feedback_adjuster = ExpertFeedbackAdjuster()

    async def _run(self) -> float:
        try:
            # Get base prediction from LLM
            question = BinaryQuestion(
                question_text=self.event.get_description(),
                background_info=None,
                resolution_criteria=None,
                fine_print=None,
                id_of_post=0,
                state=QuestionState.OPEN,
            )
            
            self.logger.info("Getting base prediction from LLM")
            reports = await self.bot.forecast_questions([question])
            base_probability = reports[0].prediction
            self.logger.info(f"Base probability: {base_probability}")
            
            return base_probability

        except Exception as e:
            self.logger.error(f"Error in LLM forecast: {e}")
            raise  # Re-raise the exception instead of returning a default value

    async def adjust_with_feedback(
        self,
        current_prediction: float,
        agrees: bool,
        expert_weight: float = 1.0,
        expert_id: str = None,
        event_id: str = None
    ) -> float:
        """
        Adjusts the existing prediction with expert feedback
        """
        try:
            self.logger.info(f"Adjusting prediction with expert feedback (weight: {expert_weight})")
            
            new_prediction = self.feedback_adjuster.adjust_prediction(
                current_prediction=current_prediction,
                expert_agrees=agrees,
                expert_weight=expert_weight,
                expert_id=expert_id,
                event_id=event_id
            )
            
            self.logger.info(f"Adjusted prediction: {current_prediction} -> {new_prediction}")
            return new_prediction
            
        except Exception as e:
            self.logger.error(f"Error adjusting prediction: {e}")
            return current_prediction
