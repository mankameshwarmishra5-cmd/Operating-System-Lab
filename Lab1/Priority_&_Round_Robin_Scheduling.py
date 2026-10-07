# ============================================================
# CPU SCHEDULING SIMULATOR
# Priority Scheduling and Round Robin Scheduling
# ============================================================

# ------------------------------------------------------------
# 1. INPUT DATA
# ------------------------------------------------------------

# Each process contains:
# pid      -> Process ID
# arrival  -> Arrival Time
# burst    -> Burst Time
# priority -> Priority Number
#
# Priority rule:
# Smaller number = Higher Priority

processes = [
    {"pid": "P1", "arrival": 0, "burst": 7, "priority": 3},
    {"pid": "P2", "arrival": 2, "burst": 4, "priority": 1},
    {"pid": "P3", "arrival": 4, "burst": 1, "priority": 4},
    {"pid": "P4", "arrival": 5, "burst": 4, "priority": 2},
]

# Time quantum used by Round Robin
QUANTUM = 3


# ============================================================
# 2. NON-PREEMPTIVE PRIORITY SCHEDULING
# ============================================================

def priority_scheduling(process_list):

    # Create a copy of the process list.
    # This allows us to remove completed processes
    # without changing the original process list.
    remaining = [dict(p) for p in process_list]

    # Current CPU time
    current_time = 0

    # Stores the CPU execution intervals
    intervals = []

    # Continue until all processes are completed
    while remaining:

        # Find all processes that have already arrived
        ready = [
            p for p in remaining
            if p["arrival"] <= current_time
        ]

        # If no process is ready, CPU remains idle
        if not ready:

            # Find the next process that will arrive
            next_arrival = min(
                p["arrival"] for p in remaining
            )

            # Store the CPU idle interval
            intervals.append(
                ("IDLE", current_time, next_arrival)
            )

            # Move CPU time to the next arrival
            current_time = next_arrival

            continue

        # Select the process with the highest priority.
        #
        # Smaller priority number = higher priority.
        #
        # If priorities are equal:
        # 1. Earlier arrival time is selected
        # 2. If still equal, smaller PID is selected
        process = min(
            ready,
            key=lambda p: (
                p["priority"],
                p["arrival"],
                p["pid"]
            )
        )

        # Store starting time
        start = current_time

        # Calculate finishing time
        end = start + process["burst"]

        # Store the execution interval
        intervals.append(
            (process["pid"], start, end)
        )

        # Move CPU time forward
        current_time = end

        # Remove the completed process
        remaining.remove(process)

    return intervals


# ============================================================
# 3. ROUND ROBIN SCHEDULING
# ============================================================

def round_robin(process_list, quantum):

    # Create a copy of the process list
    remaining = [dict(p) for p in process_list]

    # Add remaining CPU time to every process
    for p in remaining:
        p["remaining"] = p["burst"]

    # Current CPU time
    current_time = 0

    # Stores CPU execution intervals
    intervals = []

    # Ready queue
    queue = []

    # Stores processes that have already entered the queue
    arrived = []

    # Continue while processes are still remaining
    # or the ready queue is not empty
    while remaining or queue:

        # Add all processes that have arrived
        # to the ready queue
        for p in remaining:

            if (
                p["arrival"] <= current_time
                and p not in arrived
                and p not in queue
            ):
                queue.append(p)

        # If ready queue is empty,
        # CPU has to remain idle
        if not queue:

            # Find the next arriving process
            next_arrival = min(
                p["arrival"]
                for p in remaining
                if p not in arrived
            )

            # Store CPU idle interval
            intervals.append(
                ("IDLE", current_time, next_arrival)
            )

            # Move CPU time to next arrival
            current_time = next_arrival

            continue

        # Remove the first process from the queue
        # Round Robin follows FIFO order
        process = queue.pop(0)

        # Mark the process as arrived
        if process not in arrived:
            arrived.append(process)

        # Store starting time
        start = current_time

        # Process can run for:
        # quantum OR its remaining time,
        # whichever is smaller
        run_time = min(
            quantum,
            process["remaining"]
        )

        # Calculate ending time
        end = start + run_time

        # Store this execution interval
        intervals.append(
            (process["pid"], start, end)
        )

        # Move CPU time forward
        current_time = end

        # Reduce the remaining CPU time
        process["remaining"] -= run_time

        # Check whether new processes arrived
        # while the current process was running
        for p in remaining:

            if (
                p["arrival"] <= current_time
                and p not in arrived
                and p not in queue
                and p is not process
            ):
                queue.append(p)

        # If the process still needs CPU time,
        # put it at the end of the queue
        if process["remaining"] > 0:
            queue.append(process)

        # Otherwise, the process has completed
        else:
            remaining.remove(process)

    return intervals


# ============================================================
# 4. DISPLAY EXECUTION INTERVALS
# ============================================================

def show_intervals(title, intervals):

    print("\n" + title)

    print("Process   Start   End")

    # Store the execution sequence
    sequence = []

    # Display every execution interval
    for pid, start, end in intervals:

        print(
            f"{pid:<9} {start:<7} {end}"
        )

        # Do not add IDLE to process sequence
        if pid != "IDLE":
            sequence.append(pid)

    # Display execution sequence
    print(
        "Sequence:",
        " -> ".join(sequence)
    )


# ============================================================
# 5. CALCULATE SCHEDULING METRICS
# ============================================================

def show_metrics(title, process_list, intervals):

    # Dictionary to store Completion Time
    completion = {}

    # Find the completion time of every process
    for pid, start, end in intervals:

        if pid != "IDLE":
            completion[pid] = end

    print("\n" + title)

    print(
        "PID   Arrival   Burst   "
        "Completion   Turnaround   Waiting"
    )

    # Variables for calculating averages
    total_tat = 0
    total_wt = 0

    # Calculate metrics for every process
    for p in process_list:

        # Completion Time
        ct = completion[p["pid"]]

        # Turnaround Time
        # TAT = Completion Time - Arrival Time
        tat = ct - p["arrival"]

        # Waiting Time
        # WT = Turnaround Time - Burst Time
        wt = tat - p["burst"]

        # Add values for average calculation
        total_tat += tat
        total_wt += wt

        # Display process metrics
        print(
            f'{p["pid"]:<5} '
            f'{p["arrival"]:<9} '
            f'{p["burst"]:<7} '
            f'{ct:<12} '
            f'{tat:<12} '
            f'{wt}'
        )

    # Number of processes
    n = len(process_list)

    # Calculate and display averages
    print(
        f"\nAverage Turnaround Time: "
        f"{total_tat / n:.2f}"
    )

    print(
        f"Average Waiting Time: "
        f"{total_wt / n:.2f}"
    )


# ============================================================
# 6. MAIN PROGRAM
# ============================================================

print("CPU SCHEDULING SIMULATOR")

print(
    "Priority Convention: "
    "Lower number = Higher priority"
)

print(
    "Ties broken by arrival time, then PID"
)

print(
    "Round Robin Time Quantum:",
    QUANTUM
)


# ------------------------------------------------------------
# Display Input Processes
# ------------------------------------------------------------

print("\nINPUT PROCESSES")

print("PID   AT   BT   PRIORITY")

for p in processes:

    print(
        f'{p["pid"]:<5} '
        f'{p["arrival"]:<4} '
        f'{p["burst"]:<4} '
        f'{p["priority"]}'
    )


# ============================================================
# 7. RUN PRIORITY SCHEDULING
# ============================================================

priority_intervals = priority_scheduling(processes)

# Display Priority Scheduling execution
show_intervals(
    "PRIORITY SCHEDULING (non-preemptive)",
    priority_intervals
)

# Display Priority Scheduling metrics
show_metrics(
    "Priority Scheduling Metrics",
    processes,
    priority_intervals
)


# ============================================================
# 8. RUN ROUND ROBIN SCHEDULING
# ============================================================

rr_intervals = round_robin(
    processes,
    QUANTUM
)

# Display Round Robin execution
show_intervals(
    f"ROUND ROBIN (quantum={QUANTUM})",
    rr_intervals
)

# Display Round Robin metrics
show_metrics(
    "Round Robin Metrics",
    processes,
    rr_intervals
)


# ============================================================
# END OF PROGRAM
# ============================================================