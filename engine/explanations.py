# engine/explanations.py

def generate_explanation(course_code, reason_type, context=None):
    if reason_type == "prereq_met":
        return f"{course_code} is recommended because you passed its prerequisites: {', '.join(context)}."
    elif reason_type == "failed_retake":
        return f"{course_code} is prioritized because you previously failed it and now meet prerequisites."
    elif reason_type == "credit_limit":
        return f"{course_code} was excluded due to CGPA-based credit limit."
    elif reason_type == "prereq_missing":
        return f"{course_code} is not recommended because you have not passed prerequisites: {', '.join(context)}."
    elif reason_type == "semester_unavailable":
        return f"{course_code} is not offered in the upcoming semester."
    return f"No explanation available for {course_code}."
