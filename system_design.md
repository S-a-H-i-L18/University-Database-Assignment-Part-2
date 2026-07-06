# Software System Design: Architecture and Scalability

## Part 2

# Task 2.1 – Requirements and Architecture Choice

## Task 2.1(a)

### Functional Requirements

1. **User Authentication**

   The system shall allow students, faculty members, and administrators to securely log in using their registered credentials before accessing the system.

2. **Student Portal**

   The system shall allow students to view examination results, enroll in available courses, and access their academic information.

3. **Admin Panel**

   The system shall allow administrators to manage student records, faculty details, courses, and examination marks.

---

### Non-Functional Requirements

| Non-Functional Requirement          | Design Principle Addressed | Explanation                                                                                                                        |
| ----------------------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| High Availability                   | Availability               | The system should remain operational during examination result publication when thousands of students access it simultaneously.    |
| Secure Access Control               | Security                   | User authentication, authorization, and secure communication must protect sensitive academic information from unauthorized access. |
| Fast Response Time under Heavy Load | Scalability                | The system should efficiently support approximately 50,000 concurrent users without significant performance degradation.           |

---

## Task 2.1(b)

### Comparison of Monolithic and Microservices Architecture

| Comparison Factor      | Monolithic Architecture                                                                                     | Microservices Architecture                                                                                          |
| ---------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Independent Deployment | The entire application must be deployed whenever any module changes.                                        | Each service can be developed, tested, and deployed independently without affecting other services.                 |
| Fault Isolation        | A failure in one module can potentially impact the entire application.                                      | Failure of one service is generally isolated, allowing other services to continue operating.                        |
| Management Complexity  | Easier to develop, deploy, and manage for small applications because everything exists within one codebase. | More complex due to multiple services, service communication, deployment, monitoring, and configuration management. |

### Recommended Architecture

For SARS, a **Microservices Architecture** is the recommended choice because the system must support approximately **50,000 concurrent users** during examination result publication. Independent deployment enables different modules such as Authentication, Student Portal, and Admin Panel to be updated without redeploying the entire application. Fault isolation improves system reliability because failure of one service does not necessarily stop the remaining services. Although microservices increase management complexity, the scalability, flexibility, and resilience they provide make them more suitable for a large public-facing university application.

---

# Task 2.2 – High-Level Design

## Task 2.2(a)

### Main Components of SARS

| Component                 | Single Responsibility                                                                             | Interface Exposed              |
| ------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------ |
| Authentication Service    | Authenticate users, manage login sessions, and authorize access based on user roles.              | REST API                       |
| Student Portal Service    | Allow students to view marks, enroll in courses, and access personal academic information.        | REST API                       |
| Admin Panel Service       | Manage students, faculty, courses, and examination records.                                       | REST API                       |
| Course Management Service | Maintain course details, prerequisites, and enrollment information.                               | REST API                       |
| Notification Service      | Send email notifications and academic alerts to students and faculty.                             | REST API                       |
| Database Service          | Store and retrieve persistent university data such as students, courses, enrollments, and marks.  | Database Query Interface (SQL) |
| Load Balancer             | Distribute incoming requests among available web servers to improve performance and availability. | HTTP/HTTPS Request Routing     |

### Component Responsibilities

**Authentication Service**

Responsible for validating user credentials, generating authenticated sessions, and enforcing authorization policies.

**Student Portal Service**

Responsible for providing all student-related operations including viewing marks, course enrollment, profile information, and examination details.

**Admin Panel Service**

Responsible for maintaining university records including student management, faculty management, course creation, and marks updates.

**Course Management Service**

Responsible for handling course information, enrollment rules, prerequisites, and available course offerings.

**Notification Service**

Responsible for sending emails and notifications whenever important academic events occur such as marks publication or enrollment confirmation.

**Database Service**

Responsible for storing all application data securely and providing persistent storage for every module.

**Load Balancer**

Responsible for distributing incoming client requests across multiple application servers to ensure high availability and efficient utilization of server resources.
## Task 2.2(b)

### Layered Architecture for the Student Portal Module

The Student Portal follows a three-layer architecture consisting of the Presentation Layer, Business Layer, and Data Access Layer. Each layer has a specific responsibility and communicates only with the adjacent layer, improving maintainability, scalability, and separation of concerns.

---

### 1. Presentation Layer

**Responsibilities**

* Provides the user interface for students.
* Accepts requests such as login, viewing marks, and course enrollment.
* Validates basic user input before forwarding requests.
* Displays responses returned by the Business Layer.

**Receives**

* HTTP/HTTPS requests from students through a web browser or mobile application.

**Passes**

* Validated user requests and input data to the Business Layer.

---

### 2. Business Layer

**Responsibilities**

* Implements all business rules.
* Validates enrollment eligibility.
* Calculates academic information if required.
* Processes student requests.
* Coordinates communication between the Presentation Layer and Data Access Layer.

**Receives**

* Validated requests from the Presentation Layer.

**Passes**

* Database requests to the Data Access Layer.
* Processed results back to the Presentation Layer.

---

### 3. Data Access Layer

**Responsibilities**

* Executes SQL queries.
* Inserts, updates, deletes, and retrieves records.
* Manages database connectivity.
* Ensures secure interaction with the database.

**Receives**

* Query requests from the Business Layer.

**Passes**

* Student records, marks, enrollment information, and course details back to the Business Layer.

---

### Data Flow

Student Browser

↓

Presentation Layer

↓

Business Layer

↓

Data Access Layer

↓

Database

↓

Data Access Layer

↓

Business Layer

↓

Presentation Layer

↓

Student Browser

---

## Task 2.2(c)

### Scaling Strategy

To support approximately **50,000 concurrent users**, **Horizontal Scaling** is the preferred approach.

Horizontal scaling involves adding multiple web servers instead of increasing the hardware resources of a single server. This approach improves scalability, fault tolerance, and availability because additional servers can be added whenever system demand increases. If one server fails, the remaining servers continue serving client requests, ensuring uninterrupted service during examination result publication.

Vertical scaling is less suitable because there is a physical limit to how much CPU, memory, and storage can be added to a single server. It also creates a single point of failure.

---

### Load Balancing

A **Round Robin** load-balancing algorithm is suitable for SARS because all web servers are assumed to have similar hardware specifications and processing capacity.

Round Robin distributes incoming requests sequentially among all available servers, ensuring that the workload is shared evenly. This improves response time and prevents a single server from becoming overloaded during peak traffic.

Example distribution:

* Server A → User 1
* Server B → User 2
* Server C → User 3
* Server A → User 4
* Server B → User 5
* Server C → User 6

This continuous rotation provides simple and effective load distribution for servers with equal capacity.

---

## Task 2.2(d)

### Elasticity

Elasticity enables SARS to automatically adjust computing resources according to system demand.

During examination result publication, thousands of students access the system simultaneously. Additional web servers can be automatically provisioned to accommodate the increased workload, maintaining fast response times and system availability.

During semester breaks or other off-peak periods, user traffic decreases significantly. Elasticity allows unnecessary servers to be automatically removed, reducing infrastructure costs because only the required computing resources remain active.

This dynamic allocation of resources ensures that SARS delivers high performance during peak usage while minimizing operational expenses during periods of low demand.
## Task 2.2(e)

### Session Management Problem During Peak Load

During examination result publication, the load balancer distributes approximately **50,000 concurrent users** across three web servers using the **Round Robin** algorithm.

Suppose a student's login request is handled by **Server A**. After successful authentication, Server A creates an in-memory session containing the student's login information.

When the student sends another request (for example, to view examination marks), the Round Robin load balancer may forward that request to **Server B** instead of Server A.

Since each server maintains its own in-memory session store, Server B has no record of the session created on Server A. As a result, the student appears to be unauthenticated and may be redirected to the login page or receive an authorization error.

### Name of the Problem

This problem is known as **Session Affinity (Sticky Session) Issue** or **Session Persistence Problem**, where user session data is stored only on the server that originally handled the login request.

---

### Solution 1 – Sticky Sessions (Routing-Based)

Configure the load balancer to use **Sticky Sessions (Session Affinity)**.

With this approach, once a student's login request is handled by Server A, all subsequent requests from that student are routed to the same server throughout the session.

**Advantages**

* Simple to implement.
* No changes are required to the application code.
* Existing in-memory session storage can continue to be used.

**Trade-off**

If Server A becomes unavailable, the student's session is lost because it exists only on that server. Sticky sessions may also lead to uneven load distribution if many active users remain attached to one server.

---

### Solution 2 – Shared Session Storage

Store user sessions in a **centralized shared session store** instead of each server's local memory.

Examples include a distributed cache or a shared database that all web servers can access.

With this approach, regardless of whether a request is handled by Server A, Server B, or Server C, every server retrieves the student's session information from the shared session store.

**Advantages**

* Users can be served by any web server.
* Better fault tolerance because sessions survive individual web server failures.
* Improved load distribution since requests are no longer tied to a specific server.

**Trade-off**

Maintaining a centralized session store increases infrastructure cost and introduces additional network communication for every session lookup. The shared session store also becomes another critical component that must be highly available.

---

## Conclusion

For SARS, the preferred solution is **Shared Session Storage** because it provides better scalability, fault tolerance, and flexibility for handling approximately **50,000 concurrent users**. Although it introduces additional infrastructure cost, it enables efficient load balancing and prevents user sessions from being lost when requests are routed to different servers.
