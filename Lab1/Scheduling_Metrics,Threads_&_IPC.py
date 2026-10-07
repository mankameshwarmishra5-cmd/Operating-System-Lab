# ============================================================
# SYSTEM CALLS, PROCESSES, CPU SCHEDULING AND IPC
# Scheduling Metrics, Threads and Inter-Process Communication
# ============================================================


# ============================================================
# 1. IMPORT REQUIRED MODULES
# ============================================================

from threading import Thread, current_thread
from multiprocessing import Process, Pipe, Value


# ============================================================
# 2. PROCESS INFORMATION
# ============================================================

# Each process contains:
# pid     -> Process ID
# arrival -> Arrival Time
# burst   -> Burst Time

processes = [
    {"pid": "P1", "arrival": 0, "burst": 7},
    {"pid": "P2", "arrival": 2, "burst": 4},
    {"pid": "P3", "arrival": 4, "burst": 1},
    {"pid": "P4", "arrival": 5, "burst": 4},
]


# ============================================================
# 3. ROUND ROBIN EXECUTION INTERVALS
# ============================================================

# Each tuple contains:
# (Process ID, Start Time, End Time)
#
# These are the Round Robin execution slices.

intervals = [
    ("P1", 0, 2),
    ("P2", 2, 4),
    ("P1", 4, 6),
    ("P3", 6, 7),
    ("P2", 7, 9),
    ("P4", 9, 11),
    ("P1", 11, 13),
    ("P4", 13, 15),
    ("P1", 15, 16),
]


# ============================================================
# 4. CALCULATE SCHEDULING METRICS
# ============================================================

def calculate_metrics():

    print("\n" + "=" * 60)
    print("SCHEDULING METRICS")
    print("=" * 60)

    # CT  = Completion Time
    # TAT = Turnaround Time
    # WT  = Waiting Time
    # RT  = Response Time

    print("PID\tAT\tBT\tCT\tTAT\tWT\tRT")

    # Variables used to calculate averages
    tat_total = 0
    wt_total = 0
    rt_total = 0

    # Calculate metrics for every process
    for p in processes:

        pid = p["pid"]
        arrival = p["arrival"]
        burst = p["burst"]

        # Find all execution intervals belonging to this process
        runs = [
            x for x in intervals
            if x[0] == pid
        ]

        # First time the process gets CPU
        first_start = runs[0][1]

        # Last time the process finishes
        completion = runs[-1][2]

        # Turnaround Time
        # TAT = Completion Time - Arrival Time
        tat = completion - arrival

        # Waiting Time
        # WT = Turnaround Time - Burst Time
        wt = tat - burst

        # Response Time
        # RT = First CPU Start Time - Arrival Time
        rt = first_start - arrival

        # Add values for average calculation
        tat_total += tat
        wt_total += wt
        rt_total += rt

        # Display metrics
        print(
            f"{pid}\t"
            f"{arrival}\t"
            f"{burst}\t"
            f"{completion}\t"
            f"{tat}\t"
            f"{wt}\t"
            f"{rt}"
        )

    # Number of processes
    n = len(processes)

    # Display average values
    print("\n" + "-" * 60)
    print("AVERAGES")
    print("-" * 60)

    print(
        f"Average Turnaround Time: "
        f"{tat_total / n:.2f}"
    )

    print(
        f"Average Waiting Time   : "
        f"{wt_total / n:.2f}"
    )

    print(
        f"Average Response Time  : "
        f"{rt_total / n:.2f}"
    )


# ============================================================
# 5. DISPLAY GANTT CHART
# ============================================================

def show_gantt_chart(intervals):

    print("\n" + "=" * 60)
    print("ROUND ROBIN GANTT CHART")
    print("=" * 60)

    # Print process names
    print("| " + " | ".join(
        pid for pid, _, _ in intervals
    ) + " |")

    # Create time boundaries
    times = [intervals[0][1]]

    for _, start, end in intervals:
        times.append(end)

    # Print exact time boundaries
    print("  " + "   ".join(
        str(t) for t in times
    ))


# ============================================================
# 6. DISPLAY ROUND ROBIN EXECUTION SLICES
# ============================================================

def show_execution_slices(intervals):

    print("\n" + "=" * 60)
    print("ROUND ROBIN EXECUTION SLICES")
    print("=" * 60)

    print("Process\tStart\tEnd\tCPU Time")

    for pid, start, end in intervals:

        cpu_time = end - start

        print(
            f"{pid}\t"
            f"{start}\t"
            f"{end}\t"
            f"{cpu_time}"
        )


# ============================================================
# 7. CHECK AND DISPLAY CPU IDLE PERIODS
# ============================================================

def show_idle_periods(intervals):

    print("\n" + "=" * 60)
    print("CPU IDLE PERIODS")
    print("=" * 60)

    idle_found = False

    for i in range(len(intervals) - 1):

        current_end = intervals[i][2]
        next_start = intervals[i + 1][1]

        # If next process starts after current process ends,
        # CPU was idle during that interval.
        if next_start > current_end:

            idle_found = True

            print(
                f"CPU Idle: {current_end} - {next_start}"
            )

    if not idle_found:
        print("No CPU idle periods.")


# ============================================================
# 8. THREADING DEMONSTRATION
# ============================================================

# This function is executed by each thread.
def thread_task(name):

    # Get the ID of the current thread
    thread_id = current_thread().ident

    print(
        name,
        "| Running | Thread ID:",
        thread_id
    )

    # Display work completed by the thread
    print(
        name,
        "| Work completed: Scheduling analysis"
    )


# Create and run two threads
def thread_demo():

    print("\n" + "=" * 60)
    print("THREAD DEMONSTRATION")
    print("=" * 60)

    # Create Thread 1
    t1 = Thread(
        target=thread_task,
        args=("Thread 1",)
    )

    # Create Thread 2
    t2 = Thread(
        target=thread_task,
        args=("Thread 2",)
    )

    # Start both threads
    t1.start()
    t2.start()

    # Wait for both threads to finish
    t1.join()
    t2.join()

    print("Both threads completed.")


# ============================================================
# 9. INTER-PROCESS COMMUNICATION USING PIPE
# ============================================================

# This function runs inside the child process.
def child_process(child_conn):

    # Message sent from child process to parent process
    message = "Hello Parent, message from Child"

    # Send message through Pipe
    child_conn.send(message)

    # Close child side of Pipe
    child_conn.close()


def pipe_demo():

    print("\n" + "=" * 60)
    print("INTER-PROCESS COMMUNICATION USING PIPE")
    print("=" * 60)

    # Create a communication Pipe
    parent_conn, child_conn = Pipe()

    # Create child process
    child = Process(
        target=child_process,
        args=(child_conn,)
    )

    # Start child process
    child.start()

    # Parent receives the message
    message = parent_conn.recv()

    # Wait for child process to finish
    child.join()

    # Display process roles and message
    print("Process Role: Child Process")
    print("Transmitted Message:", message)

    print("Process Role: Parent Process")
    print("Received Message:", message)


# ============================================================
# 10. SHARED MEMORY DEMONSTRATION
# ============================================================

# This function runs in the child process.
def update_shared(value):

    # Increase the shared value by 10
    value.value += 10


def shared_memory_demo():

    print("\n" + "=" * 60)
    print("SHARED MEMORY DEMONSTRATION")
    print("=" * 60)

    # Create an integer stored in shared memory
    shared_value = Value("i", 5)

    print(
        "Before child process:",
        shared_value.value
    )

    # Create child process
    child = Process(
        target=update_shared,
        args=(shared_value,)
    )

    # Start child process
    child.start()

    # Wait for child process
    child.join()

    print(
        "After child process:",
        shared_value.value
    )


# ============================================================
# 11. EXPLANATION OF RESULTS
# ============================================================

def explain_results():

    print("\n" + "=" * 60)
    print("EXPLANATION OF RESULTS")
    print("=" * 60)

    print("\n1. SCHEDULING RESULTS")
    print(
        "Round Robin gives each ready process a fixed time slice. "
        "If a process is not completed within its time quantum, "
        "it can receive another CPU turn later."
    )

    print("\n2. BENEFITS OF THREADS")
    print(
        "Threads allow multiple tasks within a process to execute "
        "concurrently. Threads can improve responsiveness and "
        "allow tasks to work independently."
    )

    print("\n3. IPC USING PIPE")
    print(
        "A Pipe allows processes to communicate by sending and "
        "receiving messages. The child process sends the message "
        "and the parent process receives it."
    )

    print("\n4. LIMITATION OF PIPE")
    print(
        "A Pipe is mainly useful for communication between "
        "connected processes. Communication must be coordinated "
        "properly when multiple processes are involved."
    )

    print("\n5. SHARED MEMORY")
    print(
        "Shared memory allows processes to access a common value. "
        "It can be efficient, but simultaneous access may require "
        "proper synchronization."
    )


# ============================================================
# 12. MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SYSTEM CALLS, PROCESSES, CPU SCHEDULING AND IPC")
    print("=" * 60)

    print("\nINPUT PROCESSES")
    print("-" * 60)
    print("PID\tArrival Time\tBurst Time")

    for p in processes:

        print(
            f'{p["pid"]}\t'
            f'{p["arrival"]}\t\t'
            f'{p["burst"]}'
        )


    # --------------------------------------------------------
    # Scheduling Metrics
    # --------------------------------------------------------

    calculate_metrics()


    # --------------------------------------------------------
    # Gantt Chart
    # --------------------------------------------------------

    show_gantt_chart(intervals)


    # --------------------------------------------------------
    # Round Robin Execution Slices
    # --------------------------------------------------------

    show_execution_slices(intervals)


    # --------------------------------------------------------
    # CPU Idle Periods
    # --------------------------------------------------------

    show_idle_periods(intervals)


    # --------------------------------------------------------
    # Thread Demonstration
    # --------------------------------------------------------

    thread_demo()


    # --------------------------------------------------------
    # Pipe IPC Demonstration
    # --------------------------------------------------------

    pipe_demo()


    # --------------------------------------------------------
    # Shared Memory Demonstration
    # --------------------------------------------------------

    shared_memory_demo()


    # --------------------------------------------------------
    # Final Explanation
    # --------------------------------------------------------

    explain_results()


    print("\n" + "=" * 60)
    print("PROGRAM COMPLETED SUCCESSFULLY")
    print("=" * 60)