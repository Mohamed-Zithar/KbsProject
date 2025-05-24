from experta import KnowledgeEngine
from engine.facts import Course, StudentInfo
from engine.explanations import generate_explanation
import pandas as pd  

class CourseAdvisor(KnowledgeEngine):
    def __init__(self, student, all_courses):
        super().__init__()
        self.student = student
        self.all_courses = all_courses
        self.recommendations = []
        self.explanations = []
        self.total_credits = 0

    def add_course(self, course, reason_type, context=None):
        if self.total_credits + course["credit_hours"] <= self.max_credits():
            self.recommendations.append(course)
            self.total_credits += course["credit_hours"]
            self.explanations.append(generate_explanation(course["code"], reason_type, context))
        else:
            self.explanations.append(generate_explanation(course["code"], "credit_limit_exceeded"))

    def max_credits(self):
        cgpa = self.student["cgpa"]
        return 12 if cgpa < 2.0 else 15 if cgpa < 3.0 else 18

    def run_engine(self):
        passed = set(self.student["passed"])
        failed = set(self.student["failed"])
        upcoming_sem = self.student["semester"].lower()

        print("\n=== Recommendation Engine Started ===")
        print("CGPA:", self.student["cgpa"])
        print("Semester:", upcoming_sem)
        print("Passed:", passed)
        print("Failed:", failed)

        for _, row in self.all_courses.iterrows():
            course = row.to_dict()
            code = course["coursecode"]
            course["code"] = code
            course["credit_hours"] = int(course["credithours"])

            # ✅ Fix: Use pd.isna to avoid string 'nan' bugs
            prereq_raw = course.get("prerequisites")
            coreq_raw = course.get("corequisites")
            prereqs = [] if pd.isna(prereq_raw) else [p.strip() for p in str(prereq_raw).split(',') if p.strip()]
            coreqs = [] if pd.isna(coreq_raw) else [c.strip() for c in str(coreq_raw).split(',') if c.strip()]
            course["prerequisites"] = prereqs
            course["corequisites"] = coreqs

            print(f"\n🔍 Evaluating {code} (Sem: {course['semester']} | Prereqs: {prereqs})")

            # Already passed
            if code in passed:
                print(f"⏭️ Skipped {code} — already passed.")
                continue

            # Retake failed course if prerequisites met
            if code in failed and all(p in passed for p in prereqs):
                print(f"🔁 Retaking failed course {code}")
                self.add_course(course, "failed_retake", prereqs)
                continue

            # Check if prerequisites are satisfied
            if all(p in passed for p in prereqs):
                if course["semester"].lower() in [upcoming_sem, "both"]:
                    print(f"✅ Recommending {code}")
                    self.add_course(course, "prereq_met", prereqs)
                else:
                    print(f"📅 Not offered this semester: {code}")
                    self.explanations.append(generate_explanation(code, "semester_unavailable"))
            else:
                missing = [p for p in prereqs if p not in passed]
                print(f"❌ Missing prerequisites for {code}: {missing}")
                self.explanations.append(generate_explanation(code, "prereq_missing", missing))

        if not self.recommendations:
            print("⚠️ No courses recommended.")
