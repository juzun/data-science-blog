from typing import Dict, List

import pandas as pd


def search_for_columns_with_keyword(
    data: Dict[str, pd.DataFrame], keywords: List[str]
) -> Dict[int, List[str]]:
    return {
        key: [
            col
            for col in data[key].columns
            if any(keyword in col.lower() for keyword in keywords)
        ]
        for key in data
        if any(
            keyword in col.lower() for col in data[key].columns for keyword in keywords
        )
    }


def categorize_gender(value: str) -> str:
    value = value.lower()
    if (
        "non-binary" in value
        or "genderqueer" in value
        or "gender non-conforming" in value
        or "queer" in value
    ):
        return "Queer/Non-binary"
    elif "woman" in value or "female" in value:
        return "Female"
    elif ("man" in value and "woman" not in value) or (
        "male" in value and "female" not in value
    ):
        return "Male"
    else:
        return "Other"
