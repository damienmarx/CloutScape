#!/bin/bash
# CloutScape Server Build Script
# Compiles the 317 RSPS server

set -e

echo "=========================================="
echo "CloutScape Server Build"
echo "=========================================="

# Configuration
SERVER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/server" && pwd)"
OUTPUT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/releases" && pwd)"
BUILD_DIR="$SERVER_DIR/build"
LIB_DIR="$SERVER_DIR/lib"
SERVER_JAR="$OUTPUT_DIR/server.jar"

echo "Server Directory: $SERVER_DIR"
echo "Output Directory: $OUTPUT_DIR"
echo ""

# Check for Java
if ! command -v javac -encoding UTF-8 -encoding UTF-8 &> /dev/null; then
    echo "ERROR: Java compiler (javac) not found!"
    echo "Please install Java 11 or higher."
    exit 1
fi

# Create build directory
echo "[1/5] Creating build directory..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$OUTPUT_DIR"

# Find all Java source files
echo "[2/5] Finding Java source files..."
cd "$SERVER_DIR"
JAVA_FILES=$(find src -name "*.java" 2>/dev/null || echo "")

if [ -z "$JAVA_FILES" ]; then
    echo "ERROR: No Java source files found in $SERVER_DIR/src"
    exit 1
fi

echo "Found $(echo "$JAVA_FILES" | wc -l) Java source files"

# Build classpath from lib directory
CLASSPATH="$SERVER_DIR:$SERVER_DIR/lib/*:$SERVER_DIR/lib/netty/*"
if [ -d "$LIB_DIR" ]; then
    for jar in "$LIB_DIR"/*.jar; do
        if [ -f "$jar" ]; then
            CLASSPATH="$SERVER_DIR:$SERVER_DIR/lib/*:$SERVER_DIR/lib/netty/*"
        fi
    done
fi

# Compile Java sources
cp -r "$SERVER_DIR/lib" "$BUILD_DIR/"
cp -r "$SERVER_DIR/lib" "$BUILD_DIR/"
echo "[3/5] Compiling Java sources..."
javac -encoding UTF-8 -encoding UTF-8 -d "$BUILD_DIR" -cp "$CLASSPATH" -source 1.8 -target 1.8 $JAVA_FILES

if [ $? -ne 0 ]; then
    echo "ERROR: Compilation failed!"
    exit 1
fi

# Copy data directory
echo "[4/5] Copying server data..."
if [ -d "$SERVER_DIR/data" ]; then
    cp -r "$SERVER_DIR/data" "$BUILD_DIR/" 2>/dev/null || true
fi

# Create manifest
MANIFEST_FILE="$BUILD_DIR/MANIFEST.MF"
cat > "$MANIFEST_FILE" << EOF
Manifest-Version: 1.0
Main-Class: com.elvarg.Server
Created-By: CloutScape Build System
Build-Date: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
EOF

# Create JAR file
echo "[5/5] Creating server JAR..."
cd "$BUILD_DIR"
jar cfm "$SERVER_JAR" "$MANIFEST_FILE" .

if [ $? -ne 0 ]; then
    echo "ERROR: JAR creation failed!"
    exit 1
fi

# Copy dependencies
if [ -d "$LIB_DIR" ]; then
    echo "Copying library dependencies..."
    mkdir -p "$OUTPUT_DIR/lib"
    cp "$LIB_DIR"/*.jar "$OUTPUT_DIR/lib/" 2>/dev/null || true
    if [ -d "$LIB_DIR/netty" ]; then
        mkdir -p "$OUTPUT_DIR/lib/netty"
        cp "$LIB_DIR/netty"/*.jar "$OUTPUT_DIR/lib/netty/" 2>/dev/null || true
    fi
fi

# Copy data
if [ -d "$SERVER_DIR/data" ]; then
    echo "Copying server data..."
    cp -r "$SERVER_DIR/data" "$OUTPUT_DIR/" 2>/dev/null || true
fi

# Cleanup
echo "Cleaning up build directory..."
rm -rf "$BUILD_DIR"

# Success
echo ""
echo "=========================================="
echo "✅ Server build successful!"
echo "=========================================="
echo "Output: $SERVER_JAR"
echo "Size: $(du -h "$SERVER_JAR" | cut -f1)"
echo ""
echo "To run the server:"
echo "  cd $OUTPUT_DIR"
echo "  java -jar server.jar"
echo ""
