#!/bin/bash

# Base directory
BASE_DIR="./"
SCRIPT_DIR="${BASE_DIR}/00.scripts"

# Functions
run_python_task() {
    local task_name="$1"
    local script_path="$2"
    local task_file="$3"

    echo "Starting task: $task_name"

    # Start and monitor the Python task
    python3 "$script_path" &
    local task_pid=$!

    # Wait until the task file is deleted
    while [ -f "$task_file" ]; do
        sleep 1
    done

    # Ensure the process is terminated
    wait "$task_pid" 2>/dev/null
    echo "Task $task_name completed."
}

run_shell_task() {
    local task_name="$1"
    local script_path="$2"
    local task_file="$3"

    echo "Starting task: $task_name"

    # Start and monitor the shell task
    bash "$script_path" &
    local task_pid=$!

    # Wait until the task file is deleted
    while [ -f "$task_file" ]; do
        sleep 1
    done

    # Ensure the process is terminated
    wait "$task_pid" 2>/dev/null
    echo "Task $task_name completed."
}

# Main execution
echo "Starting master script"

# Task 1: Frame Export
run_python_task "Frame Export" "${SCRIPT_DIR}/frame_export.py" "${SCRIPT_DIR}/task_running_Cap01"

# Task 2: Transfer (CAP -> FACE)
run_shell_task "Transfer to Face Recognition" "${SCRIPT_DIR}/transfer-cap-face.sh" "${SCRIPT_DIR}/task_running_TransferCapToFace"

# Task 3: Face Recognition
run_python_task "Face Recognition" "${SCRIPT_DIR}/face_recognition.py" "${SCRIPT_DIR}/task_running_Face01"

# Task 4: Transfer (FACE -> QUALI)
run_shell_task "Transfer to Quality Check" "${SCRIPT_DIR}/transfer-face-quali.sh" "${SCRIPT_DIR}/task_running_TransferFaceToQuali"

# Task 5: Quality Control
run_python_task "Quality Check" "${SCRIPT_DIR}/quality_check.py" "${SCRIPT_DIR}/task_running_QualityCheck"

# Task 6: Transfer (QUALI -> output)
run_shell_task "Transfer to Output and Cleanup" "${SCRIPT_DIR}/transfer-output.sh" "${SCRIPT_DIR}/task_running_TransferQualiToOutput"

echo "All tasks completed. Master script finished."
