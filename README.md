# CloutScape AIO - Discord Setup Bot

An all-in-one Python3 Discord bot that automatically configures your Discord server for CloutScape AIO. Includes a Flask web app for management and monitoring.

## ✨ Features

✅ **Auto-Setup** - Creates all required channels, roles, and permissions with a single command
✅ **Zero Configuration** - Only requires Discord token and admin ID
✅ **Web Dashboard** - Flask app for monitoring and management
✅ **Logging** - Comprehensive logging of all bot activities
✅ **Secure** - No complex configuration needed
✅ **Fast** - Complete server setup in under a minute
✅ **Customizable** - Easy to modify channels, roles, and permissions

## 📋 What Gets Created

### Channels (10)
- **announcements** - Server announcements and updates
- **giveaways** - Giveaway announcements
- **gambling-logs** - Gambling activity logs
- **pvp-kills** - PvP kill logs
- **leaderboards** - Community leaderboards
- **events** - Event announcements
- **general** - General discussion
- **bot-commands** - Bot commands
- **logs** - Bot activity logs
- **admin** - Admin-only channel

### Roles (5)
- **Admin** - Full permissions (red)
- **Event Manager** - Event management permissions (gold)
- **VIP** - VIP member permissions (purple)
- **Member** - Regular member permissions (blue)
- **Muted** - Limited permissions (gray)

### Permissions
- Automatically configured per channel
- Role-based access control
- Admin-only channels protected

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- Discord Bot Token
- Discord Admin ID

### 2. Installation

```bash
# Clone repository
git clone https://github.com/No6love9/CloutScape.git
cd discord-setup-bot

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 3. Configuration

Edit `.env` with your credentials:

```env
DISCORD_TOKEN=your_bot_token_here
ADMIN_ID=your_discord_user_id_here
```

### 4. Get Your Credentials

#### Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section
4. Click "Add Bot"
5. Copy the token under TOKEN

#### Discord Admin ID
1. Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
2. Right-click your username
3. Select "Copy User ID"

#### Bot Invite URL
1. In Developer Portal, go to "OAuth2" → "URL Generator"
2. Select scopes: "bot"
3. Select permissions: "Administrator"
4. Copy the generated URL
5. Open in browser to invite bot to your server

### 5. Run the Bot

```bash
# Terminal 1: Start the Discord bot
python3 bot.py

# Terminal 2: Start the Flask web app
python3 app.py
```

### 6. Setup Your Server

In your Discord server, run:

```
!setup
```

Confirm with "yes" and the bot will automatically:
- Create all channels
- Create all roles
- Set up permissions
- Save configuration

### 7. Access the Dashboard

Open your browser and go to:

```
http://localhost:5000
```

## 📖 Commands

### Public Commands
- `!setup` - Setup the server (Admin only)
- `!status` - Check setup status
- `!help` - Show help message

### Admin Dashboard
- Login at `/admin`
- View server statistics
- Monitor configured servers
- Export data

## 🌐 Web App Routes

### Public Routes
- `/` - Home page
- `/setup` - Setup guide
- `/docs` - Documentation
- `/api/status` - Bot status API
- `/api/info` - Bot info API

### Admin Routes
- `/admin` - Admin login
- `/admin/dashboard` - Admin dashboard
- `/admin/logout` - Logout
- `/api/admin/stats` - Statistics API
- `/api/admin/servers` - Servers list API
- `/api/admin/server/<id>` - Server details API
- `/api/admin/settings` - Settings API

## 📁 Project Structure

```
discord-setup-bot/
├── bot.py                 # Main Discord bot
├── app.py                 # Flask web app
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── README.md              # This file
├── bot.log                # Bot logs
├── web.log                # Web app logs
├── server_config.json     # Server configurations
├── bot_settings.json      # Bot settings
└── templates/
    ├── index.html         # Home page
    ├── setup.html         # Setup guide
    ├── admin_login.html   # Admin login
    └── admin_dashboard.html # Admin dashboard
```

## 🔧 Configuration

### Bot Configuration (bot.py)

Edit the `Config` class to customize:

```python
CHANNELS = {
    'channel-name': {
        'description': 'Channel description',
        'topic': 'Channel topic',
        'nsfw': False,
        'category': 'Category Name'
    }
}

ROLES = {
    'Role Name': {
        'color': discord.Color.blue(),
        'hoist': True,
        'mentionable': True,
        'permissions': ['send_messages', 'read_messages']
    }
}
```

### Web App Configuration (app.py)

Edit the `WebConfig` class to customize:

```python
SECRET_KEY = 'your-secret-key'
SESSION_TYPE = 'filesystem'
PERMANENT_SESSION_LIFETIME = 86400
```

## 📊 Monitoring

### Bot Logs
```bash
tail -f bot.log
```

### Web App Logs
```bash
tail -f web.log
```

### Server Configuration
View `server_config.json` for all configured servers:

```json
{
  "123456789": {
    "guild_name": "My Server",
    "setup_date": "2024-02-12T10:30:00",
    "roles": 5,
    "channels": 10,
    "status": "completed"
  }
}
```

## 🔒 Security

- **Never** commit `.env` file to Git
- **Never** share your bot token publicly
- Use strong passwords for admin access
- Enable SSL/TLS in production
- Regularly update dependencies

## 🐛 Troubleshooting

### Bot Won't Start
```bash
# Check if token is valid
python3 -c "import os; print(os.getenv('DISCORD_TOKEN'))"

# Check logs
tail -f bot.log
```

### Bot Can't Create Channels
- Ensure bot has "Administrator" permission
- Check if bot role is above other roles
- Verify bot is in the server

### Web App Won't Start
```bash
# Check if port 5000 is available
lsof -i :5000

# Use different port
FLASK_PORT=5001 python3 app.py
```

### Login Failed
- Verify Admin ID is correct
- Verify Bot Token is correct
- Check admin credentials in `.env`

## 📚 API Examples

### Get Bot Status
```bash
curl http://localhost:5000/api/status
```

### Get Bot Info
```bash
curl http://localhost:5000/api/info
```

### Admin Login
```bash
curl -X POST http://localhost:5000/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"admin_id": "123456789", "token": "your_token"}'
```

### Get Server Stats
```bash
curl -X GET http://localhost:5000/api/admin/stats \
  -H "Authorization: Bearer your_token"
```

## 🚀 Deployment

### Docker
```bash
docker build -t cloutscape-bot .
docker run -e DISCORD_TOKEN=your_token -e ADMIN_ID=your_id -p 5000:5000 cloutscape-bot
```

### Heroku
```bash
heroku create your-app-name
heroku config:set DISCORD_TOKEN=your_token ADMIN_ID=your_id
git push heroku main
```

### VPS
```bash
# Install Python 3.8+
sudo apt-get install python3 python3-pip

# Install dependencies
pip3 install -r requirements.txt

# Run with systemd
sudo systemctl start cloutscape-bot
```

## 📝 Logs

### Bot Log Format
```
2024-02-12 10:30:00 - bot - INFO - Bot logged in as CloutScape#1234
2024-02-12 10:30:01 - bot - INFO - Bot is in 5 guilds
2024-02-12 10:30:02 - bot - INFO - Created role: Admin
```

### Web App Log Format
```
2024-02-12 10:30:00 - app - INFO - Starting Flask app
2024-02-12 10:30:01 - app - INFO - Loaded configurations for 5 servers
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/No6love9/CloutScape/issues)
- **Documentation**: See this README
- **Discord**: Join our community server

## 🎉 Getting Started

1. **Setup Discord Bot** - Follow the "Get Your Credentials" section
2. **Configure Environment** - Edit `.env` with your credentials
3. **Run the Bot** - Start both `bot.py` and `app.py`
4. **Setup Server** - Run `!setup` in your Discord server
5. **Access Dashboard** - Open `http://localhost:5000`

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Python** | 3.8 | 3.10+ |
| **RAM** | 512 MB | 1 GB |
| **Disk** | 100 MB | 500 MB |
| **OS** | Linux/macOS/Windows | Ubuntu 20.04+ |

## ✅ Checklist

- [ ] Created Discord bot in Developer Portal
- [ ] Copied bot token
- [ ] Got admin ID
- [ ] Created `.env` file with credentials
- [ ] Installed dependencies with `pip install -r requirements.txt`
- [ ] Started bot with `python3 bot.py`
- [ ] Started web app with `python3 app.py`
- [ ] Invited bot to Discord server
- [ ] Ran `!setup` command in server
- [ ] Accessed dashboard at `http://localhost:5000`

---

**Version**: 1.0.0
**Last Updated**: February 2026
**Status**: Production Ready

Enjoy managing your CloutScape AIO Discord server! 🎉
