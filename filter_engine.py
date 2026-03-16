class FilterEngine:

    @staticmethod
    def apply_filters(candidates, filters):

        if not filters:
            return candidates

        filtered = []

        edu_rank = {
            "Bachelors": 1,
            "Masters": 2,
            "PhD": 3
        }

        for c in candidates:

            # -------------------------
            # GENDER FILTER
            # -------------------------
            gender_pref = filters.get("gender_preference")

            if gender_pref and gender_pref.lower() != "any":
                if not c.get("gender"):
                    continue
                if c["gender"].lower() != gender_pref.lower():
                    continue

            # -------------------------
            # LOCATION FILTER
            # -------------------------
            if filters.get("location"):
                if c.get("location", "").lower() != filters["location"].lower():
                    continue

            # -------------------------
            # SALARY FILTER
            # -------------------------
            if filters.get("max_salary_budget") is not None:
                if c.get("expected_salary", float("inf")) > filters["max_salary_budget"]:
                    continue

            # -------------------------
            # NOTICE PERIOD FILTER
            # -------------------------
            if filters.get("max_notice_period") is not None:
                if c.get("notice_period_days", float("inf")) > filters["max_notice_period"]:
                    continue

            # -------------------------
            # INDUSTRY FILTER
            # -------------------------
            if filters.get("industry_required"):
                if filters["industry_required"] not in c.get("industry_experience", []):
                    continue

            # -------------------------
            # EDUCATION FILTER
            # -------------------------
            if filters.get("education_required"):
                required = edu_rank.get(filters["education_required"], 0)
                candidate_edu = edu_rank.get(c.get("education_level"), 0)

                if candidate_edu < required:
                    continue

            filtered.append(c)

        return filtered