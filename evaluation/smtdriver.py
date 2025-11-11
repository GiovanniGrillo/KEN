import os

def run_python_script_in_dir(script_path, dir_path):
    # Save the current working directory
    original_cwd = os.getcwd()

    try:
        # Change to the target directory
        os.chdir(dir_path)

        # Run the Python script
        os.system(f'python3 {script_path} ')

    finally:
        # Change back to the original directory
        os.chdir(original_cwd)

def run_verifier_for_better_bpftrace_proram(context_desc: str, program: str) -> str:
    print("\n\n[run_verifier_for_better_bpftrace_proram]: enter\n")
    with open('../ken/context.txt', 'w') as f:
        f.write(context_desc)
    with open('../ken/program.bt', 'w') as f:
        f.write(program)
    # Run the verifier for the better bpftrace program
    try:
        run_python_script_in_dir('verifier.py', '../ken')
    except:
        print("Verifier failed, using original program")
        return program
    
    res = ''
    with open('../ken/result.bt', 'r') as f:
        res = f.read()
    # Return the path to the output file
    print("\n\n[run_verifier_for_better_bpftrace_proram]: exit\n")
    return res

if __name__ == "__main__":
    try:
        run_python_script_in_dir('verifier.py', '../ken')
    except:
        print("Verifier failed")
