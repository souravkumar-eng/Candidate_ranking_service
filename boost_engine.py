class BoostEngine:

    @staticmethod
    def apply_boosts(candidate, filters, score):

        if not filters:
            return score

        # Location boost
        if filters.get("location"):
            if candidate.get("location") == filters.get("location"):
                score *= 1.05

        # Gender preference boost
        if filters.get("gender_preference"):
            if candidate.get("gender") == filters.get("gender_preference"):
                score *= 1.03

        # Notice period boost
        if filters.get("max_notice_period") is not None:
            if candidate.get("notice_period_days", 9999) <= filters.get("max_notice_period"):
                score *= 1.02

        return score
    