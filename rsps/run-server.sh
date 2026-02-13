#!/bin/bash
# CloutScape Server Runner
# Starts the RSPS server with proper configuration

set -e

echo "=========================================="
echo "CloutScape RSPS Server"
echo "=========================================="

# Configuration
RELEASES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/releases" && pwd)"
SERVER_JAR="$RELEASES_DIR/server.jar"
LIB_DIR="$RELEASES_DIR/lib"
DATA_DIR="$RELEASES_DIR/data"

# Java options
JAVA_OPTS="-Xmx1G -Xms512M"

# Check if server JAR exists
if [ ! -f "$SERVER_JAR" ]; then
    echo "ERROR: Server JAR not found at $SERVER_JAR"
    echo "Please run build-server.sh first!"
    exit 1
fi

# Build classpath
CLASSPATH="$SERVER_JAR"
if [ -d "$LIB_DIR" ]; then
    for jar in "$LIB_DIR"/*.jar; do
        if [ -f "$jar" ]; then
            CLASSPATH="$CLASSPATH:$jar"
        fi
    done
fi
if [ -d "$LIB_DIR/netty" ]; then
    for jar in "$LIB_DIR/netty"/*.jar; do
        if [ -f "$jar" ]; then
            CLASSPATH="$CLASSPATH:$jar"
        fi
    done
fi

# Change to releases directory
cd "$RELEASES_DIR"

echo "Server JAR: $SERVER_JAR"
echo "Classpath: $CLASSPATH"
echo "Java Options: $JAVA_OPTS"
echo ""
echo "Starting server..."
echo "=========================================="
echo ""

# Run server
java $JAVA_OPTS -cp "$CLASSPATH" com.elvarg.Elvarg

# If server crashes, show error
if [ $? -ne 0 ]; then
    echo ""
    echo "=========================================="
    echo "❌ Server crashed or stopped unexpectedly!"
    echo "=========================================="
    exit 1
fi
