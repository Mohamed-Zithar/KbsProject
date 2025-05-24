# utils/helpers.py
import pandas as pd
def validate_course_references(df):
    valid_codes = set(df['coursecode'])
    def validate(refs):
        if pd.isna(refs) or refs.strip() == "":
            return True
        for code in refs.split(","):
            if code.strip() not in valid_codes:
                return False
        return True
    return all(df['prerequisites'].apply(validate)) and all(df['corequisites'].apply(validate))
