from random import choices, sample, uniform


class Human:
    """Represents a human with a name."""

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f'{self.name}'


class University:
    """University that manages students, tutors, and the learning process."""

    def __init__(self, name: str):
        self.name = name
        self.tutors = set()
        self.groups = {1: []}
        self.logs_by_group = {}
        self.logs_by_tutor = {}

    def hire(self, tutor):
        """Hires a tutor for the university."""
        if isinstance(tutor, Tutor):
            self.tutors.add(tutor)
            self.logs_by_tutor[tutor.name] = []

    def enroll(self, other, group=1):
        if isinstance(other, Human):
            other = Student(other.name)
            if group in self.groups.keys():
                if len(self.groups[group]) < 5:
                    self.groups[group] += [other]
                    other.university = self.name
                    other.group = group
                else:
                    i = 1
                    while True:
                        if i in self.groups.keys():
                            if len(self.groups[i]) < 5:
                                self.groups[i] += [other]
                                break
                            else:
                                i += 1
                        else:
                            self.groups[i] = [other]
                            break
            else:
                self.groups[group] = [other]

    def start_semester(self, weeks=20):
        """Starts the semester, conducts lectures, and holds exams."""
        self.log_event(f"🏫 The semester at {self.name} has started!", group=0, detailed=True)
        for week in range(1, weeks + 1):
            for tutor in self.tutors:
                for group in self.groups:
                    tutor.teach(self, group)

        self.log_event("🎓 The semester has ended! Exams begin.", group=0, detailed=True)
        for tutor in self.tutors:
            for group in self.groups:
                tutor.examinate(self, group)

        self.show_statistics()

    def log_event(self, message, group=None, tutor=None, detailed=False):
        """Stores events in group and tutor logs."""
        if group is not None:
            self.logs_by_group.setdefault(group, []).append((message, detailed))
        if tutor is not None:
            self.logs_by_tutor.setdefault(tutor, []).append((message, detailed))

    def show_logs(self):
        """Displays all logs (summary and detailed)."""
        print("\n💡 Logs Summary:")
        for group_number, logs in self.logs_by_group.items():
            print(f"\n📚 Group {group_number}:")
            avg_attendance = self.calculate_avg_attendance_for_group(group_number)
            print(f"📝 Average attendance: {avg_attendance}%")
            for log, detailed in logs:
                if not detailed:
                    print(f"📝 {log}")

        for tutor_name, logs in self.logs_by_tutor.items():
            print(f"\n🎓 Tutor {tutor_name}:")
            avg_attendance = self.calculate_avg_attendance_for_tutor(tutor_name)
            print(f"📝 Average attendance: {avg_attendance}%")
            for log, detailed in logs:
                if not detailed:
                    print(f"📝 {log}")

    def show_logs_by_group(self, group_number):
        """Displays summary logs for a specific group."""
        group_students = self.groups.get(group_number, [])
        if not group_students:
            print(f"📭 No students in Group {group_number}.")
            return

        avg_attendance = self.calculate_avg_attendance_for_group(group_number)
        avg_grade = self.calculate_avg_grade_for_group(group_number)
        print(f"\n📚 Logs for Group {group_number} (summary):")
        print(f"📝 Average attendance: {avg_attendance:.2f}%")
        print(f"📝 Average grade: {avg_grade:.2f}")

    def show_detailed_logs_by_group(self, group_number):
        """Displays detailed logs for a specific group."""
        group_students = self.groups.get(group_number, [])
        if not group_students:
            print(f"📭 No students in Group {group_number}.")
            return

        print(f"\n📚 Detailed Logs for Group {group_number}:")
        for student in group_students:
            if isinstance(student, Student):
                print(f"\n👤 Student: {student.name}")
                print(f"  📅 Attendance:")
                for subject, attendance in student.attendance.items():
                    print(f"    - {subject}: {attendance} classes attended")
                print(f"  📊 Grades:")
                for subject, grade in student.specializations.items():
                    print(f"    - {subject}: {grade}")
        print("\n" + "=" * 50)

    def show_logs_by_tutor(self, tutor_name):
        """Displays summary logs for a specific tutor."""

        tutor = next((t for t in self.tutors if t.name == tutor_name), None)
        if not tutor:
            print(f"⚠️ Invalid tutor name. Please enter a valid name from the list.")
            return

        subject = tutor.subject
        avg_attendance = self.calculate_avg_attendance_for_tutor(subject)
        avg_grade = self.calculate_avg_grade_for_tutor(subject)
        print(f"\n🎓 Logs for Tutor {tutor_name} (summary):")
        print(f"📝 Average attendance: {avg_attendance:.2f}%")
        print(f"📝 Average grade: {avg_grade:.2f}")

    def show_detailed_logs_by_tutor(self, tutor_name):
        """Displays detailed logs for a specific tutor."""
        tutor = next((t for t in self.tutors if t.name == tutor_name), None)
        if not tutor:
            print(f"⚠️ Invalid tutor name. Please enter a valid name from the list.")
            return

        subject = tutor.subject
        print(f"\n🎓 Detailed Logs for Tutor {tutor_name}:")
        for group_number, students in self.groups.items():
            print(f"\n📚 Group {group_number}:")
            for student in students:
                if isinstance(student, Student) and subject in student.attendance:
                    print(f"\n  👤 Student: {student.name}")
                    print(f"    📅 Attendance: {student.attendance[subject]} classes attended")
                    if subject in student.specializations:
                        print(f"    📊 Grade: {student.specializations[subject]}")
            print("\n" + "-" * 50)

    def calculate_avg_attendance_for_group(self, group_number):
        """Calculates the average attendance for a specific group."""
        group_students = self.groups.get(group_number, [])
        total_attendance = 0
        total_count = 0

        for student in group_students:
            if isinstance(student, Student):
                total_attendance += sum((attendance / 20) * 100 for attendance in student.attendance.values())
                total_count += len(student.attendance)

        return (total_attendance / total_count) if total_count else 0

    def calculate_avg_grade_for_group(self, group_number):
        """Calculates the average grade for a specific group."""
        group_students = self.groups.get(group_number, [])
        total_grades = 0
        total_count = 0

        for student in group_students:
            if isinstance(student, Student):
                grades = list(student.specializations.values())
                if grades:
                    total_grades += sum(grades)
                    total_count += len(grades)

        return (total_grades / total_count) if total_count else 0

    def calculate_avg_attendance_for_tutor(self, subject):
        """Calculates the average attendance for a specific tutor's subject."""
        total_attendance = 0
        total_students = 0

        for group_number, students in self.groups.items():
            for student in students:
                if subject in student.attendance:
                    total_attendance += (student.attendance[subject] / 20) * 100
                    total_students += 1

        return (total_attendance / total_students) if total_students else 0

    def calculate_avg_grade_for_tutor(self, subject):
        total_grades = 0
        total_students = 0

        for group_number, students in self.groups.items():
            for student in students:
                if isinstance(student, Student) and subject in student.specializations:
                    total_grades += student.specializations[subject]
                    total_students += 1

        return (total_grades / total_students) if total_students else 0

    def show_statistics(self):
        best_students = 0
        worst_students = 0

        for group in self.groups.values():
            for student in group:
                if isinstance(student, Student):
                    grades = list(student.specializations.values())
                    if 5 in grades:
                        best_students += 1
                    if 2 in grades:
                        worst_students += 1

        self.log_event(f"📊 Semester results:", group=0, detailed=True)
        self.log_event(f"🏆 {best_students} students received the highest grade (5).", group=0, detailed=True)
        self.log_event(f"⚠️ {worst_students} students received the lowest grade (2).", group=0, detailed=True)


class Student(Human):
    """A student enrolled in the university."""

    def __init__(self, name):
        super().__init__(name)
        self.group = None
        self.university = None
        self.specializations = dict()
        self.attendance = dict()


class Tutor(Human):
    """A tutor who conducts lectures and exams."""

    def __init__(self, name, subject: str):
        super().__init__(name)
        self.subject = subject

    def teach(self, university, group_number):
        if group_number not in university.groups:
            return

        group_students = university.groups[group_number]
        if not group_students:
            return

        attendance_probability = uniform(0.3, 1.0)
        attending_students = sample(group_students, k=int(len(group_students) * attendance_probability))

        for student in attending_students:
            student.attendance[self.subject] = student.attendance.get(self.subject, 0) + 1

        message = f"📚 {self.name} taught {self.subject} to Group {group_number}. ✅ {len(attending_students)} students attended."
        university.log_event(message, group=group_number, tutor=self.subject, detailed=False)

    def examinate(self, university, group_number):
        if group_number not in university.groups:
            return

        group_students = university.groups[group_number]
        if not group_students:
            return

        for student in group_students:
            attendance = student.attendance.get(self.subject, 0)

            if attendance <= 5:
                grade = choices([2, 3], weights=[60, 20])[0]
            elif 6 <= attendance <= 10:
                grade = choices([2, 3, 4], weights=[60, 50, 5])[0]
            elif 11 <= attendance <= 15:
                grade = choices([3, 4, 5], weights=[30, 70, 20])[0]
            elif 16 <= attendance < 20:
                grade = choices([3, 4, 5], weights=[5, 20, 50])[0]
            else:
                grade = choices([4, 5], weights=[1, 30])[0]

            student.specializations[self.subject] = grade

        message = f"📝 {self.name} held an exam in {self.subject} for Group {group_number}."
        university.log_event(message, group=group_number, tutor=self.subject, detailed=False)


def simulate_smtu(logs=False):
    def green_input(prompt):
        # Returns user input with green color.
        print(prompt, end="")
        user_input = input("\033[32m")
        print("\033[0m", end="")
        return user_input

    # Initialize the university
    smtu = University('SMTU')

    # Create students
    student_names = [
        "Alexei", "Anastasia", "Andrei", "Arina", "Bogdan", "Dmitry", "Ekaterina",
        "Elizaveta", "Ivan", "Irina", "Kirill", "Ksenia", "Leonid", "Lidia", "Maxim",
        "Maria", "Mikhail", "Natalia", "Nikita", "Olga", "Pavel", "Polina", "Roman",
        "Svetlana", "Sergey", "Tatiana", "Timofey", "Valentina", "Valentin", "Vera",
        "Viktor", "Yulia", "Vadim", "Vasilisa", "Ilya", "Inna", "Yevgeny", "Marina",
        "Oleg", "Alina"
    ]
    students = [Student(name) for name in student_names]

    # Enroll students
    for student in students:
        smtu.enroll(student)

    # Create tutors
    tutors = [
        Tutor('Ella', 'math'),
        Tutor('Sergey', 'physics'),
        Tutor('Alina', 'english'),
        Tutor('Inna', 'history'),
        Tutor('Boris', 'PE'),
    ]

    # Hire tutors
    for tutor in tutors:
        smtu.hire(tutor)

    # Start semester
    smtu.start_semester()

    # Printing logs if file is running directly
    if logs:
        print(f'\033[31mUniversity model simulation started!\033[0m')
        for log, detailed in smtu.logs_by_group.get(0, []):
            if detailed:
                print(log)

        # SMTU system
        print("\n🏫 University Structure:")
        print("\n📚 Groups and Students:")
        for group_number, students in smtu.groups.items():
            print(f"  🎒 Group {group_number}:")
            for student in students:
                print(f"    👤 {student.name}")

        print("\n🎓 Tutors and Subjects:")
        for tutor in tutors:
            print(f"  👨‍🏫 {tutor.name} ({tutor.subject})")

        # Interactive menu
        while True:
            print("\n💡 Available groups:", list(smtu.groups.keys()))
            print("💡 Available tutors:", [f"{t.name} ({t.subject})" for t in tutors])
            choice = green_input("\n📖 Choose an action:\n1 - Show all logs\n2 - Show logs by group\n3 - Show logs by tutor\n(Press 'Enter' or type 'exit' to quit)\n>>> ")

            if choice == "1":
                smtu.show_logs()
            elif choice == "2":
                while True:
                    print("\n💡 Available groups:", list(smtu.groups.keys()))
                    group = green_input("Enter the group number:\n>>> ")
                    if group == 'exit' or group == '':
                        exit(f'\033[31mUniversity model simulation completed!\033[0m')
                    if group.isdigit() and int(group) in smtu.groups:
                        smtu.show_logs_by_group(int(group))
                        more = green_input("\nDo you want to see detailed logs for this group? (y/n):\n>>> ").strip().lower()
                        if more.lower() == 'y':
                            smtu.show_detailed_logs_by_group(int(group))
                            break
                        elif more.lower() == 'n':
                            break
                        elif more == '' or more == 'exit':
                            exit(f'\033[31mUniversity model simulation completed!\033[0m')
                    print("\033[33m⚠️ Invalid group. Please enter a valid number from the list.\033[0m")
            elif choice == "3":
                while True:
                    print("💡 Available tutors:", [f"{t.name} ({t.subject})" for t in tutors])
                    tutor_name = green_input("Enter the tutor's name:")
                    if tutor_name == "exit" or tutor_name == '':
                        exit(f'\033[31mUniversity model simulation completed!\033[0m')
                    if tutor_name.lower() in [t.name.lower() for t in tutors]:
                        smtu.show_logs_by_tutor(tutor_name)
                        more = green_input("\nDo you want to see detailed logs for this tutor? (y/n):\n>>> ").strip().lower()
                        if more.lower() == 'y':
                            smtu.show_detailed_logs_by_tutor(tutor_name)
                            break
                        elif more.lower() == 'n':
                            break
                        elif more == '' or more == 'exit':
                            exit(f'\033[31mUniversity model simulation completed!\033[0m')
                    print(f"\033[33m⚠️ Invalid tutor name. Please enter a valid name from the list.\033[0m")
            elif choice == 'exit' or choice == '':
                exit(f'\033[31mUniversity model simulation completed!\033[0m')
            else:
                print("\033[33m⚠️ Invalid input. Please try again.\033[0m")


if __name__ == '__main__':
    simulate_smtu(logs=True)