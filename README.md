# Software System Design: Architecture and Scalability (Part 2)

## Overview

This repository contains the solution for **Part 2 – Software System Design: Architecture and Scalability**. The solution includes system architecture design, low-level class design, design patterns, and fault-tolerant system design for the Student Academic Record System (SARS).

---

# Repository Contents

* **system_design.md** – Tasks 2.1 and 2.2 (requirements, architecture, scalability, and high-level design).
* **lld_classes.py** – Student and Enrollment classes together with the EnrollmentRepository interface.
* **singleton_demo.py** – Thread-safe Singleton implementation for the shared database connection.
* **observer_demo.py** – Observer pattern implementation for marks update notifications.
* **README.md** – Design decisions and implementation explanations.

---

# Architecture Decisions (Task 2.1)

The system adopts a **Microservices Architecture** because SARS is expected to support approximately **50,000 concurrent users** during examination result publication.

The application is divided into independent services such as:

* Authentication Service
* Student Portal Service
* Admin Panel Service
* Course Management Service
* Notification Service

This architecture was selected because it provides:

* Independent deployment of services.
* Better scalability by scaling only heavily used services.
* Improved fault isolation, allowing one service to fail without stopping the entire application.
* Easier long-term maintenance and future expansion.

Although microservices introduce additional deployment and management complexity, their scalability and reliability make them more suitable than a monolithic architecture for this scenario.

---

# Application of SOLID Principles

## Single Responsibility Principle (SRP)

The **Student** class is responsible only for storing and managing student information.

It intentionally does **not** contain email notification functionality. Notification responsibilities are handled by dedicated notification classes.

---

## Open/Closed Principle (OCP)

The **Enrollment** class is designed to support extension through inheritance.

The example **WaitlistedEnrollment** class extends the base Enrollment class without requiring any modifications to the original implementation.

---

## Dependency Inversion Principle (DIP)

The application depends on the **EnrollmentRepository** abstraction instead of a concrete database implementation.

This allows different storage implementations (for example, an in-memory repository or a relational database) to be substituted without changing the business logic.

---

# Observer Pattern Rationale (Task 2.3d)

The Observer pattern keeps the Admin Panel loosely coupled from the notification services.

Whenever a student's marks are updated, the **MarksUpdateNotifier** (subject) informs all registered observers.

The implementation includes:

* EmailNotifier
* AuditLogNotifier

The Admin Panel does not communicate directly with these services. Instead, it only notifies the subject, which forwards updates to every registered observer.

This design improves maintainability because additional notification services can be introduced without modifying the Admin Panel.

---

# Redundancy Strategy (Task 2.4)

To achieve high availability during examination result publication, redundancy is applied to the database tier.

A **primary-replica database architecture** is used in which data is replicated from the primary database server to one or more replica servers.

If the primary server fails:

* A replica is promoted to become the new primary server.
* Read operations continue using the promoted replica.
* Write operations are redirected to the new primary after failover.
* Replication is re-established once the failed server is recovered or replaced.

This approach minimizes downtime, improves fault tolerance, and reduces the risk of data loss.

---

# Programming Language

The implementation uses **Python 3**.

---

# References

The following resources were consulted while preparing this assignment:

* *Design Patterns: Elements of Reusable Object-Oriented Software* by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides.
* Robert C. Martin, *Agile Software Development: Principles, Patterns, and Practices*.
* Python 3 Official Documentation.
* General software engineering concepts related to microservices, scalability, SOLID principles, Singleton, and Observer design patterns.

All source code and written explanations were prepared specifically for this assignment.
