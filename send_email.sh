#!/bin/bash

declare -A VENV_LIST
VENV_LIST=(
    ["env1"]="/Users/ishitkaroli/Desktop/Test/.venv"
    ["env2"]="/path/to/venv2"
    ["env3"]="/path/to/venv3"
)

# Display the list of available environments
echo "Available Python Virtual Environments:"
PS3="Please select the environment to activate: "
select env in "${!VENV_LIST[@]}"; do
    if [ -n "$env" ]; then
        echo "You selected $env"
        VENV_PATH="${VENV_LIST[$env]}/bin/activate"
        break
    else
        echo "Invalid selection. Please try again."
    fi
done

# Step 2: Activate the selected environment
if [ -f "$VENV_PATH" ]; then
    echo "Activating virtual environment: $env"
    source "$VENV_PATH"
else
    echo "Error: Virtual environment $env not found!"
    exit 1
fi

# Step 3: Check dependencies from requirements.txt (assuming it's in the current directory)
if [ -f "requirements.txt" ]; then
    echo "Checking dependencies in requirements.txt..."
    pip install -r requirements.txt
else
    echo "No requirements.txt found. Skipping dependency installation."
fi

# Step 4: Ask user if they want to run the Python script
read -p "All set! Do you want to run the Python script? (yes/no): " confirm
if [ "$confirm" == "yes" ]; then
# Replace this with your actual Python script
    python3 /Users/ishitkaroli/Desktop/Test/send_email.py
else
    echo "Exiting without running the script."
fi