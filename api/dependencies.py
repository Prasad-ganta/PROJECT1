import json
import joblib


# =========================================
# LOAD XGBOOST MODEL
# =========================================

def get_xgboost_model():

    model = joblib.load(
        "saved_models/xgboost_model.pkl"
    )

    return model


# =========================================
# LOAD DISTANCE MATRIX
# =========================================

def get_distance_matrix():

    with open(
        "data/matrices/distance_matrix.json",
        "r"
    ) as f:

        matrix = json.load(f)

    return matrix


# =========================================
# LOAD LABEL ENCODERS
# =========================================

def get_label_encoders():

    encoders = joblib.load(
        "saved_models/label_encoders.pkl"
    )

    return encoders