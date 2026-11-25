
import streamlit as st

# =====================================
# STUDENT MARKS MANAGEMENT SYSTEM
# =====================================

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>

/* Main application background */
.stApp {
    background: #f4f7fb;
}

/* Main heading */
h1 {
    color: #1e3a8a;
    font-weight: 800;
    text-align: center;
}

/* Subheadings */
h2, h3 {
    color: #1e40af;
}

/* Paragraph text */
p, label {
    color: #334155;
}

/* Buttons */
.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 22px;
    font-weight: bold;
    transition: 0.3s;
}

/* Button hover effect */
.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
    border: none;
}

/* Input fields */
.stTextInput input,
.stNumberInput input {
    border-radius: 8px;
    border: 1px solid #cbd5e1;
}

/* Select boxes */
.stSelectbox div[data-baseweb="select"] {
    border-radius: 8px;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}

/* Data tables */
[data-testid="stDataFrame"] {
    background: white;
    border-radius: 12px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #e8efff;
}

/* Form containers */
[data-testid="stForm"] {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #dbeafe;
}

/* Success messages */
[data-testid="stAlert"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# INITIAL STUDENT DATA
# =====================================

if "students" not in st.session_state:

    st.session_state.students = [
        (101, "Teja", 85, 90, 80),
        (102, "Rohini", 75, 85, 90),
        (103, "Sravya", 85, 80, 85),
        (104, "Mani", 90, 95, 92)
    ]

# =====================================
# COMMON FUNCTIONS
# =====================================

def calculate_total(student):
    return sum(student[2:5])


def calculate_percentage(student):
    return calculate_total(student) / 300 * 100


def calculate_grade(percentage):

    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("🎓 EduTrack")

st.sidebar.write("Student Management System")

menu = st.sidebar.radio(
    "MAIN MENU",
    [
        "Dashboard",
        "Add Student",
        "Display Students",
        "Count Method",
        "Index Method",
        "Update Marks",
        "Student Ranking",
        "Delete Student"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Python + Streamlit Project")


# =====================================
# DASHBOARD
# =====================================

if menu == "Dashboard":

    st.title("🎓 Student Management Dashboard")

    st.write("Welcome to Student Marks Management System")

    students = st.session_state.students

    total_students = len(students)

    average = (
        sum(calculate_percentage(s) for s in students)
        / total_students
        if total_students else 0
    )

    topper = max(
        students,
        key=calculate_total,
        default=None
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Students", total_students)

    col2.metric("Class Average", f"{average:.2f}%")

    col3.metric(
        "Topper",
        topper[1] if topper else "N/A"
    )

    st.divider()

    st.subheader("Student Records")

    if students:

        for student in students:

            total = calculate_total(student)
            percentage = calculate_percentage(student)

            st.write(
                f"**{student[1]}** | "
                f"Roll No: {student[0]} | "
                f"Total: {total}/300 | "
                f"Percentage: {percentage:.2f}% | "
                f"Grade: {calculate_grade(percentage)}"
            )

    else:
        st.info("No students available.")


# =====================================
# ADD STUDENT
# =====================================

elif menu == "Add Student":

    st.title("➕ Add New Student")

    with st.form("student_form"):

        roll = st.number_input(
            "Roll Number",
            min_value=1,
            step=1
        )

        name = st.text_input("Student Name")

        python_marks = st.number_input(
            "Python Marks",
            min_value=0,
            max_value=100
        )

        sql_marks = st.number_input(
            "SQL Marks",
            min_value=0,
            max_value=100
        )

        react_marks = st.number_input(
            "React Marks",
            min_value=0,
            max_value=100
        )

        submitted = st.form_submit_button("Add Student")

        if submitted:

            if not name.strip():
                st.error("Please enter a student name.")

            elif any(s[0] == roll for s in st.session_state.students):
                st.error("Roll number already exists.")

            else:

                new_student = (
                    roll,
                    name.strip(),
                    python_marks,
                    sql_marks,
                    react_marks
                )

                st.session_state.students.append(new_student)

                st.success("Student added successfully!")


# =====================================
# DISPLAY STUDENTS
# =====================================

elif menu == "Display Students":

    st.title("📋 Student Details and Marks")

    students = st.session_state.students

    if students:

        for student in students:

            with st.expander(f"{student[1]} - Roll No: {student[0]}"):

                st.write("**Python:**", student[2])
                st.write("**SQL:**", student[3])
                st.write("**React:**", student[4])

                total = calculate_total(student)
                percentage = calculate_percentage(student)

                st.write("**Total:**", total, "/ 300")
                st.write("**Average:**", f"{total / 3:.2f}")
                st.write("**Percentage:**", f"{percentage:.2f}%")
                st.write("**Grade:**", calculate_grade(percentage))

    else:
        st.warning("No student records found.")


# =====================================
# COUNT METHOD
# =====================================

elif menu == "Count Method":

    st.title("🔢 Count Method")

    st.write("Count how many times a student name occurs.")

    names = tuple(s[1] for s in st.session_state.students)

    name = st.text_input("Enter student name")

    if st.button("Count Name"):

        result = names.count(name)

        st.success(f"{name} appears {result} time(s).")


# =====================================
# INDEX METHOD
# =====================================

elif menu == "Index Method":

    st.title("🔍 Index Method")

    names = tuple(s[1] for s in st.session_state.students)

    name = st.text_input("Enter student name")

    if st.button("Find Position"):

        if name in names:

            position = names.index(name)

            st.success(f"Student: {names[position]}")

            st.info(f"Index Position: {position}")

            st.write(f"Display Position: {position + 1}")

        else:
            st.error("Student not found!")


# =====================================
# UPDATE MARKS
# =====================================

elif menu == "Update Marks":

    st.title("✏️ Update Student Marks")

    students = st.session_state.students

    if students:

        roll_numbers = [s[0] for s in students]

        roll = st.selectbox(
            "Select Roll Number",
            roll_numbers
        )

        student = next(s for s in students if s[0] == roll)

        st.write("Student Name:", student[1])

        subject = st.selectbox(
            "Select Subject",
            ["Python", "SQL", "React"]
        )

        new_marks = st.number_input(
            "Enter New Marks",
            min_value=0,
            max_value=100,
            step=1
        )

        if st.button("Update Marks"):

            # Step 1: Tuple to List
            student_list = list(student)

            # Step 2: Find subject index
            subject_index = {
                "Python": 2,
                "SQL": 3,
                "React": 4
            }

            # Step 3: Update the selected mark
            student_list[subject_index[subject]] = new_marks

            # Step 4: List back to Tuple
            updated_student = tuple(student_list)

            # Step 5: Update outer collection
            updated_students = list(students)

            position = roll_numbers.index(roll)

            updated_students[position] = updated_student

            st.session_state.students = tuple(updated_students)

            st.success("Marks updated successfully!")

            st.write("Updated Record:", updated_student)

    else:
        st.warning("No students available to update.")


# =====================================
# STUDENT RANKING
# =====================================

elif menu == "Student Ranking":

    st.title("🏆 Student Ranking")

    ranking = sorted(
        st.session_state.students,
        key=calculate_total,
        reverse=True
    )

    if ranking:

        for position, student in enumerate(ranking, start=1):

            st.write(
                f"**Rank {position}: {student[1]}** "
                f"| Total Marks: {calculate_total(student)}"
            )

    else:
        st.info("No student records available.")


# =====================================
# DELETE STUDENT
# =====================================

elif menu == "Delete Student":

    st.title("🗑️ Delete Student")

    students = st.session_state.students

    if students:

        roll_numbers = [s[0] for s in students]

        roll = st.selectbox(
            "Select Student Roll Number",
            roll_numbers
        )

        if st.button("Delete Student"):

            st.session_state.students = tuple(
                student
                for student in students
                if student[0] != roll
            )

            st.success("Student deleted successfully!")

    else:
        st.warning("No student records available.")
