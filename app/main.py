import sys
import os
import subprocess

def handle_echo(args):
    print(" ".join(args))

def get_fn_path(fn_name):
    dirs = os.environ["PATH"].split(":")
    full_path = [os.path.join(dir, fn_name) for dir in dirs if os.path.exists(os.path.join(dir, fn_name))]
    if full_path and os.path.isfile(full_path[0]) and os.access(full_path[0], os.X_OK):
        return full_path[0]

def handle_type(args):
    if len(args) == 0:
        print("No args passed")

    built_in_cmds = ["echo", "exit", "type"]

    if args[0] in built_in_cmds: 
        sys.stdout.write(f"{args[0]} is a shell builtin\n")
        return
    
    if fn_path := get_fn_path(args[0]):
        sys.stdout.write(f"{args[0]} is {fn_path}\n")
        return

    sys.stdout.write(f"{args[0]} not found\n")

def handle_fn_exec(fn_path, args):
    subprocess.run([fn_path, *args])

def handle_pwd():
    sys.stdout.write(f"{os.getcwd()}\n")

def handle_cd(args):
    dir_path = args[0] if len(args) > 0 else "~"

    if dir_path == "~":
        home_dir = os.environ["HOME"]
        if os.path.isdir(home_dir):
            os.chdir(home_dir)
        return

    if not os.path.isdir(dir_path):
        sys.stdout.write(f"{dir_path}: No such file or directory\n")
        return

    if dir_path.startswith("."):
        os.chdir(os.path.normpath(os.path.join(os.getcwd(), dir_path)))
        return
    
    os.chdir(dir_path)


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        key, *args = input().split()
        
        if key == "exit":
            break
        if key == "echo":
            handle_echo(args)
        elif key == "type":
            handle_type(args)
        elif key == "pwd":
            handle_pwd()
        elif key == "cd":
            handle_cd(args)
        elif fn_path := get_fn_path(key):
            handle_fn_exec(fn_path, args)
        else:
            sys.stdout.write(f"{key}: command not found\n")
            

if __name__ == "__main__":
    main() 
