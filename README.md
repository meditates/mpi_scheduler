# MPI task scheduler in Python 
This Python program implements a parallel task scheduler system using MPI, simulating a distributed environment where multiple servers handle tasks concurrently. This system employs a Master-Worker pattern, characterized by centralized task distribution. 
\
\
The program begins with generating a group of tasks with ID, arrival time, and duration. By arrival time order, the master process controls the task scheduling until all the tasks are finished. It assigns tasks to inactive worker processes and collects the results (actual process time) once the tasks are completed. 
### Master Process
- Master maintains the active worker set.
- Master process enters a for loop and assigns tasks in time order to inactive workers, then set them as active.
- If all workers are busy, the master probes them to see if they have finished the tasks. If so, the master collects the result and marks the worker as inactive.
- After all tasks are processed, the master signals all workers to stop.
### Workers Process
- Each worker waits for tasks from the master process. They do not have active status by themselves.
- Upon receiving a task, the worker simulates processing it by sleeping for the running time based on duration.
- Once the task is processed, the worker sends the result (print message and processing time) back to the master and then waits for the next task or a termination signal.

## Run command: (e.g., using 16 processes)
mpiexec -n 16 python3 scheduler.py

## Example output:
Task 6 completed in 5.80 seconds\
.\
.\
.\
Task 32 completed in 0.86 seconds\
Task 91 completed in 4.51 seconds\
All tasks completed in 49.45 seconds\
Total process time for all tasks: 475.61 units
