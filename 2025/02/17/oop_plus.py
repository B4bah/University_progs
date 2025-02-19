'''
TODO
Change the system to where university is the one who's taking exams through tutors
'''

from random import choices, sample, uniform


class Human:
    def __init__(self, name: str):
        self.name = name

    def __add__(self, other):
        return self.name + other.name

    def __str__(self):
        return f'{self.name} is a human'


class University:
    def __init__(self, name: str):
        self.name = name
        self.tutors = set()
        self.groups = {1: []}

    def __str__(self):
        tutors_str = "\n    Tutors: " + ", ".join(f"{tutor.name} ({tutor.subject})" for tutor in self.tutors) if self.tutors else "No tutors"

        groups_str = ""
        for group, students in self.groups.items():
            groups_str += f"\n    Group {group}: {', '.join(student.name for student in students)}"

        return f'University {self.name}: {tutors_str} {groups_str}'

    def hire(self, other):
        if isinstance(other, Tutor):
            self.tutors.add(other)

    def enroll(self, other, group=1):
        if isinstance(other, Student):
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


class Student(Human):
    def __init__(self, name):
        super().__init__(name)
        self.group = None
        self.university = None
        self.specializations = dict()
        self.attendance = dict()

    def __str__(self):
        return f'{self.name} is a student at {self.university} in {self.group} group, knowledge: {self.attendance}, specializations: {self.specializations}'


class Tutor(Human):
    def __init__(self, name, subject: str):
        super().__init__(name)
        self.subject = subject

    def __str__(self):
        return f'{self.name} is a tutor'

    def teach(self, university, group_number):
        if group_number not in university.groups:
            print(f"Group {group_number} not found in {university.name}.")
            return

        group_students = university.groups[group_number]
        if not group_students:
            print(f"Group {group_number} has no students.")
            return

        attendance_probability = uniform(0.5, 1.0)
        attending_students = sample(group_students, k=int(len(group_students) * attendance_probability))
        absent_students = [s for s in group_students if s not in attending_students]

        for student in attending_students:
            student.attendance[self.subject] = student.attendance.get(self.subject, 0) + 1

        print(f"\n📚 {self.name} taught {self.subject} to group {group_number}.")
        print(f"✅ Attended ({len(attending_students)}): {', '.join(s.name for s in attending_students)}")
        print(f"❌ Missed ({len(absent_students)}): {', '.join(s.name for s in absent_students) if absent_students else 'No one missed this class!'}")

    def examinate(self, university, group_number):
        if group_number not in university.groups:
            print(f"Group {group_number} not found in {university.name}.")
            return

        group_students = university.groups[group_number]
        if not group_students:
            print(f"Group {group_number} has no students.")
            return

        for student in group_students:
            if isinstance(student, Student):
                attendance = student.attendance.get(self.subject, 0)

                if attendance <= 5:
                    grade = choices([2, 3], weights=[60, 40])[0]
                elif 6 <= attendance <= 10:
                    grade = choices([2, 3, 4], weights=[60, 40, 5])[0]
                elif 11 <= attendance <= 15:
                    grade = choices([3, 4, 5], weights=[40, 60, 10])[0]
                elif 16 <= attendance <= 20:
                    grade = choices([3, 4, 5], weights=[5, 20, 50])[0]

                student.specializations[self.subject] = grade
                print(f"\n📝 {self.name} is conducting an exam in {self.subject} for group {group_number}.")
                print(f"🎓 Students being examined ({len(group_students)}): {', '.join(s.name for s in group_students)}")
                print(f"🏆 Results:")
                for student in group_students:
                    grade = student.specializations.get(self.subject, 'Not graded')
                    print(f"   🎓 {student.name} → {grade}")


# Creating SMTU
smtu = University('SMTU')

# Creating Students
# Creating a list of student names
student_names = [
    "Alexei", "Anastasia", "Andrei", "Arina", "Bogdan", "Dmitry", "Ekaterina",
    "Elizaveta", "Ivan", "Irina", "Kirill", "Ksenia", "Leonid", "Lidia", "Maxim",
    "Maria", "Mikhail", "Natalia", "Nikita", "Olga", "Pavel", "Polina", "Roman",
    "Svetlana", "Sergey", "Tatiana", "Timofey", "Valentina", "Valentin", "Vera",
    "Viktor", "Yulia", "Vadim", "Vasilisa", "Ilya", "Inna", "Yevgeny", "Marina",
    "Oleg", "Alina"
]
students = [Student(name) for name in student_names]

# Enrolling students into the SMTU
for student in students:
    smtu.enroll(student)


# Creating Tutors
tutors = [
    Tutor('Ella', 'math'),
    Tutor('Sergey', 'physics'),
    Tutor('Alina', 'english'),
    Tutor('Inna', 'history'),
    Tutor('Boris', 'PE'),
]

# Hiring Tutors in SMTU
for tutor in tutors:
    smtu.hire(tutor)

print(smtu)

# Teaching Students
for _ in range(20):
    for tutor in tutors:
        tutor.teach(smtu, 1)

# Examinating Students
for tutor in tutors:
    tutor.examinate(smtu, 1)