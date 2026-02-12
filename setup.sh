#!/bin/bash
# CloutScape Master Setup Script
# Automated installation and configuration for CloutScape RSPS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${PURPLE}"
cat << "EOF"
   _____ _             _   _____                      
  / ____| |           | | / ____|                     
 | |    | | ___  _   _| || (___   ___ __ _ _ __   ___ 
 | |    | |/ _ \| | | | | \___ \ / __/ _` | '_ \ / _ \
 | |____| | (_) | |_| | | ____) | (_| (_| | |_) |  __/
  \_____|_|\___/ \__,_|_||_____/ \___\__,_| .__/ \___|
                                          | |         
                                          |_|         
EOF
echo -e "${NC}"
echo -e "${CYAN}=========================================="
echo -e "CloutScape RSPS - Automated Setup"
echo -e "==========================================${NC}"
echo ""

# Get installation directory
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo -e "${BLUE}Installation Directory: $INSTALL_DIR${NC}"
echo ""

# Function to print step
print_step() {
    echo -e "${GREEN}[STEP $1/$2]${NC} $3"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Function to print info
print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_warning "Please do not run this script as root!"
    print_info "Run as a regular user. The script will use sudo when needed."
    exit 1
fi

# Total steps
TOTAL_STEPS=10

# Step 1: Check system requirements
print_step 1 $TOTAL_STEPS "Checking system requirements..."
echo ""

# Check OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    print_success "Operating System: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    print_success "Operating System: macOS"
else
    print_error "Unsupported operating system: $OSTYPE"
    exit 1
fi

# Check for required commands
REQUIRED_COMMANDS=("wget" "curl" "git")
for cmd in "${REQUIRED_COMMANDS[@]}"; do
    if command -v $cmd &> /dev/null; then
        print_success "$cmd is installed"
    else
        print_error "$cmd is not installed!"
        exit 1
    fi
done

echo ""

# Step 2: Install Java
print_step 2 $TOTAL_STEPS "Installing Java 11..."
echo ""

if command -v java &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2)
    print_success "Java is already installed: $JAVA_VERSION"
else
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_info "Installing OpenJDK 11..."
        sudo apt-get update -qq
        sudo apt-get install -y openjdk-11-jdk openjdk-11-jre
        print_success "Java 11 installed"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            print_info "Installing Java via Homebrew..."
            brew install openjdk@11
            print_success "Java 11 installed"
        else
            print_error "Homebrew not found! Please install Java 11 manually."
            exit 1
        fi
    fi
fi

echo ""

# Step 3: Install Python and dependencies
print_step 3 $TOTAL_STEPS "Installing Python and dependencies..."
echo ""

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python is installed: $PYTHON_VERSION"
else
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_info "Installing Python 3..."
        sudo apt-get install -y python3 python3-pip
        print_success "Python 3 installed"
    else
        print_error "Python 3 not found! Please install Python 3.8+ manually."
        exit 1
    fi
fi

# Install Python dependencies
if [ -f "$INSTALL_DIR/requirements.txt" ]; then
    print_info "Installing Python dependencies..."
    pip3 install -r "$INSTALL_DIR/requirements.txt" --user -q
    print_success "Python dependencies installed"
fi

echo ""

# Step 4: Configure environment
print_step 4 $TOTAL_STEPS "Configuring environment..."
echo ""

ENV_FILE="$INSTALL_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
    print_info "Creating .env file..."
    
    # Prompt for Discord token
    echo -e "${YELLOW}Enter your Discord Bot Token:${NC}"
    read -r DISCORD_TOKEN
    
    # Prompt for Admin ID
    echo -e "${YELLOW}Enter your Discord Admin ID:${NC}"
    read -r ADMIN_ID
    
    # Prompt for domain (optional)
    echo -e "${YELLOW}Enter your Cloudflare domain (e.g., cloutscape.com) or press Enter to skip:${NC}"
    read -r DOMAIN
    
    if [ -z "$DOMAIN" ]; then
        DOMAIN="play.cloutscape.com"
    fi
    
    # Create .env file
    cat > "$ENV_FILE" << EOF
# CloutScape Configuration
DISCORD_TOKEN=$DISCORD_TOKEN
ADMIN_ID=$ADMIN_ID

# RSPS Configuration
RSPS_HOST=localhost
RSPS_PORT=43594
CLOUDFLARE_DOMAIN=$DOMAIN

# Web Dashboard
FLASK_PORT=5000
FLASK_ENV=production
SECRET_KEY=$(openssl rand -hex 32)

# Client Download URL (will be updated after build)
CLIENT_DOWNLOAD_URL=https://github.com/No6love9/CloutScape/releases/latest/download/client.jar
EOF
    
    print_success ".env file created"
else
    print_success ".env file already exists"
fi

# Load environment variables
set -a
source "$ENV_FILE"
set +a

echo ""

# Step 5: Build RSPS server
print_step 5 $TOTAL_STEPS "Building RSPS server..."
echo ""

if [ -f "$INSTALL_DIR/rsps/build-server.sh" ]; then
    cd "$INSTALL_DIR/rsps"
    ./build-server.sh
    print_success "Server built successfully"
else
    print_warning "Server build script not found, skipping..."
fi

echo ""

# Step 6: Compile client
print_step 6 $TOTAL_STEPS "Compiling client..."
echo ""

if [ -f "$INSTALL_DIR/rsps/compile-client.sh" ]; then
    cd "$INSTALL_DIR/rsps"
    export CLOUDFLARE_DOMAIN
    ./compile-client.sh || print_warning "Client compilation failed (this is normal if source is incomplete)"
else
    print_warning "Client compilation script not found, skipping..."
fi

echo ""

# Step 7: Setup Cloudflare tunnel
print_step 7 $TOTAL_STEPS "Setting up Cloudflare tunnel..."
echo ""

echo -e "${YELLOW}Do you want to setup Cloudflare tunnel now? (y/n):${NC}"
read -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "$INSTALL_DIR/cloudflare/setup-tunnel.sh" ]; then
        cd "$INSTALL_DIR/cloudflare"
        ./setup-tunnel.sh
    else
        print_warning "Cloudflare setup script not found"
    fi
else
    print_info "Skipping Cloudflare tunnel setup"
    print_info "You can run it later: ./cloudflare/setup-tunnel.sh"
fi

echo ""

# Step 8: Install systemd services (Linux only)
print_step 8 $TOTAL_STEPS "Installing systemd services..."
echo ""

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${YELLOW}Do you want to install systemd services? (y/n):${NC}"
    read -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Installing systemd services..."
        
        # Replace placeholders in service files
        for service_file in "$INSTALL_DIR/systemd"/*.service; do
            if [ -f "$service_file" ]; then
                SERVICE_NAME=$(basename "$service_file")
                TEMP_FILE="/tmp/$SERVICE_NAME"
                
                # Replace placeholders
                sed "s|%USER%|$USER|g" "$service_file" | \
                sed "s|%INSTALL_DIR%|$INSTALL_DIR|g" | \
                sed "s|%DISCORD_TOKEN%|$DISCORD_TOKEN|g" | \
                sed "s|%ADMIN_ID%|$ADMIN_ID|g" | \
                sed "s|%CLOUDFLARE_DOMAIN%|$CLOUDFLARE_DOMAIN|g" > "$TEMP_FILE"
                
                # Copy to systemd directory
                sudo cp "$TEMP_FILE" "/etc/systemd/system/$SERVICE_NAME"
                rm "$TEMP_FILE"
                
                print_success "Installed $SERVICE_NAME"
            fi
        done
        
        # Reload systemd
        sudo systemctl daemon-reload
        print_success "Systemd services installed"
        
        print_info "To start services, run:"
        print_info "  sudo systemctl start cloutscape-server"
        print_info "  sudo systemctl start cloutscape-bot"
        print_info "  sudo systemctl start cloutscape-web"
        
    else
        print_info "Skipping systemd service installation"
    fi
else
    print_info "Systemd services are only available on Linux"
fi

echo ""

# Step 9: Create starter scripts
print_step 9 $TOTAL_STEPS "Creating starter scripts..."
echo ""

# Create start-all script
cat > "$INSTALL_DIR/start-all.sh" << 'EOF'
#!/bin/bash
# Start all CloutScape services

INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Starting CloutScape services..."

# Load environment
set -a
source "$INSTALL_DIR/.env"
set +a

# Start server in background
echo "Starting RSPS server..."
cd "$INSTALL_DIR/rsps"
./run-server.sh &
SERVER_PID=$!

# Wait a bit for server to start
sleep 5

# Start Discord bot in background
echo "Starting Discord bot..."
cd "$INSTALL_DIR"
python3 bot_enhanced_v2.py &
BOT_PID=$!

# Start web dashboard in background
echo "Starting web dashboard..."
python3 app_enhanced.py &
WEB_PID=$!

echo ""
echo "All services started!"
echo "Server PID: $SERVER_PID"
echo "Bot PID: $BOT_PID"
echo "Web PID: $WEB_PID"
echo ""
echo "To stop all services, run: ./stop-all.sh"
echo ""
EOF

# Create stop-all script
cat > "$INSTALL_DIR/stop-all.sh" << 'EOF'
#!/bin/bash
# Stop all CloutScape services

echo "Stopping CloutScape services..."

# Kill Python processes
pkill -f "bot_enhanced_v2.py"
pkill -f "app_enhanced.py"

# Kill Java processes
pkill -f "server.jar"

echo "All services stopped!"
EOF

chmod +x "$INSTALL_DIR/start-all.sh"
chmod +x "$INSTALL_DIR/stop-all.sh"

print_success "Starter scripts created"

echo ""

# Step 10: Final summary
print_step 10 $TOTAL_STEPS "Setup complete!"
echo ""

echo -e "${GREEN}=========================================="
echo -e "✅ CloutScape Setup Complete!"
echo -e "==========================================${NC}"
echo ""
echo -e "${CYAN}📁 Installation Directory:${NC} $INSTALL_DIR"
echo ""
echo -e "${CYAN}🚀 Quick Start:${NC}"
echo ""
echo -e "  ${YELLOW}1. Start all services:${NC}"
echo -e "     ./start-all.sh"
echo ""
echo -e "  ${YELLOW}2. Stop all services:${NC}"
echo -e "     ./stop-all.sh"
echo ""
echo -e "  ${YELLOW}3. Start individual services:${NC}"
echo -e "     ./rsps/run-server.sh          # Start RSPS server"
echo -e "     python3 bot_enhanced_v2.py    # Start Discord bot"
echo -e "     python3 app_enhanced.py       # Start web dashboard"
echo ""
echo -e "${CYAN}🌐 Access Points:${NC}"
echo ""
echo -e "  ${YELLOW}RSPS Server:${NC} $CLOUDFLARE_DOMAIN:43594"
echo -e "  ${YELLOW}Web Dashboard:${NC} http://localhost:5000"
echo -e "  ${YELLOW}Discord Bot:${NC} Invite to your server and run !setup"
echo ""
echo -e "${CYAN}📥 Client Download:${NC}"
echo ""
echo -e "  ${YELLOW}Location:${NC} $INSTALL_DIR/rsps/releases/client.jar"
echo -e "  ${YELLOW}Upload to:${NC} GitHub Releases for easy distribution"
echo ""
echo -e "${CYAN}📚 Documentation:${NC}"
echo ""
echo -e "  ${YELLOW}README:${NC} $INSTALL_DIR/README.md"
echo -e "  ${YELLOW}Architecture:${NC} $INSTALL_DIR/ARCHITECTURE.md"
echo -e "  ${YELLOW}Features:${NC} $INSTALL_DIR/FEATURES.md"
echo ""
echo -e "${CYAN}💡 Next Steps:${NC}"
echo ""
echo -e "  1. Start the services with ./start-all.sh"
echo -e "  2. Invite the Discord bot to your server"
echo -e "  3. Run !setup in your Discord server"
echo -e "  4. Upload client.jar to GitHub releases"
echo -e "  5. Players can register with !register username"
echo ""
echo -e "${GREEN}=========================================="
echo -e "Enjoy CloutScape! 🎮"
echo -e "==========================================${NC}"
echo ""
