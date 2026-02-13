# CloutScape AIO - Ultimate OSRS Ecosystem

**CloutScape** is a comprehensive OSRS ecosystem featuring a native **Discord Setup Bot**, a professional **Web Platform** for gold trading, and advanced community management tools.

## 🌟 Two Core Components

### 1. 🤖 Discord Setup Bot (AIO)
An all-in-one Python3 Discord bot that automatically configures your Discord server for CloutScape AIO.
- ✅ **Auto-Setup** - Creates all required channels, roles, and permissions with a single command.
- ✅ **Zero Configuration** - Only requires Discord token and admin ID.
- ✅ **Web Dashboard** - Flask app for monitoring and management.
- ✅ **Secure & Fast** - Complete server setup in under a minute.

### 2. 💎 CloutScape Pro Platform (Web & Gold Trading)
A professional web application for OSRS players to buy gold at the cheapest prices and join a vibrant gambling community.
- ✅ **Live Price Comparison** - Real-time competitor tracking with automated scraping.
- ✅ **Smart Pricing** - Always 15% below market average.
- ✅ **Discord/Telegram Bots** - Community integration with commands and webhooks.
- ✅ **Admin Dashboard** - Complete control panel for orders, users, and prices.
- ✅ **Docker Ready** - Full stack orchestration with PostgreSQL and Redis.

---

## 🚀 Quick Start

### 1. Discord Setup Bot
```bash
# Clone repository
git clone https://github.com/No6love9/CloutScape.git
cd CloutScape

# Install dependencies
pip install -r requirements.txt

# Configure .env and run
python3 bot.py
python3 app.py
```
*Run `!setup` in your Discord server to begin.*

### 2. Pro Web Platform
```bash
cd platform/
cp .env.example .env
# Edit .env with your credentials
docker-compose up -d
```
*See [QUICKSTART_PRO.md](QUICKSTART_PRO.md) for detailed setup.*

---

## 📁 Project Structure

```
CloutScape/
├── platform/               # 🆕 Pro Web Platform (Flask, Postgres, Redis)
├── modules/                # Bot logic modules (gambling, pvp, etc.)
├── templates/              # Web dashboard templates
├── rsps/                   # RSPS integration tools
├── bot.py                  # Main Discord bot
├── app.py                  # Flask management app
├── deploy.sh               # 🆕 Automated VPS deployment script
├── CLOUDFLARE_SETUP.md     # 🆕 Cloudflare & SSL guide
├── QUICKSTART_PRO.md       # 🆕 Pro platform setup guide
└── README.md               # This file
```

## 🌐 Deployment & Hosting

We recommend deploying the Pro Platform using the included automated tools:
1.  **Cloudflare**: Use for DNS and SSL (see `CLOUDFLARE_SETUP.md`).
2.  **VPS Deployment**: Use the `deploy.sh` script for a one-click setup on any Ubuntu server.

---

## 📖 Documentation
- **Features**: See [FEATURES.md](FEATURES.md)
- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Pro Setup**: See [QUICKSTART_PRO.md](QUICKSTART_PRO.md)
- **WSL2/Kali Guide**: See [WSL2_KALI_GUIDE.md](WSL2_KALI_GUIDE.md)
- **Integration Guide**: See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
- **Promotions & Pricing**: See [PROMOTIONS.md](PROMOTIONS.md)

## 🤝 Support
- **Issues**: [GitHub Issues](https://github.com/No6love9/CloutScape/issues)
- **Discord**: Join our community server

---
**Version**: 2.0.0 (Pro Integrated)
**Last Updated**: February 2026
**Status**: Production Ready

*Engineered for the elite OSRS community.*
