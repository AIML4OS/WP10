#!/bin/bash
echo "Executing the download_data.sh script"

# === Description ===
# This script downloads a data file from an S3 bucket using `mc` (MinIO client)
# and stores it in the ~/work/data directory.

# === Config destination folder ===
DEST_DIR="$HOME/work/data"
# Ensure destination folder exists
mkdir -p "$DEST_DIR"

# === Download a first file ===
DATA_PATH="s3/donnees-insee/diffusion/ETAT_CIVIL/2020/DECES_COM_1019.csv"
echo "Downloading $DATA_PATH to $DEST_FILE..."
mc cp "$DATA_PATH" "$DEST_DIR"

# === Check success ===
if [ $? -eq 0 ]; then
  echo "✅ File downloaded successfully to $DEST_FILE"
else
  echo "❌ Failed to download file from $DATA_PATH"
  exit 1
fi

# === Download a second file ===
# Repeat the code above for each file

