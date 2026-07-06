# ==========================================================
# singleton_demo.py
# Part 2
# Task 2.3(c)
# Thread-Safe Singleton Design Pattern
# ==========================================================

import threading


class DatabaseConnection:
    """
    Thread-safe Singleton implementation.

    This class ensures that only one DatabaseConnection
    object exists throughout the application's lifetime.
    """

    # Shared Singleton instance
    _instance = None

    # Lock used to prevent multiple threads from creating
    # more than one instance simultaneously.
    _lock = threading.Lock()

    def __new__(cls):
        """
        Double-checked locking implementation.

        The first check avoids unnecessary locking once the
        Singleton has already been created.
        """

        if cls._instance is None:

            with cls._lock:

                # Second check ensures another thread has not
                # already created the instance while waiting.
                if cls._instance is None:
                    cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        # Prevent reinitialization.
        if hasattr(self, "_initialized"):
            return

        self.connection = "Shared Database Connection"
        self._initialized = True

    def get_connection(self):
        """
        Returns the shared database connection.
        """
        return self.connection


# ==========================================================
# Why locking is required
# ==========================================================

"""
Naive lazy initialization without locking is not thread-safe.

If two threads execute:

    if instance is None:

at the same time, both may find that no instance exists.

Each thread can then create a new object, resulting in
multiple Singleton instances.

Using threading.Lock() ensures that only one thread can
create the instance at a time.
"""


# ==========================================================
# Demonstration
# ==========================================================

def worker(thread_number):
    connection = DatabaseConnection()

    print(
        f"Thread {thread_number}: "
        f"Object ID = {id(connection)}, "
        f"Connection = {connection.get_connection()}"
    )


if __name__ == "__main__":

    threads = []

    for i in range(5):
        thread = threading.Thread(
            target=worker,
            args=(i + 1,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
