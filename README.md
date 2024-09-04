# MPI task scheduler in Python 
This Python program implements a parallel task scheduler system using MPI, simulating a distributed environment where multiple servers handle tasks concurrently. The scenario is that several tasks with varying durations arrive at different times and then are processed by multiple worker processes managed by a master process.
\
The program begins with generating a group of tasks with ID, arrival time, and duration. The master process controls the task scheduling until all the tasks are finished. It assigns tasks to inactive worker processes and collects the results (actual process time) once the tasks are completed. 
### Master Process
- Master process enters a for loop until all the tasks have finished.
- It assigns tasks to inactive workers as they arrive.
- If all workers are busy, the master probes the workers to see if they have finished the tasks. If so, the master collects the result, marks the worker as inactive, and updates the number of completed tasks.
- After all tasks are processed, the master signals all workers to stop.
### Worker Process
- Each worker waits for tasks from the master process. They do not have active status by themselves.
- Upon receiving a task, the worker processes it, simulating the running time based on its duration.
- Once the task is processed, the worker sends the result (print message and processing time) back to the master and then waits for the next task or a termination signal.
## Example output:
Task 6 completed in 5.80 seconds\
.\
.\
.\
Task 32 completed in 0.86 seconds\
Task 91 completed in 4.51 seconds\
All tasks completed in 49.45 seconds\
Total process time for all tasks: 475.61 units
