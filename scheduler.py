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

def generate_tasks(num_tasks, max_arrival_time, max_duration):
    return [Task(i, 
                 np.random.randint(0, max_arrival_time), 
                 np.random.randint(1, max_duration + 1)) 
            for i in range(num_tasks)]

def process_task(task):
    actual_duration = task.duration * (0.8 + 0.4 * np.random.random())
    time.sleep(actual_duration * 0.1)  # Simulate processing time with less time
    return f"Task {task.id} completed in {actual_duration:.2f} seconds", actual_duration

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        # Master process
        num_tasks = 100
        max_arrival_time = 50
        max_duration = 10
        
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
                    if worker not in active_workers:
                        comm.send(tasks[task_index], dest=worker)
                        active_workers.add(worker)
                        task_index += 1
                        break
                else:
                    break  # No available workers

            # Check for completed tasks
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
        # Worker processes
        while True:
            task = comm.recv(source=0)
            if task is None:
                break
            result, actual_duration = process_task(task)
            comm.send((result, actual_duration), dest=0)

if __name__ == "__main__":
    main()