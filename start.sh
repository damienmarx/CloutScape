#!/bin/bash

################################################################################
# CloutScape AIO - Discord Setup Bot - Quick Start Script
# Starts both the Discord bot and Flask web app
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  CloutScape AIO - Discord Setup Bot                        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}\n"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ Error: .env file not found!${NC}"
    echo -e "${YELLOW}Please copy .env.example to .env and configure it:${NC}"
    echo -e "  cp .env.example .env"
    echo -e "  nano .env"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python 3 is not installed!${NC}"
    exit 1
fi

# Check if requirements are installed
echo -e "${BLUE}→ Checking dependencies...${NC}"
if ! python3 -c "import discord, flask" 2>/dev/null; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip3 install -r requirements.txt
fi

echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Create logs directory
mkdir -p logs

# Load environment variables
export $(cat .env | grep -v '#' | xargs)

# Check if Discord token is set
if [ -z "$DISCORD_TOKEN" ]; then
    echo -e "${RED}❌ Error: DISCORD_TOKEN not set in .env${NC}"
    exit 1
fi

if [ -z "$ADMIN_ID" ]; then
    echo -e "${RED}❌ Error: ADMIN_ID not set in .env${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Configuration loaded${NC}\n"

# Function to handle cleanup
cleanup() {
    echo -e "\n${YELLOW}Shutting down...${NC}"
    kill $BOT_PID $APP_PID 2>/dev/null || true
    echo -e "${GREEN}✓ Shutdown complete${NC}"
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

# Start the bot
echo -e "${BLUE}→ Starting Discord bot...${NC}"
python3 bot.py > logs/bot.log 2>&1 &
BOT_PID=$!
echo -e "${GREEN}✓ Bot started (PID: $BOT_PID)${NC}"

# Wait a moment for bot to initialize
sleep 2

# Start the web app
echo -e "${BLUE}→ Starting Flask web app...${NC}"
python3 app.py > logs/app.log 2>&1 &
APP_PID=$!
echo -e "${GREEN}✓ Web app started (PID: $APP_PID)${NC}\n"

# Display access information
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  CloutScape AIO is now running!                            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}\n"

echo -e "${BLUE}📊 Access Points:${NC}"
echo -e "  • Web Dashboard: ${BLUE}http://localhost:5000${NC}"
echo -e "  • Setup Guide: ${BLUE}http://localhost:5000/setup${NC}"
echo -e "  • Admin Panel: ${BLUE}http://localhost:5000/admin${NC}"
echo -e "  • API Status: ${BLUE}http://localhost:5000/api/status${NC}\n"

echo -e "${BLUE}📝 Logs:${NC}"
echo -e "  • Bot: ${BLUE}logs/bot.log${NC}"
echo -e "  • Web: ${BLUE}logs/app.log${NC}\n"

echo -e "${BLUE}🎮 Discord Commands:${NC}"
echo -e "  • ${BLUE}!setup${NC} - Setup the server"
echo -e "  • ${BLUE}!status${NC} - Check setup status"
echo -e "  • ${BLUE}!help${NC} - Show help\n"

echo -e "${YELLOW}Press Ctrl+C to stop${NC}\n"

# Wait for processes
wait $BOT_PID $APP_PID
