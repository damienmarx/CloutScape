# CloutScape Pro - Implementation Guide

**Status**: Core infrastructure complete. Discord bot, economy system, and REST API operational.

## Project Overview

CloutScape Pro is an elite OSRS-themed casino, POS, economy, and community platform built on Discord with RuneLite integration. The system combines a powerful Discord bot, backend REST API, and provably fair gambling mechanics to create an immersive player-driven economy.

## Architecture

### Core Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Discord Bot** | discord.py | Player commands, games, economy management |
| **Backend API** | Flask + SQLAlchemy | RESTful endpoints for game state and data |
| **Database** | JSON (dev) / MySQL (prod) | Player accounts, inventory, game logs |
| **Gambling System** | Python | Provably fair RNG, game logic, statistics |
| **RSPS Integration** | Socket/HTTP | Server communication and player management |

### Directory Structure

```
CloutScape_git/
├── bot.py                      # Main Discord bot (enhanced v2)
├── api.py                      # Flask REST API
├── cogs/
│   ├── economy.py             # Economy commands (transfer, balance)
│   ├── games.py               # Casino games (dice, poker, slots, craps)
│   ├── admin.py               # Admin commands (ban, addgp, broadcast)
│   └── profiles.py            # Player profiles and leaderboards
├── modules/
│   ├── rsps_integration.py    # RSPS server communication
│   ├── gambling.py            # Gambling system and RNG
│   ├── pvp.py                 # PvP system
│   ├── events.py              # Event management
│   ├── rewards.py             # Daily rewards and bonuses
│   └── webhooks.py            # Discord webhook management
├── templates/                  # Flask HTML templates
├── SYSTEM_PROMPT.md           # AI architect guidelines
└── requirements.txt           # Python dependencies
```

## Features Implemented

### ✅ Completed

1. **Discord Bot Core**
   - Server setup with automated channel/role creation
   - Player registration and account management
   - Profile viewing and statistics
   - Leaderboards (GP, logins)

2. **Economy System**
   - GP balance tracking
   - Player-to-player transfers
   - Admin balance management (add/remove/set)

3. **Casino Games**
   - **Dice Duel**: High roll wins (1-100 range)
   - **Flower Poker**: Hand ranking system
   - **Slots**: 3-reel with multipliers (10x jackpot)
   - **Craps**: Simplified 7/11 win, 2/3/12 lose logic
   - **Roulette**: Number/color/odd-even betting

4. **Admin Tools**
   - Player banning/unbanning
   - Password reset
   - GP manipulation
   - Rank assignment
   - Server broadcasts

5. **REST API**
   - Player profile endpoints
   - Leaderboard queries
   - Gambling statistics
   - Admin management endpoints
   - Server health checks

### 🔄 In Progress

- Inventory system (stackable/noted items)
- GE price sync (live prices.runescape.wiki)
- RuneLite overlay integration
- Provably fair verification logs
- Tournament system

### 📋 Planned

- Monetization layer (VIP subscriptions, Patreon sync)
- Advanced anti-cheat (session tracking, pattern detection)
- Dynamic house edge configuration
- OCR fallback for game verification
- WebSocket real-time updates

## Setup Instructions

### Prerequisites

- Python 3.11+
- Discord bot token (from Discord Developer Portal)
- Admin Discord ID
- Flask + discord.py installed

### Installation

```bash
# Clone the repository
git clone https://github.com/No6love9/CloutScape.git
cd CloutScape

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DISCORD_TOKEN="your_bot_token_here"
export ADMIN_ID="your_discord_id_here"
export CLOUTSCAPE_API_KEY="your_api_key_here"

# Run the bot
python3 bot.py

# In another terminal, run the API
python3 api.py
```

### Environment Variables

```bash
# Discord Bot
DISCORD_TOKEN=your_token_here
ADMIN_ID=your_discord_id
GUILD_ID=optional_guild_id
COMMAND_PREFIX=!

# RSPS Server
RSPS_HOST=localhost
RSPS_PORT=43594
CLOUDFLARE_DOMAIN=play.cloutscape.com

# Flask API
API_PORT=5000
API_HOST=0.0.0.0
FLASK_DEBUG=False
CLOUTSCAPE_API_KEY=dev-key-change-in-production
```

## Command Reference

### Player Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `!register <username>` | `!register Zezima` | Create in-game account |
| `!profile [@member]` | `!profile @Player` | View player profile |
| `!balance` | `!balance` | Check GP balance |
| `!transfer <@member> <amount>` | `!transfer @Player 1000` | Send GP to player |
| `!dice <bet> <@opponent>` | `!dice 1000 @Player` | Dice duel (1-100) |
| `!flowerpoker <bet> <@opponent>` | `!flowerpoker 5000 @Player` | Flower poker game |
| `!slots <bet>` | `!slots 500` | Spin slots (3-reel) |
| `!craps <bet>` | `!craps 1000` | Play craps |
| `!leaderboard [gp\|logins]` | `!leaderboard gp` | View top players |
| `!achievements [@member]` | `!achievements @Player` | View achievements |

### Admin Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `!setup` | `!setup` | Create server channels/roles |
| `!addgp <@member> <amount>` | `!addgp @Player 10000` | Add GP to player |
| `!removegp <@member> <amount>` | `!removegp @Player 5000` | Remove GP from player |
| `!setgp <@member> <amount>` | `!setgp @Player 50000` | Set exact GP balance |
| `!ban <@member> [reason]` | `!ban @Player Cheating` | Ban player |
| `!unban <@member>` | `!unban @Player` | Unban player |
| `!resetpass <@member>` | `!resetpass @Player` | Reset player password |
| `!broadcast <message>` | `!broadcast Server maintenance at 10pm` | Send announcement |
| `!players` | `!players` | List all registered players |
| `!delaccount <@member>` | `!delaccount @Player` | Delete player account |
| `!setrank <@member> <rank>` | `!setrank @Player VIP` | Set player rank |

## API Endpoints

### Player Endpoints

```
GET  /api/players/<player_id>           # Get player profile
GET  /api/players                        # List all players
GET  /api/players/<player_id>/balance   # Get player balance
POST /api/players/<player_id>/balance   # Update balance (requires API key)
```

### Leaderboard Endpoints

```
GET  /api/leaderboard/gp?limit=10      # GP leaderboard
GET  /api/leaderboard/logins?limit=10  # Login leaderboard
```

### Gambling Endpoints

```
GET  /api/gambling/stats/<player_id>   # Get player gambling stats
GET  /api/gambling/logs?limit=50       # Get recent gambling logs
```

### Admin Endpoints

```
POST /api/admin/ban/<player_id>              # Ban player (requires API key)
POST /api/admin/unban/<player_id>            # Unban player (requires API key)
POST /api/admin/reset-password/<player_id>  # Reset password (requires API key)
```

### Server Endpoints

```
GET  /api/status                        # RSPS server status
GET  /api/health                        # Health check
```

## Testing

### Test Player Registration

```bash
# In Discord, run:
!register TestPlayer
# Bot will DM you with login credentials
```

### Test Dice Game

```bash
# Player 1:
!dice 1000 @Player2

# Player 2 will be prompted to accept
# Winner gets 2x bet amount
```

### Test API

```bash
# Get player profile
curl http://localhost:5000/api/players/123456789

# Get GP leaderboard
curl http://localhost:5000/api/leaderboard/gp?limit=5

# Add GP (requires API key)
curl -X POST http://localhost:5000/api/players/123456789/balance \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action": "add", "amount": 10000}'
```

## Next Logical Milestones

### Phase 1: Inventory & POS System (Priority)
- Stackable/noted item system
- GE price sync from prices.runescape.wiki
- Player-to-player trading with confirmation
- Bank PIN security

### Phase 2: Provably Fair Gambling
- Server-side seeded RNG
- Client verification logs
- Transparent hash chains
- Audit trail for all bets

### Phase 3: RuneLite Integration
- Java plugin for overlay
- WebSocket real-time updates
- OCR fallback for game verification
- In-client action triggers

### Phase 4: Monetization
- Discord subscription tiers (VIP perks)
- Patreon role sync
- Cosmetic shop
- Referral bonus system

### Phase 5: Advanced Features
- Tournament system with live brackets
- Dynamic house edge (1-5% configurable)
- Anti-cheat pattern detection
- CAPTCHA on high-value bets

## Deployment

### Production Checklist

- [ ] Change `CLOUTSCAPE_API_KEY` to secure random value
- [ ] Set `FLASK_DEBUG=False`
- [ ] Configure MySQL/PostgreSQL database
- [ ] Set up SSL/TLS for API
- [ ] Configure rate limiting
- [ ] Enable audit logging
- [ ] Set up monitoring and alerts
- [ ] Deploy to cloud (AWS, GCP, Azure)
- [ ] Configure Cloudflare for DDoS protection

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "bot.py"]
```

## Troubleshooting

### Bot not responding to commands

- Verify `DISCORD_TOKEN` is correct
- Check bot has permissions in the guild
- Ensure `COMMAND_PREFIX` matches your usage
- Check bot.log for errors

### API returning 401

- Verify `X-API-Key` header is set correctly
- Ensure `CLOUTSCAPE_API_KEY` environment variable is set

### Player account not found

- Run `!register <username>` first
- Check player_accounts.json exists
- Verify Discord ID is correct

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the development team
- Join our Discord server

---

**CloutScape Pro is your legacy. Build it. Perfect it. Scale it.**
