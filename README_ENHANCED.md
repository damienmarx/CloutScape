# 🎮 CloutScape - Discord-Integrated RSPS Platform

> **The most sophisticated Discord-integrated RuneScape Private Server platform with zero-configuration networking, automated setup, and seamless player authentication.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/badge/Discord-Integrated-7289DA.svg)](https://discord.com)
[![RSPS](https://img.shields.io/badge/RSPS-317-green.svg)](https://github.com/No6love9/CloutScape)

---

## 🌟 What is CloutScape?

CloutScape is a **complete RSPS ecosystem** that seamlessly integrates a 317 revision RuneScape Private Server with Discord, featuring:

- **🔐 Discord Authentication** - Players register and login using Discord accounts
- **🌐 Cloudflare Networking** - Zero port forwarding, DDoS protection, SSL encryption
- **🤖 Sophisticated Bot** - Comprehensive Discord bot with economy, events, and management
- **📊 Web Dashboard** - Real-time server statistics and admin controls
- **📥 Easy Distribution** - Pre-compiled client.jar and server packages
- **⚡ One-Command Setup** - Fully automated installation and configuration

---

## ✨ Key Features

### 🎯 For Players

- **Simple Registration**: Register with `!register username` in Discord
- **Instant Download**: Get client.jar with `!download` command
- **Secure Login**: Discord-linked authentication, no password sharing
- **Live Statistics**: View your stats, leaderboards, and rankings
- **Real-time Notifications**: Get notified of PvP kills, gambling wins, events
- **Economy System**: Earn and manage GP through gameplay

### 👑 For Server Owners

- **Zero Configuration**: Automated setup script handles everything
- **No Port Forwarding**: Cloudflare tunnel provides public access
- **DDoS Protection**: Built-in Cloudflare security
- **Easy Management**: Discord commands for all admin tasks
- **Scalable**: Supports 100+ concurrent players
- **Professional**: Production-ready with systemd services

### 🛠️ For Developers

- **Clean Codebase**: Well-documented, modular architecture
- **RSPS Integration**: Full 317 server with Discord API bridge
- **Extensible**: Easy to add custom features and modules
- **Open Source**: MIT licensed, fork and customize freely

---

## 🚀 Quick Start (3 Minutes)

### Prerequisites

- **Operating System**: Linux (Ubuntu 22.04+), macOS, or Windows (WSL2)
- **Discord Bot**: Create at [Discord Developer Portal](https://discord.com/developers/applications)
- **Cloudflare Account**: Free account at [Cloudflare](https://www.cloudflare.com) (optional but recommended)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/No6love9/CloutScape.git
cd CloutScape

# 2. Run automated setup
chmod +x setup.sh
./setup.sh

# 3. Start all services
./start-all.sh
```

**That's it!** Your RSPS is now running. 🎉

---

## 📋 Detailed Setup Guide

### Step 1: Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and name it "CloutScape"
3. Go to "Bot" section and click "Add Bot"
4. Copy the **Bot Token** (you'll need this)
5. Enable these **Privileged Gateway Intents**:
   - Server Members Intent
   - Message Content Intent
6. Go to "OAuth2" → "URL Generator"
7. Select scopes: `bot`, `applications.commands`
8. Select permissions: `Administrator`
9. Copy the generated URL and invite bot to your server

### Step 2: Get Your Discord Admin ID

1. Open Discord and enable Developer Mode:
   - User Settings → Advanced → Developer Mode (toggle on)
2. Right-click your username and select "Copy User ID"
3. Save this ID (you'll need it during setup)

### Step 3: Run Automated Setup

The setup script will:
- ✅ Install Java 11 (required for RSPS)
- ✅ Install Python 3 and dependencies
- ✅ Build RSPS server from source
- ✅ Compile client.jar
- ✅ Configure environment variables
- ✅ Setup Cloudflare tunnel (optional)
- ✅ Install systemd services (Linux only)
- ✅ Create starter scripts

```bash
./setup.sh
```

During setup, you'll be prompted for:
- Discord Bot Token
- Discord Admin ID
- Cloudflare Domain (optional)

### Step 4: Start Services

#### Option A: Start All Services at Once

```bash
./start-all.sh
```

#### Option B: Start Services Individually

```bash
# Terminal 1: Start RSPS server
cd rsps
./run-server.sh

# Terminal 2: Start Discord bot
python3 bot_enhanced_v2.py

# Terminal 3: Start web dashboard
python3 app_enhanced.py
```

#### Option C: Use Systemd (Linux Only)

```bash
# Enable services to start on boot
sudo systemctl enable cloutscape-server
sudo systemctl enable cloutscape-bot
sudo systemctl enable cloutscape-web

# Start services
sudo systemctl start cloutscape-server
sudo systemctl start cloutscape-bot
sudo systemctl start cloutscape-web

# Check status
sudo systemctl status cloutscape-server
```

### Step 5: Setup Discord Server

1. Invite the bot to your Discord server (use URL from Step 1)
2. In your Discord server, run: `!setup`
3. Confirm with "yes"
4. Bot will create all channels, roles, and permissions

### Step 6: Distribute Client

#### Upload to GitHub Releases

```bash
# Create a new release on GitHub
gh release create v1.0.0 \
  rsps/releases/client.jar \
  --title "CloutScape v1.0.0" \
  --notes "Initial release"
```

Players can now download with `!download` command in Discord!

---

## 🎮 Player Guide

### How to Join

1. **Join Discord Server**: Join the CloutScape Discord server
2. **Register Account**: Type `!register YourUsername` in bot-commands channel
3. **Check DMs**: Bot will send you login credentials via DM
4. **Download Client**: Type `!download` to get client.jar download link
5. **Launch Client**: Double-click client.jar to start playing
6. **Login**: Use the credentials from your DM
7. **Play**: Enjoy CloutScape!

### Player Commands

| Command | Description |
|---------|-------------|
| `!register <username>` | Create a new RSPS account |
| `!download` | Get client download link |
| `!stats [@user]` | View player statistics |
| `!leaderboard` | View top players |
| `!help` | Show all commands |

---

## 👑 Admin Guide

### Admin Commands

| Command | Description |
|---------|-------------|
| `!setup` | Setup Discord server (one-time) |
| `!addgp <@user> <amount>` | Add GP to player |
| `!removegp <@user> <amount>` | Remove GP from player |
| `!ban <@user> [reason]` | Ban a player |
| `!unban <@user>` | Unban a player |
| `!resetpass <@user>` | Reset player password |
| `!broadcast <message>` | Send server announcement |

### Server Management

#### View Logs

```bash
# Bot logs
tail -f bot.log

# Server logs (systemd)
sudo journalctl -u cloutscape-server -f

# Web dashboard logs
sudo journalctl -u cloutscape-web -f
```

#### Restart Services

```bash
# Restart all
./stop-all.sh
./start-all.sh

# Or with systemd
sudo systemctl restart cloutscape-server
sudo systemctl restart cloutscape-bot
sudo systemctl restart cloutscape-web
```

#### Backup Data

```bash
# Backup player accounts
cp player_accounts.json player_accounts.backup.json

# Backup server data
tar -czf rsps-backup-$(date +%Y%m%d).tar.gz rsps/releases/data/
```

---

## 🌐 Cloudflare Tunnel Setup

Cloudflare Tunnel provides **free, secure, zero-configuration networking** for your RSPS.

### Benefits

- ✅ **No Port Forwarding**: No router configuration needed
- ✅ **DDoS Protection**: Cloudflare's network protects your server
- ✅ **SSL/TLS**: Encrypted connections for web dashboard
- ✅ **Custom Domain**: Use your own domain (e.g., play.cloutscape.com)
- ✅ **Free Tier**: No cost for basic usage

### Setup

```bash
# Run Cloudflare setup script
cd cloudflare
./setup-tunnel.sh
```

The script will:
1. Install cloudflared
2. Login to your Cloudflare account
3. Create a tunnel named "cloutscape"
4. Configure tunnel for RSPS server and web dashboard
5. Route your domain to the tunnel

### Manual Setup

If you prefer manual setup:

```bash
# 1. Install cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# 2. Login to Cloudflare
cloudflared tunnel login

# 3. Create tunnel
cloudflared tunnel create cloutscape

# 4. Configure tunnel
nano ~/.cloudflared/config.yml
```

**config.yml example:**

```yaml
tunnel: YOUR_TUNNEL_ID
credentials-file: /home/ubuntu/.cloudflared/YOUR_TUNNEL_ID.json

ingress:
  # RSPS Server
  - hostname: play.yourdomain.com
    service: tcp://localhost:43594
  
  # Web Dashboard
  - hostname: dashboard.yourdomain.com
    service: http://localhost:5000
  
  # Catch-all
  - service: http_status:404
```

```bash
# 5. Route DNS
cloudflared tunnel route dns cloutscape play.yourdomain.com
cloudflared tunnel route dns cloutscape dashboard.yourdomain.com

# 6. Start tunnel
cloudflared tunnel run cloutscape

# 7. Install as service (optional)
sudo cloudflared service install
sudo systemctl start cloudflared
```

---

## 📊 Discord Server Structure

### Channels (14)

| Channel | Category | Purpose |
|---------|----------|---------|
| 📢 announcements | Information | Server news and updates |
| 🎁 giveaways | Events | Giveaway announcements |
| 🎰 gambling-logs | Gaming | Real-time gambling results |
| ⚔️ pvp-kills | Gaming | Live PvP kill feed |
| 🏆 leaderboards | Community | Auto-updating rankings |
| 🎯 events | Events | Tournament announcements |
| 💬 general | Community | General discussion |
| 🤖 bot-commands | Bot | Player commands |
| 📊 server-status | Information | Live server statistics |
| 🎮 game-guide | Information | How to play guides |
| 💰 economy | Community | Market and trading |
| 🔧 support | Support | Player support tickets |
| 📝 logs | Admin | Admin logs |
| 👑 admin | Admin | Admin-only channel |

### Roles (10)

| Role | Color | Permissions | How to Get |
|------|-------|-------------|------------|
| 👑 Server Owner | Crimson | Administrator | Server owner |
| ⚡ Admin | Orange | Administrator | Promoted by owner |
| 🛡️ Moderator | Gold | Moderation | Promoted by admin |
| 🎯 Event Manager | Goldenrod | Event management | Promoted by admin |
| 💎 VIP | Purple | VIP perks | Donation/promotion |
| 🌟 Veteran | Blue | Veteran perks | Long-time players |
| ⚔️ PvP Legend | Dark Red | Special perks | Top PvP players |
| 🎰 High Roller | Green | Special perks | Top gamblers |
| 👤 Member | Light Blue | Basic perms | Auto-assigned on register |
| 🔇 Muted | Gray | Read-only | Punishment |

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                     CloutScape Platform                  │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Discord    │  │     Web      │  │     RSPS     │  │
│  │     Bot      │  │  Dashboard   │  │    Server    │  │
│  │  (Python)    │  │   (Flask)    │  │   (Java)     │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                  │                  │          │
│         └──────────────────┼──────────────────┘          │
│                            │                             │
│                    ┌───────┴────────┐                    │
│                    │  Cloudflare    │                    │
│                    │    Tunnel      │                    │
│                    └───────┬────────┘                    │
│                            │                             │
│                    ┌───────┴────────┐                    │
│                    │   Public       │                    │
│                    │   Internet     │                    │
│                    └────────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Player Registration**:
   - Player runs `!register` in Discord
   - Bot creates RSPS account
   - Bot sends credentials via DM
   - Player downloads client

2. **Player Login**:
   - Player launches client.jar
   - Client connects to Cloudflare tunnel
   - Tunnel routes to RSPS server
   - Server validates with Discord bot
   - Player enters game

3. **Game Events**:
   - RSPS server logs events
   - Bot reads event logs
   - Bot sends Discord notifications
   - Web dashboard updates statistics

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| RSPS Server | Java | 11 |
| Discord Bot | Python | 3.11+ |
| Web Framework | Flask | 3.0+ |
| Networking | Cloudflare Tunnel | Latest |
| Client | Java Application | 11 |
| Database | JSON Files | - |

---

## 📁 Project Structure

```
CloutScape/
├── bot_enhanced_v2.py          # Enhanced Discord bot
├── app_enhanced.py             # Web dashboard
├── setup.sh                    # Automated setup script
├── start-all.sh                # Start all services
├── stop-all.sh                 # Stop all services
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── README.md                   # This file
├── ARCHITECTURE.md             # Architecture documentation
├── FEATURES.md                 # Features documentation
│
├── modules/                    # Bot modules
│   ├── rsps_integration.py     # RSPS server integration
│   ├── gambling.py             # Gambling system
│   ├── pvp.py                  # PvP tracking
│   ├── events.py               # Event management
│   ├── rewards.py              # Economy system
│   └── webhooks.py             # Discord webhooks
│
├── rsps/                       # RSPS server files
│   ├── server/                 # Server source code
│   ├── client/                 # Client source code
│   ├── data/                   # Game data files
│   ├── releases/               # Built files
│   │   ├── client.jar          # Compiled client
│   │   ├── server.jar          # Compiled server
│   │   └── data/               # Server data
│   ├── build-server.sh         # Server build script
│   ├── compile-client.sh       # Client compile script
│   └── run-server.sh           # Server launcher
│
├── cloudflare/                 # Cloudflare configuration
│   └── setup-tunnel.sh         # Tunnel setup script
│
├── systemd/                    # Systemd service files
│   ├── cloutscape-server.service
│   ├── cloutscape-bot.service
│   ├── cloutscape-web.service
│   └── cloutscape-tunnel.service
│
└── discord-content/            # Discord channel content
    ├── announcements.md
    ├── game-guide.md
    └── rules.md
```

---

## 🔧 Configuration

### Environment Variables

Edit `.env` file:

```bash
# Discord Configuration
DISCORD_TOKEN=your_bot_token_here
ADMIN_ID=your_discord_user_id

# RSPS Configuration
RSPS_HOST=localhost
RSPS_PORT=43594
CLOUDFLARE_DOMAIN=play.yourdomain.com

# Web Dashboard
FLASK_PORT=5000
FLASK_ENV=production
SECRET_KEY=random_secret_key_here

# Client Download URL
CLIENT_DOWNLOAD_URL=https://github.com/No6love9/CloutScape/releases/latest/download/client.jar
```

### Server Settings

Edit `rsps/server/src/com/elvarg/Server.java` to customize:
- Server name
- Max players
- XP rates
- Drop rates
- Combat settings

### Client Settings

Edit `rsps/client/src/Client.java` to customize:
- Server address (auto-configured from CLOUDFLARE_DOMAIN)
- Client title
- Viewport size

---

## 🐛 Troubleshooting

### Bot Won't Start

```bash
# Check if token is valid
echo $DISCORD_TOKEN

# Check Python dependencies
pip3 install -r requirements.txt --user

# Check logs
tail -f bot.log
```

### Server Won't Start

```bash
# Check Java version
java -version

# Check if port is in use
lsof -i :43594

# Check server logs
tail -f rsps/releases/server.log
```

### Client Won't Connect

1. Check if server is running: `ps aux | grep server.jar`
2. Check Cloudflare tunnel: `cloudflared tunnel info cloutscape`
3. Verify domain in `.env` matches client configuration
4. Check firewall rules

### Cloudflare Tunnel Issues

```bash
# Check tunnel status
cloudflared tunnel info cloutscape

# View tunnel logs
sudo journalctl -u cloudflared -f

# Restart tunnel
sudo systemctl restart cloudflared
```

---

## 📈 Scaling & Performance

### Recommended Specifications

| Players | CPU | RAM | Storage | Bandwidth |
|---------|-----|-----|---------|-----------|
| 10-50 | 2 cores | 2 GB | 10 GB | 10 Mbps |
| 50-100 | 4 cores | 4 GB | 20 GB | 50 Mbps |
| 100-200 | 8 cores | 8 GB | 50 GB | 100 Mbps |

### Performance Optimization

1. **Increase Java heap size**:
   ```bash
   # Edit run-server.sh
   JAVA_OPTS="-Xmx2G -Xms1G"  # Increase from 1G to 2G
   ```

2. **Enable JVM optimizations**:
   ```bash
   JAVA_OPTS="-Xmx2G -Xms1G -XX:+UseG1GC -XX:MaxGCPauseMillis=200"
   ```

3. **Use SSD storage** for faster data access

4. **Enable Cloudflare caching** for web dashboard

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Elvarg RSPS** - Base 317 server implementation
- **discord.py** - Discord bot framework
- **Cloudflare** - Free tunnel and DDoS protection
- **RSPS Community** - Inspiration and support

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/No6love9/CloutScape/issues)
- **Discord**: Join our community server
- **Documentation**: See [ARCHITECTURE.md](ARCHITECTURE.md) and [FEATURES.md](FEATURES.md)

---

## 🎯 Roadmap

- [x] Discord authentication system
- [x] Cloudflare tunnel integration
- [x] Automated setup script
- [x] Web dashboard
- [x] Economy system
- [x] Event management
- [ ] Database migration (PostgreSQL)
- [ ] Multiple world support
- [ ] Mobile client (Android/iOS)
- [ ] Advanced anti-cheat
- [ ] Custom content packs

---

**Made with ❤️ by the CloutScape Team**

**Version**: 2.0.0  
**Last Updated**: February 2026  
**Status**: Production Ready ✅

🎮 **Start your RSPS journey today!** 🎮
