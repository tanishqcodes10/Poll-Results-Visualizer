"""
data_generator.py
Generates a realistic synthetic poll dataset for development and testing.
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_poll_data(n=500, seed=42):
    np.random.seed(seed)
    random.seed(seed)

    start_date = datetime(2024, 1, 1)

    # Question bank with realistic answer options
    questions = {
        "Which product do you prefer?":
            ["Product A", "Product B", "Product C", "Product D"],
        "How satisfied are you with our service?":
            ["Very Satisfied","Satisfied","Neutral","Dissatisfied","Very Dissatisfied"],
        "Which feature is most important to you?":
            ["Price","Quality","Support","Speed"],
        "How often do you use our product?":
            ["Daily","Weekly","Monthly","Rarely"],
        "Would you recommend us to a friend?":
            ["Definitely Yes","Probably Yes","Not Sure","Probably No","Definitely No"]
    }

    # Realistic probability weights (simulate real polling bias)
    weights = {
        "Which product do you prefer?":         [0.38,0.28,0.22,0.12],
        "How satisfied are you with our service?": [0.30,0.35,0.20,0.10,0.05],
        "Which feature is most important to you?": [0.40,0.30,0.18,0.12],
        "How often do you use our product?":    [0.25,0.35,0.25,0.15],
        "Would you recommend us to a friend?":  [0.35,0.30,0.18,0.10,0.07]
    }

    regions    = ["North","South","East","West","Central"]
    age_groups = ["18-24","25-34","35-44","45-54","55+"]
    genders    = ["Male","Female","Non-Binary","Prefer Not to Say"]

    rows = []
    for i in range(n):
        q      = random.choice(list(questions.keys()))
        chosen = random.choices(questions[q], weights=weights[q], k=1)[0]
        date   = start_date + timedelta(days=random.randint(0, 364))
        rows.append({
            "respondent_id":    f"R{1000+i}",
            "date":             date.strftime("%Y-%m-%d"),
            "question":         q,
            "option_selected":  chosen,
            "region":           random.choice(regions),
            "age_group":        random.choices(age_groups,
                                    weights=[0.18,0.28,0.22,0.18,0.14], k=1)[0],
            "gender":           random.choices(genders,
                                    weights=[0.45,0.45,0.06,0.04], k=1)[0],
            "response_time_sec": round(np.random.normal(45, 15), 1)
        })

    df = pd.DataFrame(rows)
    print(f"[data_generator] Generated {len(df)} responses, {df['question'].nunique()} questions")
    return df

if __name__ == "__main__":
    df = generate_poll_data()
    df.to_csv("data/poll_data.csv", index=False)
    print("Saved → data/poll_data.csv")