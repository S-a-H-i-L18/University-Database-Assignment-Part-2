# ==========================================================
# lld_classes.py
# Part 2
# Task 2.3(a)
# Student and Enrollment Classes
# ==========================================================

from abc import ABC, abstractmethod
from typing import List, Optional


# ==========================================================
# Student Class
# ==========================================================

class Student:
    """
    Represents a student in the Student Portal.

    SOLID Principle:
    Single Responsibility Principle (SRP)

    This class is responsible only for storing and managing
    student information.

    It does NOT send email notifications.
    """

    def __init__(
        self,
        student_id: int,
        name: str,
        department: str,
        email: str
    ):
        self.student_id = student_id
        self.name = name
        self.department = department
        self.email = email

    # -----------------------------
    # Getter Methods
    # -----------------------------

    def get_student_id(self) -> int:
        return self.student_id

    def get_name(self) -> str:
        return self.name

    def get_department(self) -> str:
        return self.department

    def get_email(self) -> str:
        return self.email

    # -----------------------------
    # Update Methods
    # -----------------------------

    def update_department(self, department: str) -> None:
        self.department = department

    def update_email(self, email: str) -> None:
        self.email = email

    # -----------------------------
    # Display Information
    # -----------------------------

    def display_student(self) -> None:
        print("Student ID :", self.student_id)
        print("Name       :", self.name)
        print("Department :", self.department)
        print("Email      :", self.email)


# ==========================================================
# Enrollment Class
# ==========================================================

class Enrollment:
    """
    Represents a student's enrollment.

    SOLID Principle:
    Open/Closed Principle (OCP)

    This class is designed to be extended through inheritance.
    New enrollment types (for example WaitlistedEnrollment)
    can inherit from this class without modifying it.
    """

    def __init__(
        self,
        enrollment_id: int,
        student: Student,
        course_code: str,
        enrollment_year: int,
        marks: Optional[float] = None
    ):
        self.enrollment_id = enrollment_id
        self.student = student
        self.course_code = course_code
        self.enrollment_year = enrollment_year
        self.marks = marks

    # -----------------------------
    # Getter Methods
    # -----------------------------

    def get_enrollment_id(self) -> int:
        return self.enrollment_id

    def get_student(self) -> Student:
        return self.student

    def get_course_code(self) -> str:
        return self.course_code

    def get_enrollment_year(self) -> int:
        return self.enrollment_year

    def get_marks(self) -> Optional[float]:
        return self.marks

    # -----------------------------
    # Update Methods
    # -----------------------------

    def update_marks(self, marks: float) -> None:
        self.marks = marks

    # -----------------------------
    # Business Method
    # -----------------------------

    def display_enrollment(self) -> None:
        print("Enrollment ID :", self.enrollment_id)
        print("Student       :", self.student.get_name())
        print("Course Code   :", self.course_code)
        print("Year          :", self.enrollment_year)
        print("Marks         :", self.marks)


# ==========================================================
# Example Extension
# Demonstrates Open/Closed Principle
# ==========================================================

class WaitlistedEnrollment(Enrollment):

    def __init__(
        self,
        enrollment_id: int,
        student: Student,
        course_code: str,
        enrollment_year: int,
        waitlist_position: int
    ):
        super().__init__(
            enrollment_id,
            student,
            course_code,
            enrollment_year
        )

        self.waitlist_position = waitlist_position

    def display_waitlist(self) -> None:
        print(
            f"{self.student.get_name()} "
            f"is waitlisted at position "
            f"{self.waitlist_position}"
        )
# ==========================================================
# Task 2.3(b)
# EnrollmentRepository Interface
# ==========================================================

class EnrollmentRepository(ABC):
    """
    EnrollmentRepository Interface

    SOLID Principle:
    Dependency Inversion Principle (DIP)

    High-level modules should depend on this abstraction
    instead of depending on a specific database implementation.
    """

    @abstractmethod
    def save(self, enrollment: Enrollment) -> None:
        """Save an enrollment record."""
        pass

    @abstractmethod
    def find_by_id(self, enrollment_id: int) -> Optional[Enrollment]:
        """Return an enrollment by its ID."""
        pass

    @abstractmethod
    def find_by_student(
        self,
        student_id: int
    ) -> List[Enrollment]:
        """Return all enrollments for a student."""
        pass

    @abstractmethod
    def update(self, enrollment: Enrollment) -> None:
        """Update an existing enrollment."""
        pass

    @abstractmethod
    def delete(self, enrollment_id: int) -> None:
        """Delete an enrollment."""
        pass


# ==========================================================
# Example Repository Implementation
# (Simple in-memory implementation for demonstration)
# ==========================================================

class InMemoryEnrollmentRepository(EnrollmentRepository):

    def __init__(self):
        self.enrollments = {}

    def save(self, enrollment: Enrollment) -> None:
        self.enrollments[enrollment.enrollment_id] = enrollment

    def find_by_id(
        self,
        enrollment_id: int
    ) -> Optional[Enrollment]:
        return self.enrollments.get(enrollment_id)

    def find_by_student(
        self,
        student_id: int
    ) -> List[Enrollment]:

        result = []

        for enrollment in self.enrollments.values():
            if enrollment.student.student_id == student_id:
                result.append(enrollment)

        return result

    def update(self, enrollment: Enrollment) -> None:
        self.enrollments[enrollment.enrollment_id] = enrollment

    def delete(self, enrollment_id: int) -> None:
        if enrollment_id in self.enrollments:
            del self.enrollments[enrollment_id]


# ==========================================================
# Demonstration
# ==========================================================

if __name__ == "__main__":

    student = Student(
        student_id=101,
        name="Aman",
        department="Computer Science",
        email="aman@university.edu"
    )

    enrollment = Enrollment(
        enrollment_id=1,
        student=student,
        course_code="CS101",
        enrollment_year=2025,
        marks=88.5
    )

    repository = InMemoryEnrollmentRepository()

    repository.save(enrollment)

    print("Student Details")
    print("----------------")
    student.display_student()

    print("\nEnrollment Details")
    print("-------------------")
    enrollment.display_enrollment()

    print("\nEnrollment Retrieved From Repository")
    print("------------------------------------")

    retrieved = repository.find_by_id(1)

    if retrieved:
        retrieved.display_enrollment()    
