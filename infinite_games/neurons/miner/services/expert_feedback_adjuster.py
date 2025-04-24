from datetime import datetime

class ExpertFeedbackAdjuster:
    def __init__(self):
        self.max_adjustment = 0.3 
        self.max_feedbacks_per_expert = 1  # Limit feedbacks per expert per event
        self.expert_history = {}  # Track expert performance
        self.feedback_history = {}  # Track feedback history
        
    def adjust_prediction(
        self,
        current_prediction: float,
        expert_agrees: bool,
        expert_weight: float,
        expert_id: str,
        event_id: str
    ) -> float:
        """
        Adjusts the prediction based on expert feedback and their weight
        
        Args:
            current_prediction: Current probability (0-1)
            expert_agrees: Whether the expert agrees (True) or disagrees (False)
            expert_weight: Expert's weight (e.g., 1.1 for trusted experts)
            expert_id: Unique identifier for the expert
            event_id: Unique identifier for the event
            
        Returns:
            New adjusted probability
        """
        # Validate expert
        if not self._validate_expert(expert_id):
            return current_prediction
            
        # Check if expert has already given feedback for this event
        feedback_key = f"{expert_id}_{event_id}"
        if feedback_key in self.feedback_history:
            return current_prediction
            
        # Record the feedback
        self.feedback_history[feedback_key] = {
            "timestamp": datetime.now(),
            "agrees": expert_agrees,
            "weight": expert_weight,
            "event_id": event_id
        }
        
        # Calculate adjustment based on expert weight and history
        base_adjustment = 0.1
        expert_multiplier = self._calculate_expert_multiplier(expert_id)
        adjustment = base_adjustment * expert_weight * expert_multiplier
        adjustment = min(adjustment, self.max_adjustment)
        
        if expert_agrees:
            new_prediction = current_prediction + ((1 - current_prediction) * adjustment)
        else:
            new_prediction = current_prediction - (current_prediction * adjustment)
            
        return max(0.0, min(1.0, new_prediction))
        
    def _validate_expert(self, expert_id: str) -> bool:
        # TODO: Implement expert validation (e.g., check against database)
        return True
        
    def _calculate_expert_multiplier(self, expert_id: str) -> float:
        # TODO: Implement expert performance calculation
        return 1.0
