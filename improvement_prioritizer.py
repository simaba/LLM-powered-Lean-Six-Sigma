class ImprovementPrioritizer:
    def __init__(self, improvement_actions: list):
        self.improvement_actions = improvement_actions

    def rank_actions(self):
        # Rank improvement actions based on impact, effort, and risk
        ranked_actions = []
        for action in self.improvement_actions:
            impact = action['impact']
            effort = action['effort']
            risk = action['risk']
            score = impact / (effort + 1) - risk
            ranked_actions.append({'action': action['action'], 'score': score})

        ranked_actions.sort(key=lambda x: x['score'], reverse=True)
        return ranked_actions

    def quick_wins(self):
        # Return actions that are quick wins (low effort, high impact)
        quick_wins = [action for action in self.improvement_actions if action['effort'] < 3 and action['impact'] > 7]
        return quick_wins

    def long_term_fixes(self):
        # Return long-term fixes (high effort, high impact)
        long_term_fixes = [action for action in self.improvement_actions if action['effort'] > 7 and action['impact'] > 7]
        return long_term_fixes

    def prioritize(self):
        # Rank actions, return quick wins and long-term fixes
        ranked_actions = self.rank_actions()
        quick_wins = self.quick_wins()
        long_term_fixes = self.long_term_fixes()

        return {
            'ranked_actions': ranked_actions,
            'quick_wins': quick_wins,
            'long_term_fixes': long_term_fixes
        }