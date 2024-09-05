#!/usr/bin/env python3
# For ubuntu system, need mpich installed: sudo apt install libmpich-dev; pip install mpi4py
from mpi4py import MPI
import numpy as np
import time

class Task:
    def __init__(self, id, arrival_time, duration):
        self.id = id
        self.arrival_time = arrival_time
        self.duration = duration

# Generate a list of tasks
def generate_tasks(num_tasks, max_arrival_time, max_duration):
    tasks = []
    for i in range(num_tasks):
        arrival_time = np.random.randint(0, max_arrival_time)
        duration = np.random.randint(1, max_duration + 1)
        tasks.append(Task(i, arrival_time, duration))
    return tasks
    
def process_task(task):
    # Simulate actual processing time with some randomness
    actual_duration = task.duration * (0.8 + 0.4 * np.random.random())
    time.sleep(actual_duration * 0.1)  # Simulate the processing time
    return f"Task {task.id} completed in {actual_duration:.2f} seconds", actual_duration

def main():
    # Initialize MPI communication
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # Master process
    if rank == 0:
        # Default setting
        num_tasks = 100
        max_arrival_time = 50
        max_duration = 10

        # Generate random tasks and sort by time
        tasks = generate_tasks(num_tasks, max_arrival_time, max_duration)
        tasks.sort(key=lambda x: x.arrival_time) 

        start_time = time.time()
        task_index = 0
        completed_tasks = 0
        active_workers = set()
        total_process_time = 0

        while completed_tasks < num_tasks:
            current_time = time.time() - start_time

            # Assign tasks to available workers
            while task_index < num_tasks and tasks[task_index].arrival_time <= current_time:
                for worker in range(1, size):
                    if worker not in active_workers:  # Find available worker
                        comm.send(tasks[task_index], dest=worker)
                        active_workers.add(worker)
                        task_index += 1
                        break
                else:
                    break  # Go through all workers but no available workers

            # Check if any works have completed tasks
            for worker in list(active_workers):
                if comm.Iprobe(source=worker):
                    result, actual_duration = comm.recv(source=worker)
                    print(result)
                    active_workers.remove(worker)
                    completed_tasks += 1
                    total_process_time += actual_duration

        # Tell workers to stop
        for worker in range(1, size):
            comm.send(None, dest=worker)

        print(f"All tasks completed in {time.time() - start_time:.2f} seconds")
        print(f"Total process time for all tasks: {total_process_time:.2f} units")

    else:
        # Worker processes always listen
        while True: 
            task = comm.recv(source=0)
            if task is None: # Stop signal received
                break
            result, actual_duration = process_task(task)
            comm.send((result, actual_duration), dest=0)

if __name__ == "__main__":
    main()
