import os

TEST_FILE = "test_file.txt"


def process_creation_demo():
    pid = os.fork()

    if pid == 0:
        print(f"Child process -> PID: {os.getpid()}, Parent PID: {os.getppid()}")
        os.execlp("echo", "echo", "Hello from exec, running inside the child process")
    else:
        os.wait()
        print(f"Parent process -> PID: {os.getpid()}, Parent PID: {os.getppid()}")


def file_operations_demo():
    fd = os.open(TEST_FILE, os.O_CREAT | os.O_WRONLY | os.O_TRUNC)
    os.write(fd, b"Hello from the OS lab test file\n")
    os.close(fd)

    fd = os.open(TEST_FILE, os.O_RDONLY)
    data = os.read(fd, 100)
    os.close(fd)

    print(f"Wrote, read and closed '{TEST_FILE}': {data.decode().strip()}")
    os.remove(TEST_FILE)


def device_interface_demo():
    fd = os.open("/dev/null", os.O_WRONLY)
    os.write(fd, b"this goes nowhere")
    os.close(fd)
    print("Wrote to /dev/null successfully (data is discarded, no error)")

    with open("/proc/version", "r") as f:
        print("Read /proc/version:", f.readline().strip())


def error_handling_demo():
    try:
        os.open("/no/such/path/file.txt", os.O_RDONLY)
    except OSError as e:
        print(f"Handled expected error opening invalid path: {e}")


print("PROCESS CREATION (fork + exec)")
process_creation_demo()

print("\nFILE OPERATIONS")
file_operations_demo()

print("\nDEVICE AND PROC INTERFACE")
device_interface_demo()

print("\nERROR HANDLING")
error_handling_demo()

print("\nSUMMARY")
print("Process creation, wait and exec: done")
print("File create/write/read/close: done")
print("Device (/dev/null) and /proc interface access: done")
print("Invalid path handled with a clear error message: done")