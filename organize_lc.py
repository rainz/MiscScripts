#!/bin/bash

# Loop through all files matching the pattern "lc*.py"
for file in lc*.py; do
  # Check if the file actually exists to avoid issues if no files match
  if [ -e "$file" ]; then
    # Extract the first 5 characters from the file's name
    dir_name="${file:0:5}00"

    # Create the new directory. The -p flag prevents an error if the directory already exists.
    echo "Making dir for $dir_name if it does not exist"
    mkdir -p "$dir_name"

    # Move the file into the new directory using git mv
    echo "Moving $file to $dir_name/"
    git mv "$file" "$dir_name/"
  fi
done

echo "Operation complete."
