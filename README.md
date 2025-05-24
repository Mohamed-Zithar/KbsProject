# 📖 AIU CSE Course Advisor

A knowledge-based advising system to help students at **Alamein International University (AIU)** plan their course registration based on prerequisites, semester availability, failed courses, CGPA limits, and their study track.

---

## 🔧 Features

* ✅ Personalized course recommendations
* ✅ Retake prioritization for failed courses
* ✅ Admin-only course editor (add/edit/delete)
* ✅ Login system for students and admins
* ✅ Full rule-based inference using Experta
* ✅ Explanations for every recommendation decision

---

## 🔍 Technologies

* Python 3.10+
* Streamlit
* Experta (Rule-based inference engine)
* Pandas

---

## 🔹 Project Structure

```bash
aiu_kbs_project2/
│
├── auth/                 # Login + session logic
│   └── login.py
│
├── data/                 # Knowledge base files
│   ├── courses.csv       # Course data
│   └── users.csv         # User login and roles
│
├── editor/               # Admin editor for KB
│   └── kb_editor.py
│
├── engine/               # Inference engine
│   ├── advisor.py        # Recommendation engine
│   ├── facts.py          # Experta facts
│   └── explanations.py   # Explanation rules
│
├── interface/
│   └── app.py            # Main Streamlit UI
│
├── utils/
│   └── helpers.py        # Shared CSV utilities
│
├── requirements.txt
└── README.md
```

---

## 🚪 Roles

| Name                | Branch                   | Responsibilities                       |
| ------------------- | ------------------------ | -------------------------------------- |
| **Adham Zewail**    | `feature/inference`      | advisor.py, facts.py, explanations.py  |
| **Walid Tamer**     | `feature/editor-ui`      | kb\_editor.py, helpers.py, courses.csv |
| **Mohamed Ibrahim** | `feature/interface-auth` | app.py, login.py, users.csv            |

---

## ⚡ How to Run

1. Install requirements:

```bash
pip install -r requirements.txt
```

2. Run Streamlit app:

```bash
streamlit run interface/app.py
```

---

## 🔧 Example Credentials

### Admin:

* **Username:** admin
* **Password:** admin123

### Student:

* **Username:** student1
* **Password:** student123

> ✉️ You can modify users in `data/users.csv`

---

## 🎓 License

MIT License © 2025 AIU Team

---

## 🔗 GitHub

[github.com/Mohamed-Zithar/KbsProject](https://github.com/Mohamed-Zithar/KbsProject)
