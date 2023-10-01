import subprocess
import os
# Script written by CHATGPT
# Define the directory where pytest scripts are located
tests_directory = "./tests"

# Get a list of all .py files in the tests directory
pytest_scripts = [
    os.path.join(root, filename)
    for root, _, files in os.walk(tests_directory)
    for filename in files
    if filename.startswith("test_") and filename.endswith(".py")
]

# Initialize the result variable with a return code of 0
result = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
failed_tests = []

# Iterate through the pytest scripts and run them one by one
for script in pytest_scripts:
    print(f"Running pytest script: {script}")

    # Run the pytest script using subprocess
    current_result = subprocess.run(["pytest", script])

    # Check the return code to determine success or failure
    if current_result.returncode == 0:
        print(f"Test script {script} PASSED")
    else:
        print(f"Test script {script} FAILED")
        failed_tests.append(script)

    # Update the overall result based on the current result
    result.returncode += current_result.returncode

# Summarize the test results
total_tests = len(pytest_scripts)
num_failed_tests = len(failed_tests)

print(f"Total tests: {total_tests}")
print(f"Failed tests: {num_failed_tests}")

if num_failed_tests > 0:
    print("Failed test scripts:")
    for failed_test in failed_tests:
        print(f"  {failed_test}")

# Exit with an appropriate return code
exit(result.returncode)
