'''
TODO
make a system where students attend classes and get knowledge
'''

from random import choice


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
        return f'University {self.name}: \n    Tutors: {self.tutors} \n    Students: {self.groups}'

    def hire(self, other):
        if isinstance(other, Tutor):
            self.tutors.add((other.name, other.subject))

    def enroll(self, other, group=1):
        if isinstance(other, Student):
            if group in self.groups.keys():
                if len(self.groups[group]) < 2:
                    self.groups[group] += [other.name]
                    other.university = self.name
                    other.group = group
                else:
                    i = 1
                    while True:
                        if i in self.groups.keys():
                            if len(self.groups[i]) < 2:
                                self.groups[i] += [other.name]
                                break
                            else:
                                i += 1
                        else:
                            self.groups[i] = [other.name]
                            break
            else:
                self.groups[group] = [other.name]


class Student(Human):
    def __init__(self, name):
        super().__init__(name)
        self.group = None
        self.university = None
        self.knowledge = []

    def __str__(self):
        return f'{self.name} is a student at {self.university} in {self.group} group, knowledge: {", ".join(self.knowledge)}'

    def answer(self, question):
        answers = ['correctly', 'not correctly']
        print(f'{self.name} answers on qustion № {question} {choice(answers)}')


class Tutor(Human):
    def __init__(self, name, subject: str):
        super().__init__(name)
        self.subject = subject

    def __str__(self):
        return f'{self.name} is a tutor'

    def educate(self):
        pass

    def examinate(self):
        questions = [str(x) for x in range(100)]
        return choice(questions)

    def teach(self, other):
        if isinstance(other, Student):
            if not (self.subject in other.knowledge):
                other.knowledge.append(self.subject)


smtu = University('SMTU')

anton = Student('Anton')
michael = Student('Michael')
egor = Student('Egor')

smtu.enroll(anton)
smtu.enroll(michael)
smtu.enroll(egor)

ella = Tutor('Ella', 'math')
boris = Tutor('Boris', 'physics')

smtu.hire(ella)
smtu.hire(boris)

ella.teach(anton)

print(smtu)
