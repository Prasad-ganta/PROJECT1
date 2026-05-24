from typing import Any


# =====================================================
# FEATURE-BASED CONFIDENCE
# =====================================================

def compute_confidence(
    features: dict[str, Any]
) -> float:

    """
    Confidence score based on
    feature completeness.
    """

    required = [

        "Hour",

        "Visit_Duration_Min",

        "Stop_Encoded",

        "Traffic_Level"
    ]

    present = sum(

        1
        for key in required

        if features.get(key)
        not in (None, "", 0)
    )

    base = present / len(required)

    return round(

        min(max(base, 0.0), 1.0),

        2
    )


# =====================================================
# ROUTE CONFIDENCE
# =====================================================

def calculate_confidence(
    total_eta_minutes: float
) -> float:

    """
    Route-level confidence score.
    """

    if total_eta_minutes <= 60:
        return 0.95

    elif total_eta_minutes <= 120:
        return 0.90

    elif total_eta_minutes <= 180:
        return 0.85

    elif total_eta_minutes <= 240:
        return 0.80

    return 0.75