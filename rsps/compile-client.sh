#!/bin/bash
# CloutScape Client Compilation Script
# Compiles the 317 RSPS client into a distributable JAR file

set -e

echo "=========================================="
echo "CloutScape Client Compilation"
echo "=========================================="

# Configuration
CLIENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/client" && pwd)"
OUTPUT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/releases" && pwd)"
BUILD_DIR="$CLIENT_DIR/build"
MANIFEST_FILE="$BUILD_DIR/MANIFEST.MF"
CLIENT_JAR="$OUTPUT_DIR/client.jar"

# Server configuration (will be embedded in client)
SERVER_HOST="${CLOUDFLARE_DOMAIN:-play.cloutscape.com}"
SERVER_PORT="${RSPS_PORT:-43594}"

echo "Client Directory: $CLIENT_DIR"
echo "Output Directory: $OUTPUT_DIR"
echo "Server Host: $SERVER_HOST"
echo "Server Port: $SERVER_PORT"
echo ""

# Check for Java
if ! command -v javac &> /dev/null; then
    echo "ERROR: Java compiler (javac) not found!"
    echo "Please install Java 11 or higher."
    exit 1
fi

# Create build directory
echo "[1/6] Creating build directory..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

# Find all Java source files
echo "[2/6] Finding Java source files..."
cd "$CLIENT_DIR"
JAVA_FILES=$(find src -name "*.java" 2>/dev/null || echo "")

if [ -z "$JAVA_FILES" ]; then
    echo "ERROR: No Java source files found in $CLIENT_DIR/src"
    exit 1
fi

echo "Found $(echo "$JAVA_FILES" | wc -l) Java source files"

# Compile Java sources
echo "[3/6] Compiling Java sources..."
javac -d "$BUILD_DIR" -source 1.8 -target 1.8 $JAVA_FILES

if [ $? -ne 0 ]; then
    echo "ERROR: Compilation failed!"
    exit 1
fi

# Copy resources (if any)
echo "[4/6] Copying resources..."
if [ -d "$CLIENT_DIR/src/resources" ]; then
    cp -r "$CLIENT_DIR/src/resources"/* "$BUILD_DIR/" 2>/dev/null || true
fi

# Copy data files
if [ -d "$CLIENT_DIR/../data" ]; then
    mkdir -p "$BUILD_DIR/data"
    cp -r "$CLIENT_DIR/../data"/* "$BUILD_DIR/data/" 2>/dev/null || true
fi

# Create manifest
echo "[5/6] Creating JAR manifest..."
cat > "$MANIFEST_FILE" << EOF
Manifest-Version: 1.0
Main-Class: Client
Server-Host: $SERVER_HOST
Server-Port: $SERVER_PORT
Created-By: CloutScape Build System
Build-Date: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
EOF

# Create JAR file
echo "[6/6] Creating JAR file..."
cd "$BUILD_DIR"
jar cfm "$CLIENT_JAR" "$MANIFEST_FILE" .

if [ $? -ne 0 ]; then
    echo "ERROR: JAR creation failed!"
    exit 1
fi

# Cleanup
echo "Cleaning up build directory..."
rm -rf "$BUILD_DIR"

# Success
echo ""
echo "=========================================="
echo "✅ Client compilation successful!"
echo "=========================================="
echo "Output: $CLIENT_JAR"
echo "Size: $(du -h "$CLIENT_JAR" | cut -f1)"
echo ""
echo "To test the client, run:"
echo "  java -jar $CLIENT_JAR"
echo ""
