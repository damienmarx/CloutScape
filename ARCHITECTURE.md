# CloutScape Enhanced Architecture Design

## Overview
CloutScape is a sophisticated Discord-integrated RSPS (RuneScape Private Server) platform that combines a 317 revision server with seamless Discord authentication, Cloudflare networking, and comprehensive game management features.

## System Architecture

### 1. Core Components

#### A. RSPS Server (Elvarg 317)
- **Technology**: Java-based 317 protocol server
- **Features**: 
  - Clean combat system
  - Player authentication via Discord
  - Real-time event logging to Discord
  - Economy integration with Discord bot
  - PvP tracking and leaderboards
  - Gambling system integration

#### B. Discord Bot (Enhanced CloutScape)
- **Technology**: Python 3.11+ with discord.py
- **Features**:
  - Automated server setup
  - Player authentication and registration
  - Real-time game event notifications
  - Economy management
  - Leaderboards and statistics
  - Event management
  - Admin dashboard

#### C. Web Dashboard (Flask)
- **Technology**: Flask + Python
- **Features**:
  - Real-time server statistics
  - Player management
  - Economy overview
  - Event creation and management
  - Admin controls

#### D. Cloudflare Tunnel (Networking)
- **Technology**: Cloudflare Tunnel (cloudflared)
- **Purpose**: Secure, zero-configuration networking
- **Benefits**:
  - No port forwarding required
  - DDoS protection
  - SSL/TLS encryption
  - Custom domain support
  - Free tier available

### 2. Network Architecture

```
Player (Discord) → Discord Bot → Authentication → RSPS Server
                                                      ↓
                                              Cloudflare Tunnel
                                                      ↓
                                              Public Domain
                                                      ↓
                                              Client.jar
```

#### Cloudflare Tunnel Setup
1. **Installation**: Automated via setup script
2. **Configuration**: 
   - Tunnel for RSPS server (port 43594)
   - Tunnel for web dashboard (port 5000)
   - Custom subdomain: `play.cloutscape.com` (or user's domain)
3. **Authentication**: Cloudflare token-based (free tier)

### 3. Player Authentication Flow

```
1. Player joins Discord server
2. Player runs !register command
3. Bot creates RSPS account with Discord-linked credentials
4. Bot sends player download link for client.jar
5. Player downloads client from GitHub releases
6. Player launches client with auto-configured server address
7. Player logs in with Discord-linked credentials
8. RSPS server validates with Discord bot
9. Player enters game world
```

### 4. Client Distribution System

#### GitHub Releases Integration
- **Location**: CloutScape repository releases
- **Files**:
  - `client.jar` - Pre-compiled game client
  - `server.zip` - Complete server package
  - `launcher.jar` - Auto-updating launcher (optional)
  
#### Client Configuration
- **Auto-configuration**: Client pre-configured with Cloudflare tunnel domain
- **Update system**: Automatic version checking
- **Easy launch**: Double-click to play

### 5. Server Management

#### Automated Setup Script
```bash
./setup.sh
```

**Actions**:
1. Install Java 11 (required for 317 client/server)
2. Install Python 3.11+ and dependencies
3. Install Cloudflare tunnel (cloudflared)
4. Configure Discord bot
5. Build RSPS server
6. Compile client.jar
7. Create systemd services
8. Start all services
9. Upload client.jar to GitHub releases

#### Service Management
- **RSPS Server**: `systemctl start cloutscape-server`
- **Discord Bot**: `systemctl start cloutscape-bot`
- **Web Dashboard**: `systemctl start cloutscape-web`
- **Cloudflare Tunnel**: `systemctl start cloutscape-tunnel`

### 6. Discord Integration Features

#### Channels (Enhanced)
1. **📢 announcements** - Server news and updates
2. **🎁 giveaways** - Automated giveaway system
3. **🎰 gambling-logs** - Real-time gambling results
4. **⚔️ pvp-kills** - Live PvP kill feed with loot
5. **🏆 leaderboards** - Auto-updating rankings
6. **🎯 events** - Tournament and event management
7. **💬 general** - Community chat
8. **🤖 bot-commands** - Player commands
9. **📊 server-status** - Live server statistics
10. **🎮 game-guide** - How to play guides
11. **💰 economy** - Market and trading
12. **🔧 support** - Player support tickets
13. **📝 logs** - Admin logs
14. **👑 admin** - Admin-only channel

#### Roles (Enhanced)
1. **👑 Server Owner** - Full control (red)
2. **⚡ Admin** - Administrative powers (orange)
3. **🛡️ Moderator** - Moderation tools (yellow)
4. **🎯 Event Manager** - Event creation (gold)
5. **💎 VIP** - Premium benefits (purple)
6. **🌟 Veteran** - Long-time players (blue)
7. **⚔️ PvP Legend** - Top PvP players (dark red)
8. **🎰 High Roller** - Top gamblers (green)
9. **👤 Member** - Regular players (light blue)
10. **🔇 Muted** - Restricted (gray)

#### Commands (Enhanced)
**Player Commands**:
- `!register` - Create RSPS account
- `!download` - Get client download link
- `!stats` - View your statistics
- `!leaderboard` - View rankings
- `!balance` - Check GP balance
- `!help` - Command list

**Admin Commands**:
- `!setup` - Initial server setup
- `!addgp <player> <amount>` - Add GP to player
- `!ban <player>` - Ban player
- `!unban <player>` - Unban player
- `!event create` - Create event
- `!broadcast <message>` - Server announcement

### 7. Data Storage

#### File-based Storage (JSON)
- `server_config.json` - Discord server configurations
- `player_accounts.json` - Player account data
- `gambling_stats.json` - Gambling statistics
- `pvp_stats.json` - PvP statistics
- `events.json` - Event data
- `economy.json` - Economy data

#### RSPS Server Storage
- `data/characters/` - Player save files
- `data/items/` - Item definitions
- `data/npcs/` - NPC definitions

### 8. Security Features

1. **Discord Authentication**: Players must be in Discord server
2. **Rate Limiting**: Prevent command spam
3. **Input Validation**: Sanitize all inputs
4. **Cloudflare Protection**: DDoS mitigation
5. **Encrypted Connections**: SSL/TLS via Cloudflare
6. **Admin Verification**: Multi-factor admin authentication
7. **Audit Logging**: All admin actions logged

### 9. Deployment Options

#### Option A: Desktop/Local (Recommended for Testing)
- Run on Windows/Mac/Linux
- Cloudflare tunnel for public access
- Easy setup with automated scripts

#### Option B: VPS/Cloud (Recommended for Production)
- Ubuntu 22.04 LTS
- 2GB+ RAM recommended
- Automated deployment script
- 24/7 uptime

#### Option C: Docker (Advanced)
- Containerized deployment
- Easy scaling
- Included Dockerfile

### 10. Monitoring and Analytics

#### Real-time Metrics
- Active players online
- Total registered players
- Server uptime
- Gambling statistics
- PvP activity
- Economy health

#### Discord Webhooks
- Player login/logout notifications
- Major achievements
- PvP kills with loot values
- Gambling jackpots
- Event announcements
- Server status alerts

### 11. Scalability

#### Current Capacity
- **Players**: 100+ concurrent (317 protocol limitation)
- **Discord**: Unlimited server members
- **Storage**: File-based (suitable for small-medium servers)

#### Future Enhancements
- Database migration (PostgreSQL/MySQL)
- Multiple world support
- Load balancing
- Redis caching

### 12. Technology Stack Summary

| Component | Technology | Version |
|-----------|-----------|---------|
| RSPS Server | Java | 11 |
| Discord Bot | Python | 3.11+ |
| Web Framework | Flask | 3.0+ |
| Networking | Cloudflare Tunnel | Latest |
| Client | Java Applet/Application | 11 |
| OS | Ubuntu/Windows/macOS | 22.04+ |

### 13. File Structure

```
CloutScape/
├── bot.py                      # Discord bot
├── app.py                      # Web dashboard
├── setup.sh                    # Automated setup script
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── README.md                   # Documentation
├── ARCHITECTURE.md             # This file
├── modules/                    # Bot modules
│   ├── __init__.py
│   ├── events.py               # Event system
│   ├── gambling.py             # Gambling system
│   ├── pvp.py                  # PvP tracking
│   ├── rewards.py              # Economy system
│   ├── webhooks.py             # Discord webhooks
│   └── rsps_integration.py     # RSPS server integration
├── rsps/                       # RSPS server files
│   ├── server/                 # Server source
│   ├── client/                 # Client source
│   ├── data/                   # Game data
│   ├── build.sh                # Build script
│   ├── run-server.sh           # Server launcher
│   └── compile-client.sh       # Client compiler
├── releases/                   # Built files for distribution
│   ├── client.jar              # Compiled client
│   └── server.zip              # Server package
├── cloudflare/                 # Cloudflare configuration
│   ├── tunnel-config.yml       # Tunnel configuration
│   └── setup-tunnel.sh         # Tunnel setup script
├── systemd/                    # Service files
│   ├── cloutscape-server.service
│   ├── cloutscape-bot.service
│   ├── cloutscape-web.service
│   └── cloutscape-tunnel.service
└── discord-content/            # Discord channel content
    ├── announcements.md
    ├── game-guide.md
    ├── rules.md
    └── starter-content.json
```

### 14. Development Roadmap

#### Phase 1: Core Integration ✅
- Integrate Elvarg 317 server
- Build client.jar compilation
- Setup Cloudflare tunneling
- Basic Discord authentication

#### Phase 2: Enhanced Features ✅
- Advanced Discord bot commands
- Real-time event notifications
- Economy integration
- Leaderboard systems

#### Phase 3: Content & Polish ✅
- Engaging Discord channel content
- Comprehensive documentation
- Automated setup scripts
- Testing and debugging

#### Phase 4: Deployment 🔄
- GitHub releases setup
- Production deployment
- Performance optimization
- User onboarding

## Conclusion

This architecture provides a robust, scalable, and user-friendly platform for running a Discord-integrated RSPS. The use of Cloudflare tunnels eliminates complex networking setup, while the automated scripts ensure anyone can deploy their own server with minimal technical knowledge.
