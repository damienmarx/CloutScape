# ⚡ CloutScape Quick Start Guide

Get your CloutScape RSPS up and running in **under 5 minutes**!

---

## 🎯 What You'll Need

- **Discord Bot Token**: Get from [Discord Developer Portal](https://discord.com/developers/applications)
- **Your Discord User ID**: Right-click your name in Discord → "Copy User ID"
- **5 minutes of your time**: That's it!

---

## 🚀 Installation (3 Commands)

### 1. Clone the Repository

```bash
git clone https://github.com/No6love9/CloutScape.git
cd CloutScape
```

### 2. Run Setup

```bash
chmod +x setup.sh
./setup.sh
```

**What happens:**
- Installs Java 11 (for RSPS)
- Installs Python dependencies
- Builds server and client
- Creates configuration files
- Sets up systemd services (optional)

**You'll be prompted for:**
- Discord Bot Token
- Discord Admin ID
- Cloudflare Domain (optional - press Enter to skip)

### 3. Start Everything

```bash
./start-all.sh
```

**Done!** Your RSPS is now running. 🎉

---

## 🎮 For Players

### How to Join

**1. Join Discord Server**
- Get invite link from server owner

**2. Register Account**
```
!register YourUsername
```
- Bot will DM you your password

**3. Download Client**
```
!download
```
- Click the download link

**4. Play!**
- Double-click `client.jar`
- Login with your credentials
- Start playing!

### Player Commands

| Command | What It Does |
|---------|-------------|
| `!register <username>` | Create your account |
| `!download` | Get client download link |
| `!stats` | View your statistics |
| `!leaderboard` | See top players |
| `!help` | Show all commands |

---

## 👑 For Server Owners

### Setup Discord Server

**1. Invite Bot to Your Server**
- Use the invite URL from Discord Developer Portal
- Make sure bot has Administrator permissions

**2. Run Setup Command**
```
!setup
```
- Bot creates all channels and roles automatically

**3. Upload Client to GitHub**
```bash
gh release create v1.0.0 \
  rsps/releases/client.jar \
  --title "CloutScape v1.0.0" \
  --notes "Initial release"
```

**4. Players Can Now Join!**
- Share your Discord invite link
- Players register with `!register`
- They download client with `!download`

### Admin Commands

| Command | What It Does |
|---------|-------------|
| `!setup` | Setup Discord server (one-time) |
| `!addgp <@user> <amount>` | Give GP to player |
| `!ban <@user>` | Ban a player |
| `!unban <@user>` | Unban a player |
| `!broadcast <message>` | Send announcement |

---

## 🌐 Optional: Cloudflare Tunnel

Want players to connect without port forwarding?

```bash
cd cloudflare
./setup-tunnel.sh
```

**Benefits:**
- ✅ No port forwarding needed
- ✅ DDoS protection
- ✅ Custom domain (play.yourdomain.com)
- ✅ Free!

---

## 🔧 Managing Your Server

### Start/Stop Services

```bash
# Start everything
./start-all.sh

# Stop everything
./stop-all.sh
```

### View Logs

```bash
# Bot logs
tail -f bot.log

# Server logs (if using systemd)
sudo journalctl -u cloutscape-server -f
```

### Restart After Changes

```bash
./stop-all.sh
./start-all.sh
```

---

## 📊 What Gets Created

### Discord Channels (14)

- 📢 **announcements** - Server news
- 🎁 **giveaways** - Giveaway events
- 🎰 **gambling-logs** - Gambling results
- ⚔️ **pvp-kills** - PvP kill feed
- 🏆 **leaderboards** - Top players
- 🎯 **events** - Tournaments
- 💬 **general** - General chat
- 🤖 **bot-commands** - Bot commands
- 📊 **server-status** - Live stats
- 🎮 **game-guide** - How to play
- 💰 **economy** - Trading
- 🔧 **support** - Help desk
- 📝 **logs** - Admin logs
- 👑 **admin** - Admin only

### Discord Roles (10)

- 👑 **Server Owner** - Full control
- ⚡ **Admin** - Administrative
- 🛡️ **Moderator** - Moderation
- 🎯 **Event Manager** - Events
- 💎 **VIP** - Premium perks
- 🌟 **Veteran** - Long-time players
- ⚔️ **PvP Legend** - Top PvP
- 🎰 **High Roller** - Top gamblers
- 👤 **Member** - Regular players
- 🔇 **Muted** - Restricted

---

## 🐛 Troubleshooting

### Bot Won't Start

```bash
# Check if token is correct
cat .env | grep DISCORD_TOKEN

# Reinstall dependencies
pip3 install -r requirements.txt --user
```

### Server Won't Start

```bash
# Check Java version (needs 11+)
java -version

# Check if port is in use
lsof -i :43594
```

### Players Can't Connect

1. Make sure server is running: `ps aux | grep server.jar`
2. Check Cloudflare tunnel: `cloudflared tunnel info cloutscape`
3. Verify domain in `.env` file

---

## 📚 More Information

- **Full Documentation**: See [README_ENHANCED.md](README_ENHANCED.md)
- **Architecture Details**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Deployment Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Features List**: See [FEATURES.md](FEATURES.md)

---

## 🎯 Next Steps

1. ✅ Setup complete? Invite bot to Discord
2. ✅ Run `!setup` in your Discord server
3. ✅ Upload client to GitHub releases
4. ✅ Share Discord invite with players
5. ✅ Enjoy your RSPS!

---

**Need Help?**
- Open an issue on [GitHub](https://github.com/No6love9/CloutScape/issues)
- Check the troubleshooting section above
- Review the full documentation

---

**That's it! You're ready to run CloutScape!** 🚀

*Made with ❤️ by the CloutScape Team*
