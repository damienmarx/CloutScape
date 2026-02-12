#!/bin/bash
# Cloudflare Tunnel Setup Script
# Sets up Cloudflare tunnel for CloutScape RSPS

set -e

echo "=========================================="
echo "CloutScape Cloudflare Tunnel Setup"
echo "=========================================="
echo ""

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo "Installing Cloudflare Tunnel (cloudflared)..."
    
    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        echo "Detected Linux system"
        
        # Download and install
        wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
        sudo dpkg -i cloudflared-linux-amd64.deb
        rm cloudflared-linux-amd64.deb
        
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "Detected macOS system"
        
        if command -v brew &> /dev/null; then
            brew install cloudflared
        else
            echo "ERROR: Homebrew not found! Please install Homebrew first."
            echo "Visit: https://brew.sh"
            exit 1
        fi
        
    else
        echo "ERROR: Unsupported operating system: $OSTYPE"
        echo "Please install cloudflared manually from:"
        echo "https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation"
        exit 1
    fi
    
    echo "✅ Cloudflared installed successfully!"
else
    echo "✅ Cloudflared is already installed"
fi

echo ""
echo "=========================================="
echo "Cloudflare Tunnel Configuration"
echo "=========================================="
echo ""
echo "To complete the setup, you need to:"
echo ""
echo "1. Login to Cloudflare:"
echo "   cloudflared tunnel login"
echo ""
echo "2. Create a tunnel:"
echo "   cloudflared tunnel create cloutscape"
echo ""
echo "3. Configure the tunnel:"
echo "   Edit the config file at: ~/.cloudflared/config.yml"
echo ""
echo "4. Route your domain:"
echo "   cloudflared tunnel route dns cloutscape play.yourdomain.com"
echo ""
echo "5. Start the tunnel:"
echo "   cloudflared tunnel run cloutscape"
echo ""
echo "=========================================="
echo "Quick Setup (Automatic)"
echo "=========================================="
echo ""

read -p "Do you want to run automatic setup now? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting automatic setup..."
    echo ""
    
    # Login
    echo "Step 1: Login to Cloudflare"
    echo "A browser window will open. Please login to your Cloudflare account."
    cloudflared tunnel login
    
    if [ $? -ne 0 ]; then
        echo "ERROR: Login failed!"
        exit 1
    fi
    
    echo "✅ Login successful!"
    echo ""
    
    # Create tunnel
    echo "Step 2: Creating tunnel 'cloutscape'..."
    cloudflared tunnel create cloutscape || echo "Tunnel may already exist"
    echo ""
    
    # Get tunnel ID
    TUNNEL_ID=$(cloudflared tunnel list | grep cloutscape | awk '{print $1}')
    
    if [ -z "$TUNNEL_ID" ]; then
        echo "ERROR: Could not find tunnel ID!"
        exit 1
    fi
    
    echo "Tunnel ID: $TUNNEL_ID"
    echo ""
    
    # Create config file
    echo "Step 3: Creating configuration file..."
    
    CONFIG_DIR="$HOME/.cloudflared"
    CONFIG_FILE="$CONFIG_DIR/config.yml"
    
    mkdir -p "$CONFIG_DIR"
    
    cat > "$CONFIG_FILE" << EOF
tunnel: $TUNNEL_ID
credentials-file: $CONFIG_DIR/$TUNNEL_ID.json

ingress:
  # RSPS Server
  - hostname: play.yourdomain.com
    service: tcp://localhost:43594
  
  # Web Dashboard
  - hostname: dashboard.yourdomain.com
    service: http://localhost:5000
  
  # Catch-all rule
  - service: http_status:404
EOF
    
    echo "✅ Configuration file created at: $CONFIG_FILE"
    echo ""
    echo "⚠️  IMPORTANT: Edit the config file and replace 'yourdomain.com' with your actual domain!"
    echo ""
    
    # Ask for domain
    read -p "Enter your domain (e.g., cloutscape.com): " DOMAIN
    
    if [ ! -z "$DOMAIN" ]; then
        sed -i "s/yourdomain.com/$DOMAIN/g" "$CONFIG_FILE"
        echo "✅ Domain updated in config file"
        echo ""
        
        # Route DNS
        echo "Step 4: Routing DNS..."
        cloudflared tunnel route dns cloutscape "play.$DOMAIN" || echo "Route may already exist"
        cloudflared tunnel route dns cloutscape "dashboard.$DOMAIN" || echo "Route may already exist"
        echo ""
    fi
    
    echo "=========================================="
    echo "✅ Setup Complete!"
    echo "=========================================="
    echo ""
    echo "To start the tunnel, run:"
    echo "  cloudflared tunnel run cloutscape"
    echo ""
    echo "Or install as a service:"
    echo "  sudo cloudflared service install"
    echo "  sudo systemctl start cloudflared"
    echo ""
    echo "Your RSPS will be accessible at:"
    echo "  play.$DOMAIN:43594"
    echo ""
    echo "Your dashboard will be accessible at:"
    echo "  https://dashboard.$DOMAIN"
    echo ""
else
    echo "Skipping automatic setup."
    echo "Please follow the manual steps above."
fi

echo ""
echo "For more information, visit:"
echo "https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/"
echo ""
