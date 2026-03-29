class ControlPlanGenerator:
    def __init__(self, prioritized_actions: list):
        self.prioritized_actions = prioritized_actions

    def generate_metrics(self):
        # For each prioritized action, suggest metrics to track.
        metrics = [
            {'action': action['action'], 'metric': 'Process efficiency'},
            {'action': action['action'], 'metric': 'Cycle time reduction'},
            {'action': action['action'], 'metric': 'Cost savings'},
        ]
        return metrics

    def assign_owners(self):
        # For each action, assign an owner.
        owners = [
            {'action': action['action'], 'owner': 'PM'},
            {'action': action['action'], 'owner': 'Team Lead'},
            {'action': action['action'], 'owner': 'Quality Manager'},
        ]
        return owners

    def set_review_cadence(self):
        # For each action, suggest a review cadence.
        review_cadence = [
            {'action': action['action'], 'cadence': 'Monthly'},
            {'action': action['action'], 'cadence': 'Quarterly'},
            {'action': action['action'], 'cadence': 'Bi-Annually'},
        ]
        return review_cadence

    def define_thresholds(self):
        # Define thresholds for when corrective action should be taken.
        thresholds = [
            {'action': action['action'], 'threshold': 'If metric exceeds 90% of target.'},
            {'action': action['action'], 'threshold': 'If process efficiency drops below 80%.'},
            {'action': action['action'], 'threshold': 'If cost savings fall short by 15%.'},
        ]
        return thresholds

    def generate_control_plan(self):
        # Generate the control plan with all components.
        metrics = self.generate_metrics()
        owners = self.assign_owners()
        review_cadence = self.set_review_cadence()
        thresholds = self.define_thresholds()

        control_plan = {
            'metrics': metrics,
            'owners': owners,
            'review_cadence': review_cadence,
            'thresholds': thresholds,
        }
        return control_plan