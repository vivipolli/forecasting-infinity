class ExpertFeedbackAdjuster:
    def __init__(self):
        self.max_adjustment = 0.3 
        self.max_feedbacks_per_expert = 1  # Limit feedbacks per expert per event
        
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
        # Check if expert has already given feedback for this event
        feedback_key = f"{expert_id}_{event_id}"
        if hasattr(self, 'feedback_history') and feedback_key in self.feedback_history:
            return current_prediction  # Expert already gave feedback, ignore
            
        # Initialize feedback history if not exists
        if not hasattr(self, 'feedback_history'):
            self.feedback_history = {}
            
        # Record the feedback
        self.feedback_history[feedback_key] = True
        
        adjustment = 0.1 * expert_weight 
        
        adjustment = min(adjustment, self.max_adjustment)
        
        if expert_agrees:
            new_prediction = current_prediction + (
                (1 - current_prediction) * adjustment
            )
        else:
            new_prediction = current_prediction - (
                current_prediction * adjustment
            )
            
        return max(0.0, min(1.0, new_prediction))
