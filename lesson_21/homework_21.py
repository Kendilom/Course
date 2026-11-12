import os
import random

from sqlalchemy import Column, ForeignKey, Integer, String, Table, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, selectinload

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:password@localhost:5678/postgres")

engine = create_engine(DATABASE_URL, echo=False)


class Base(DeclarativeBase):
    pass


enrollments = Table(
    "enrollments",
    Base.metadata,
    Column("student_id", ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
    Column("course_id", ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True),
)


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    age: Mapped[int] = mapped_column(Integer)

    courses: Mapped[list["Course"]] = relationship(
        secondary=enrollments,
        back_populates="students",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"Student(id={self.id}, {self.first_name} {self.last_name}, {self.email})"


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(255), default="")

    students: Mapped[list[Student]] = relationship(
        secondary=enrollments,
        back_populates="courses",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"Course(id={self.id}, title={self.title!r})"


def init_db() -> None:
    Base.metadata.create_all(engine)


def reset_db() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


FIRST_NAMES = [
    "Олександр", "Марія", "Іван", "Анна", "Дмитро", "Ольга", "Андрій",
    "Катерина", "Максим", "Софія", "Богдан", "Юлія", "Тарас", "Наталія",
    "Віктор", "Ірина", "Сергій", "Олена", "Роман", "Вікторія",
]
LAST_NAMES = [
    "Шевченко", "Коваленко", "Бондаренко", "Ткаченко", "Кравченко",
    "Мельник", "Олійник", "Шевчук", "Мороз", "Лисенко",
    "Гончар", "Петренко", "Савчук", "Руденко", "Литвин",
    "Поліщук", "Кузьменко", "Бойко", "Павленко", "Гриценко",
]
COURSES = [
    ("Python", "Основи програмування на Python"),
    ("Бази даних", "SQL та проєктування баз даних"),
    ("Веб-розробка", "HTML, CSS та бекенд-фреймворки"),
    ("Алгоритми", "Алгоритми та структури даних"),
    ("Машинне навчання", "Вступ до машинного навчання"),
]


def seed_data(session: Session) -> None:
    courses = [Course(title=t, description=d) for t, d in COURSES]
    session.add_all(courses)

    students = []
    for i in range(20):
        students.append(
            Student(
                first_name=FIRST_NAMES[i],
                last_name=LAST_NAMES[i],
                email=f"student{i + 1}@example.com",
                age=random.randint(17, 25),
            )
        )
    session.add_all(students)

    for student in students:
        student.courses = random.sample(courses, k=random.randint(1, 3))

    session.commit()



def add_student(session, first_name, last_name, email, age) -> Student:
    student = Student(first_name=first_name, last_name=last_name, email=email, age=age)
    session.add(student)
    session.commit()
    return student


def enroll_student(session, student_id, course_title) -> None:
    student = session.get(Student, student_id)
    course = session.scalar(select(Course).where(Course.title == course_title))
    if student is None or course is None:
        raise ValueError("Студента або курс не знайдено")
    if course not in student.courses:
        student.courses.append(course)
        session.commit()


def add_student_to_course(
    session, first_name, last_name, email, age, course_title) -> Student:

    course = session.scalar(select(Course).where(Course.title == course_title))
    if course is None:
        raise ValueError(f"Курс '{course_title}' не знайдено")
    student = Student(first_name=first_name, last_name=last_name, email=email, age=age)
    student.courses.append(course)
    session.add(student)
    session.commit()
    return student



def get_students_by_course(session: Session, course_title: str) -> list[Student]:
    stmt = (
        select(Student)
        .join(Student.courses)
        .where(Course.title == course_title)
        .order_by(Student.last_name)
    )
    return list(session.scalars(stmt))


def get_courses_by_student(session: Session, student_id: int) -> list[Course]:
    stmt = (
        select(Course)
        .join(Course.students)
        .where(Student.id == student_id)
        .order_by(Course.title)
    )
    return list(session.scalars(stmt))



def update_student(session, student_id, **fields) -> Student:

    student = session.get(Student, student_id)
    if student is None:
        raise ValueError("Студента не знайдено")
    allowed = {"first_name", "last_name", "email", "age"}
    for key, value in fields.items():
        if key not in allowed:
            raise ValueError(f"Поле '{key}' не можна змінювати")
        setattr(student, key, value)
    session.commit()
    return student


def update_course(session, course_id, **fields) -> Course:
    course = session.get(Course, course_id)
    if course is None:
        raise ValueError("Курс не знайдено")
    allowed = {"title", "description"}
    for key, value in fields.items():
        if key not in allowed:
            raise ValueError(f"Поле '{key}' не можна змінювати")
        setattr(course, key, value)
    session.commit()
    return course


def delete_student(session, student_id) -> None:
    student = session.get(Student, student_id)
    if student is None:
        raise ValueError("Студента не знайдено")
    session.delete(student)
    session.commit()


def print_distribution(session: Session) -> None:
    courses = session.scalars(
        select(Course).options(selectinload(Course.students)).order_by(Course.id)
    )
    for course in courses:
        print(f"  {course.title}: {len(course.students)} студентів")


def main() -> None:
    reset_db()

    with Session(engine) as session:
        seed_data(session) #заповнює таблицю студентами
        print_distribution(session) #виводить по ним данні

        new_student = add_student_to_course( #додає студента і курс до нього
            session, "Петро", "Новіков", "petro.novikov@example.com", 21, "Python"
        )

        enroll_student(session, new_student.id, "Бази даних") #додавання студента до курсу
        print(get_courses_by_student(session, new_student.id)) #виводить результат


        for s in get_students_by_course(session, "Python"): # виводить результат функції, яка знаходить студентів відповідного курсу
            print(s)


        first = session.scalar(select(Student).order_by(Student.id))
        print(f"Курси {first.first_name} {first.last_name}:") # виводить курси першого студента
        for c in get_courses_by_student(session, first.id):
            print(c)

        update_student(session, new_student.id, last_name="Новіченко", age=22) #оновлення данних студента
        print("Оновлено студента:", session.get(Student, new_student.id)) #результат

        python_course = session.scalar(select(Course).where(Course.title == "Python"))
        update_course(session, python_course.id, description="Python для початківців (оновлено)") #оновлення курсу
        print("Оновлено курс:", python_course) # результ

        delete_student(session, new_student.id) # видаляє студента
        print("Студента видалено", session.get(Student, new_student.id) is None) # перевірка

        print_distribution(session)


if __name__ == "__main__":
    main()
