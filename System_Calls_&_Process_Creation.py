# ============================================================
# SYSTEM CALLS AND PROCESS CREATION
# ============================================================



# ============================================================
# 1. IMPORT REQUIRED MODULES
# ============================================================

import os
import subprocess


# ============================================================
# 2. MAIN PROGRAM
# ============================================================

def main():

    print("=" * 60)
    print("SYSTEM CALLS AND PROCESS CREATION")
    print("=" * 60)


    # ========================================================
    # 3. DISPLAY INITIAL PROCESS INFORMATION
    # ========================================================

    print("\n--- PARENT PROCESS INFORMATION ---")

    # os.getpid() gives the Process ID of the current process
    parent_pid = os.getpid()

    # os.getppid() gives the Parent Process ID
    parent_parent_pid = os.getppid()

    print("Parent Process ID     :", parent_pid)
    print("Parent's Process ID   :", parent_parent_pid)


    # ========================================================
    # 4. CREATE A CHILD PROCESS
    # ========================================================

    print("\n--- PROCESS CREATION ---")

    # os.fork() creates a child process.
    #
    # After fork():
    #   > Parent receives the child's PID
    #   > Child receives 0
    #
    # fork() is available on Linux/Unix systems.

    child_pid = os.fork()


    # ========================================================
    # 5. CHILD PROCESS
    # ========================================================

    if child_pid == 0:

        print("\n--- CHILD PROCESS ---")

        # Get the child's own Process ID
        current_pid = os.getpid()

        # Get the child's Parent Process ID
        parent_pid_of_child = os.getppid()

        print("Child Process ID      :", current_pid)
        print("Parent Process ID     :", parent_pid_of_child)


        # ====================================================
        # 6. EXECUTE A HARMLESS LINUX COMMAND
        # ====================================================

        print("\n--- LINUX COMMAND FROM CHILD PROCESS ---")

        print("Command: pwd")

        # pwd only displays the current working directory.
        # It does not modify the system.

        result = subprocess.run(
            ["pwd"],
            capture_output=True,
            text=True
        )

        print("Current Directory:", result.stdout.strip())


        # ====================================================
        # 7. CREATE AND WRITE TO A CONTROLLED TEST FILE
        # ====================================================

        print("\n--- FILE CREATION AND WRITING ---")

        file_name = "system_call_test.txt"

        try:

            # Open file in write mode
            file = open(file_name, "w")

            # Write controlled information into the file
            file.write("System Calls and Process Creation Test\n")
            file.write("This file was created by the child process.\n")

            # Close the file
            file.close()

            print("File created :", file_name)
            print("Data written successfully.")
            print("File closed successfully.")

        except Exception as error:

            print("File creation error:", error)


        # ====================================================
        # 8. READ THE CONTROLLED TEST FILE
        # ====================================================

        print("\n--- FILE READING ---")

        try:

            # Open file in read mode
            file = open(file_name, "r")

            # Read the contents
            content = file.read()

            # Close the file
            file.close()

            print("File contents:")
            print(content)

            print("File read and closed successfully.")

        except Exception as error:

            print("File reading error:", error)


        # ====================================================
        # 9. INSPECT /proc INTERFACE
        # ====================================================

        print("\n--- /proc INTERFACE ---")

        # /proc is a Linux virtual filesystem.
        # /proc/self represents the currently running process.

        proc_path = "/proc/self/status"

        try:

            # Open the process information file
            file = open(proc_path, "r")

            print("Reading:", proc_path)

            # Read the first few lines
            for i in range(5):

                line = file.readline()

                if line:
                    print(line.strip())

            # Close the file
            file.close()

            print("/proc interface inspected successfully.")

        except Exception as error:

            print("/proc error:", error)


        # ====================================================
        # 10. HANDLE INVALID PATH / FAILED FILE OPERATION
        # ====================================================

        print("\n--- ERROR HANDLING ---")

        invalid_path = "/this/path/does/not/exist.txt"

        try:

            # This path intentionally does not exist.
            # It is used to demonstrate error handling.

            file = open(invalid_path, "r")

            content = file.read()

            file.close()

        except FileNotFoundError:

            print("Error handled successfully.")
            print("Invalid path:", invalid_path)
            print("Error: File or directory does not exist.")

        except Exception as error:

            print("Unexpected file error:", error)


        # ====================================================
        # 11. CHILD PROCESS FINISHED
        # ====================================================

        print("\nChild process completed its work.")

        # Exit the child process.
        os._exit(0)


    # ========================================================
    # 12. PARENT PROCESS
    # ========================================================

    else:

        print("\n--- PARENT PROCESS ---")

        print("Parent Process ID :", os.getpid())

        print("Child Process ID  :", child_pid)


        # ====================================================
        # 13. WAIT FOR CHILD PROCESS
        # ====================================================

        print("\n--- WAITING FOR CHILD PROCESS ---")

        # os.waitpid() makes the parent wait until
        # the child process finishes.

        finished_pid, status = os.waitpid(
            child_pid,
            0
        )

        print(
            "Parent waited for child process:",
            finished_pid
        )

        print("Child process completed.")


        # ====================================================
        # 14. FINAL PROCESS INFORMATION
        # ========================================================

        print("\n--- PROCESS EVIDENCE ---")

        print("Parent Process ID :", os.getpid())
        print("Child Process ID  :", finished_pid)

        print("Child exit status :", status)


        # ====================================================
        # 15. FINAL MESSAGE
        # ========================================================

        print("\n" + "=" * 60)
        print("PROGRAM COMPLETED SUCCESSFULLY")
        print("=" * 60)


# ============================================================
# 16. START THE PROGRAM
# ============================================================

if __name__ == "__main__":
    main()