# 🚀 CloutScape Deployment Guide

This comprehensive guide will walk you through deploying CloutScape on your desktop or VPS server.

---

## 📋 Prerequisites

Before you begin, ensure you have the following:

### Required

- **Discord Bot**: Created at [Discord Developer Portal](https://discord.com/developers/applications)
- **Discord Admin ID**: Your Discord user ID (enable Developer Mode in Discord settings)
- **Operating System**: Linux (Ubuntu 22.04+), macOS, or Windows with WSL2
- **Internet Connection**: For downloading dependencies and connecting to Cloudflare

### Optional but Recommended

- **Cloudflare Account**: Free account for tunnel setup
- **Custom Domain**: For professional branding (e.g., play.cloutscape.com)
- **VPS Server**: For 24/7 uptime (DigitalOcean, Linode, AWS, etc.)

---

## 🖥️ Deployment Options

### Option 1: Desktop/Local Deployment (Testing & Development)

This option is perfect for testing the server locally or running it on your personal computer.

**Pros:**
- Free (no hosting costs)
- Easy to test and modify
- Full control over the environment

**Cons:**
- Requires your computer to be running 24/7
- Limited by your home internet connection
- No automatic restarts if server crashes

**Best for:** Testing, development, small private servers

### Option 2: VPS/Cloud Deployment (Production)

This option is recommended for public servers that need 24/7 uptime.

**Pros:**
- 24/7 uptime
- Professional infrastructure
- Better performance and reliability
- Automatic backups (depending on provider)

**Cons:**
- Monthly hosting costs ($5-20/month typically)
- Requires basic Linux knowledge

**Best for:** Public servers, production environments

---

## 🛠️ Desktop/Local Deployment

### Step 1: Clone the Repository

```bash
git clone https://github.com/No6love9/CloutScape.git
cd CloutScape
```

### Step 2: Run Automated Setup

```bash
chmod +x setup.sh
./setup.sh
```

The setup script will prompt you for:
- Discord Bot Token
- Discord Admin ID
- Cloudflare Domain (optional)

### Step 3: Start Services

```bash
./start-all.sh
```

This will start:
- RSPS Server (port 43594)
- Discord Bot
- Web Dashboard (port 5000)

### Step 4: Setup Discord Server

1. Invite bot to your Discord server
2. Run `!setup` command
3. Bot will create all channels and roles

### Step 5: Test the System

1. In Discord, run `!register TestPlayer`
2. Check your DMs for credentials
3. Download client with `!download`
4. Launch client and login

---

## ☁️ VPS/Cloud Deployment

### Recommended VPS Providers

| Provider | Starting Price | Recommended Plan |
|----------|---------------|------------------|
| DigitalOcean | $6/month | Basic Droplet (2GB RAM) |
| Linode | $5/month | Nanode (1GB RAM) |
| Vultr | $6/month | Cloud Compute (2GB RAM) |
| AWS Lightsail | $5/month | 1GB RAM instance |

### Step 1: Create VPS Instance

1. Sign up for a VPS provider
2. Create a new instance with:
   - **OS**: Ubuntu 22.04 LTS
   - **RAM**: 2GB minimum (4GB recommended)
   - **Storage**: 25GB minimum
   - **Location**: Choose closest to your players

### Step 2: Connect to VPS

```bash
ssh root@your-vps-ip-address
```

### Step 3: Create Non-Root User

```bash
# Create user
adduser cloutscape

# Add to sudo group
usermod -aG sudo cloutscape

# Switch to new user
su - cloutscape
```

### Step 4: Install Git

```bash
sudo apt-get update
sudo apt-get install -y git
```

### Step 5: Clone Repository

```bash
cd ~
git clone https://github.com/No6love9/CloutScape.git
cd CloutScape
```

### Step 6: Run Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

When prompted, choose to install systemd services (recommended for VPS).

### Step 7: Enable Services

```bash
# Enable services to start on boot
sudo systemctl enable cloutscape-server
sudo systemctl enable cloutscape-bot
sudo systemctl enable cloutscape-web

# Start services
sudo systemctl start cloutscape-server
sudo systemctl start cloutscape-bot
sudo systemctl start cloutscape-web
```

### Step 8: Configure Firewall

```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow web dashboard
sudo ufw allow 5000/tcp

# Enable firewall
sudo ufw enable
```

**Note:** You don't need to open port 43594 if using Cloudflare tunnel!

### Step 9: Setup Cloudflare Tunnel

```bash
cd ~/CloutScape/cloudflare
./setup-tunnel.sh
```

Follow the prompts to:
1. Login to Cloudflare
2. Create tunnel
3. Configure domain
4. Start tunnel

---

## 🌐 Cloudflare Tunnel Setup (Detailed)

Cloudflare Tunnel eliminates the need for port forwarding and provides DDoS protection.

### Why Use Cloudflare Tunnel?

- **No Port Forwarding**: Works behind NAT/firewalls
- **DDoS Protection**: Cloudflare's network protects your server
- **SSL/TLS**: Automatic HTTPS for web dashboard
- **Custom Domain**: Use your own domain
- **Free**: No cost for basic usage

### Prerequisites

- Cloudflare account (free)
- Domain name (can be purchased through Cloudflare or any registrar)

### Setup Steps

#### 1. Run Setup Script

```bash
cd ~/CloutScape/cloudflare
./setup-tunnel.sh
```

#### 2. Login to Cloudflare

A browser window will open. Login to your Cloudflare account.

#### 3. Create Tunnel

The script will create a tunnel named "cloutscape".

#### 4. Configure Domain

When prompted, enter your domain (e.g., `cloutscape.com`).

The script will automatically configure:
- `play.cloutscape.com` → RSPS Server (port 43594)
- `dashboard.cloutscape.com` → Web Dashboard (port 5000)

#### 5. Update DNS

In your Cloudflare dashboard:
1. Go to DNS settings
2. Verify the CNAME records were created:
   - `play` → tunnel
   - `dashboard` → tunnel

#### 6. Start Tunnel

```bash
# Test tunnel
cloudflared tunnel run cloutscape

# Or install as service
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

#### 7. Update Client Configuration

Edit `.env` file:

```bash
CLOUDFLARE_DOMAIN=play.cloutscape.com
```

Rebuild client:

```bash
cd ~/CloutScape/rsps
./compile-client.sh
```

---

## 📦 Client Distribution via GitHub Releases

### Step 1: Build Client

```bash
cd ~/CloutScape/rsps
./compile-client.sh
```

This creates `rsps/releases/client.jar`.

### Step 2: Create GitHub Release

Using GitHub CLI:

```bash
# Authenticate with GitHub
gh auth login

# Create release
gh release create v1.0.0 \
  rsps/releases/client.jar \
  --title "CloutScape v1.0.0" \
  --notes "Initial release of CloutScape RSPS client"
```

Or manually:
1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Upload `client.jar`
5. Publish release

### Step 3: Update Download URL

Edit `.env`:

```bash
CLIENT_DOWNLOAD_URL=https://github.com/No6love9/CloutScape/releases/latest/download/client.jar
```

Restart bot:

```bash
sudo systemctl restart cloutscape-bot
```

---

## 🔧 Service Management

### Systemd Commands (Linux)

```bash
# Start services
sudo systemctl start cloutscape-server
sudo systemctl start cloutscape-bot
sudo systemctl start cloutscape-web

# Stop services
sudo systemctl stop cloutscape-server
sudo systemctl stop cloutscape-bot
sudo systemctl stop cloutscape-web

# Restart services
sudo systemctl restart cloutscape-server
sudo systemctl restart cloutscape-bot
sudo systemctl restart cloutscape-web

# Check status
sudo systemctl status cloutscape-server
sudo systemctl status cloutscape-bot
sudo systemctl status cloutscape-web

# View logs
sudo journalctl -u cloutscape-server -f
sudo journalctl -u cloutscape-bot -f
sudo journalctl -u cloutscape-web -f

# Enable on boot
sudo systemctl enable cloutscape-server
sudo systemctl enable cloutscape-bot
sudo systemctl enable cloutscape-web
```

### Manual Start (All Platforms)

```bash
# Start all services
./start-all.sh

# Stop all services
./stop-all.sh
```

---

## 📊 Monitoring & Maintenance

### Check Server Status

```bash
# Check if services are running
ps aux | grep java
ps aux | grep python3

# Check resource usage
htop

# Check disk space
df -h

# Check memory usage
free -h
```

### View Logs

```bash
# Bot logs
tail -f bot.log

# Server logs (if using systemd)
sudo journalctl -u cloutscape-server -f

# Web logs
sudo journalctl -u cloutscape-web -f
```

### Backup Data

```bash
# Create backup directory
mkdir -p ~/backups

# Backup player accounts
cp player_accounts.json ~/backups/player_accounts_$(date +%Y%m%d).json

# Backup server data
tar -czf ~/backups/rsps-data-$(date +%Y%m%d).tar.gz rsps/releases/data/

# Backup configuration
cp .env ~/backups/env_$(date +%Y%m%d).backup
```

### Automated Backups (Cron)

```bash
# Edit crontab
crontab -e

# Add daily backup at 3 AM
0 3 * * * cd ~/CloutScape && cp player_accounts.json ~/backups/player_accounts_$(date +\%Y\%m\%d).json
```

---

## 🔄 Updating CloutScape

### Pull Latest Changes

```bash
cd ~/CloutScape

# Stop services
./stop-all.sh

# Pull updates
git pull origin main

# Rebuild if needed
cd rsps
./build-server.sh
./compile-client.sh

# Restart services
cd ..
./start-all.sh
```

### Update Dependencies

```bash
pip3 install -r requirements.txt --upgrade --user
```

---

## 🐛 Troubleshooting

### Bot Won't Start

```bash
# Check logs
tail -f bot.log

# Verify token
cat .env | grep DISCORD_TOKEN

# Reinstall dependencies
pip3 install -r requirements.txt --user --force-reinstall
```

### Server Won't Start

```bash
# Check Java version
java -version

# Check if port is in use
lsof -i :43594

# View server logs
sudo journalctl -u cloutscape-server -f
```

### Players Can't Connect

1. Check if server is running: `ps aux | grep server.jar`
2. Check Cloudflare tunnel: `cloudflared tunnel info cloutscape`
3. Verify domain in `.env` matches client
4. Check firewall rules

### Cloudflare Tunnel Issues

```bash
# Check tunnel status
cloudflared tunnel info cloutscape

# View tunnel logs
sudo journalctl -u cloudflared -f

# Restart tunnel
sudo systemctl restart cloudflared

# Test tunnel manually
cloudflared tunnel run cloutscape
```

---

## 📈 Performance Optimization

### Increase Java Heap Size

Edit `rsps/run-server.sh`:

```bash
JAVA_OPTS="-Xmx2G -Xms1G"  # Increase from 1G to 2G
```

### Enable JVM Optimizations

```bash
JAVA_OPTS="-Xmx2G -Xms1G -XX:+UseG1GC -XX:MaxGCPauseMillis=200"
```

### Use SSD Storage

For VPS deployments, choose SSD-based instances for better I/O performance.

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** to Git
2. **Use strong passwords** for admin accounts
3. **Keep software updated** regularly
4. **Enable firewall** on VPS
5. **Use SSH keys** instead of passwords for VPS access
6. **Regular backups** of player data
7. **Monitor logs** for suspicious activity

---

## 📞 Support

If you encounter issues during deployment:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review logs for error messages
3. Open an issue on [GitHub](https://github.com/No6love9/CloutScape/issues)
4. Join our Discord community for support

---

**Deployment Complete!** 🎉

Your CloutScape RSPS is now live and ready for players!
