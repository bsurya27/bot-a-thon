def compute_score(answers: list[str]) -> float:
    yes_count = sum(1 for a in answers if a.strip().lower() == "yes")
    return round((yes_count / len(answers)) * 10, 2)

def compute_breakdown(dimension_answers: dict) -> dict:
    return {
        dim: compute_score(answers)
        for dim, answers in dimension_answers.items()
    }

def compute_final_score(breakdown: dict) -> float:
    return round(sum(breakdown.values()) / len(breakdown), 2)

def get_verdict(score: float) -> str:
    if score >= 7.5:
        return "pass"
    elif score >= 5.0:
        return "review"
    else:
        return "fail"