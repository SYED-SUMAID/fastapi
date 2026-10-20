# Python Asynchronous Programming

## 1. What Is Async Programming?

Asynchronous programming allows Python to handle multiple tasks without waiting for each task to finish before moving forward.

It is useful when tasks involve waiting, such as API requests, database queries, or delays.

## 2. Code Example

    import asyncio

    async def task1():
        print("Task 1 started")
        await asyncio.sleep(2)
        print("Task 1 completed")

    async def task2():
        print("Task 2 started")
        await asyncio.sleep(1)
        print("Task 2 completed")

    async def main():
        await asyncio.gather(task1(), task2())

    asyncio.run(main())

## 3. Output

    Task 1 started
    Task 2 started
    Task 2 completed
    Task 1 completed

## 4. Explanation

### Importing asyncio

    import asyncio

The `asyncio` module allows Python to run and manage asynchronous tasks.

### Creating an Asynchronous Function

    async def task1():

The `async` keyword defines an asynchronous function. Calling it creates a coroutine, which can be scheduled to run by the event loop.

Here, `task1()` and `task2()` are asynchronous functions.

### Using await

    await asyncio.sleep(2)

`asyncio.sleep(2)` pauses the current task for two seconds without blocking other asynchronous tasks from running.

- `task1()` waits for 2 seconds.
- `task2()` waits for 1 second.
- While one task is waiting, the other can continue.

The `await` keyword allows the current coroutine to wait for an asynchronous operation to finish.

### Using asyncio.gather()

    await asyncio.gather(task1(), task2())

`asyncio.gather()` runs both coroutines concurrently and waits for both to finish.

Instead of completing all of `task1()` before starting `task2()`, Python can switch between them while they wait.

### Creating the main() Function

    async def main():
        await asyncio.gather(task1(), task2())

The `main()` function brings both tasks together and waits for their completion.

### Running the Program

    asyncio.run(main())

`asyncio.run()` starts the event loop, runs the `main()` coroutine, and closes the event loop when the program finishes.

## 5. How Does It Work?

1. `asyncio.run(main())` starts the program.
2. `main()` schedules both tasks using `asyncio.gather()`.
3. Both tasks print their starting messages.
4. `task1()` waits for 2 seconds, while `task2()` waits for 1 second.
5. `task2()` finishes first and prints its completion message.
6. `task1()` finishes after its 2-second delay.
7. The program ends after both tasks are complete.

## 6. Important Concepts

| Concept | Meaning |
|---|---|
| `async` | Defines an asynchronous function |
| `await` | Waits for an asynchronous operation to finish |
| `asyncio` | Python's library for asynchronous programming |
| `asyncio.sleep()` | Pauses a task without blocking other asynchronous tasks |
| `asyncio.gather()` | Runs multiple awaitables concurrently and waits for them |
| `asyncio.run()` | Starts and runs an asynchronous program |
| Coroutine | An asynchronous operation that can be awaited or scheduled |

## 7. Key Takeaway

Without asynchronous programming, a task that waits for 2 seconds could make the program wait before starting the next task.

With `asyncio.gather()`, both tasks can make progress while waiting. In this example, the total execution time is approximately 2 seconds rather than 3 seconds, excluding minor overhead.

**Remember:** Asynchronous programming is especially useful for I/O-bound tasks, such as API calls and database operations, where waiting is common.