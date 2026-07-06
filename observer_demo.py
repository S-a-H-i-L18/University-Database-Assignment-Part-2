# ==========================================================
# observer_demo.py
# Part 2
# Task 2.3(d)
# Observer Design Pattern
# ==========================================================

from abc import ABC, abstractmethod


# ==========================================================
# Observer Interface
# ==========================================================

class Observer(ABC):

    @abstractmethod
    def update(self, student_id: int, new_marks: float):
        pass


# ==========================================================
# Email Notification Service
# ==========================================================

class EmailNotifier(Observer):

    def update(self, student_id: int, new_marks: float):

        print(
            f"[Email Service] "
            f"Email sent to student {student_id}: "
            f"Your marks have been updated to {new_marks}."
        )


# ==========================================================
# Audit Log Service
# ==========================================================

class AuditLogNotifier(Observer):

    def update(self, student_id: int, new_marks: float):

        print(
            f"[Audit Log] "
            f"Student {student_id} marks updated to {new_marks}."
        )


# ==========================================================
# Subject
# ==========================================================

class MarksUpdateNotifier:

    def __init__(self):

        self.observers = []

    # Register Observer

    def register(self, observer: Observer):

        self.observers.append(observer)

    # Deregister Observer

    def deregister(self, observer: Observer):

        if observer in self.observers:
            self.observers.remove(observer)

    # Notify all registered observers

    def notify(self, student_id: int, new_marks: float):

        for observer in self.observers:
            observer.update(student_id, new_marks)

    # Marks Update

    def update_marks(self, student_id: int, new_marks: float):

        print(
            f"\nAdmin updated marks of Student {student_id} "
            f"to {new_marks}\n"
        )

        self.notify(student_id, new_marks)


# ==========================================================
# Demonstration
# ==========================================================

if __name__ == "__main__":

    notifier = MarksUpdateNotifier()

    email_service = EmailNotifier()
    audit_service = AuditLogNotifier()

    # Register observers

    notifier.register(email_service)
    notifier.register(audit_service)

    # Notify observers

    notifier.update_marks(101, 91.5)

    print("\nRemoving Email Service...\n")

    # Deregister Email Service

    notifier.deregister(email_service)

    # Only Audit Log receives notification

    notifier.update_marks(101, 95.0)
