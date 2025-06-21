#!/bin/bash

# Check for required argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <output_directory>"
    exit 1
fi

OUTPUT_DIR="$1"
MODEL_FILE="jobshop5.mzn"
INSTANCE_DIR="instances"
MZN_TIMEOUT="1200000"  # 20 minutes in seconds

# Ensure model file exists
if [ ! -f "$MODEL_FILE" ]; then
    echo "Error: $MODEL_FILE not found in current directory."
    exit 1
fi

# Ensure instance directory exists
if [ ! -d "$INSTANCE_DIR" ]; then
    echo "Error: $INSTANCE_DIR directory not found."
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Run each instance
for DZN_FILE in "$INSTANCE_DIR"/*.dzn; do
    BASENAME=$(basename "$DZN_FILE" .dzn)
    OUTPUT_FILE="$OUTPUT_DIR/${BASENAME}.out"

    echo "Running $DZN_FILE..."

    minizinc -a -s -f --output-time -t "$MZN_TIMEOUT" -o "$OUTPUT_FILE" --solver Pumpkin "$MODEL_FILE" "$DZN_FILE" 

    echo "Finished $DZN_FILE"
done

echo "All instances processed. Outputs saved to $OUTPUT_DIR"

