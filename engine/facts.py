# engine/facts.py
from experta import Fact
class Course(Fact):
    """Knowledge base representation of a course."""
    code: str
    name: str
    description: str
    prerequisites: list
    corequisites: list
    credit_hours: int
    semester: str
class StudentInfo(Fact):
    """Facts about the student."""
    cgpa: float
    semester: str
    passed: list
    failed: list
