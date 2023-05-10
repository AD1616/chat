# Check if port number argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: ./script.sh <port>"
    exit 1
fi

# Assign the port number from the argument
port=$1

# Find the process IDs (PIDs) associated with the specified port
pids=$(lsof -t -i:$port)

# Check if any PIDs are found
if [ -z "$pids" ]; then
    echo "No processes found running on port $port."
    exit 0
fi

# Terminate the processes using the found PIDs
echo "Attempting to terminate processes running on port $port..."
echo "$pids" | xargs -r kill
