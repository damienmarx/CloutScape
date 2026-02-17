# CloutScape AIO - The Ultimate RSPS & Gambling Ecosystem

**CloutScape** is a high-performance, provocative gambling platform fully integrated with a custom RSPS (RuneScape Private Server) backend. It features a modern web interface, a comprehensive gambling suite, and a powerful Discord bot for community management.

## 🌟 Key Features

### 🎰 Advanced Gambling Suite
*   **Rich Slots**: A high-energy slot machine with custom visualizers.
*   **Keno 40**: A fast-paced 40-square Keno game with multiple hit multipliers.
*   **Crash**: High-tension multiplier game with real-time cash-out.
*   **Dice Duel**: Provably fair dice rolling against the house.

### 🤝 The Syndicate Program (Referral System)
*   **Tiered Commissions**: Earn up to 15% of the house edge from your referrals.
*   **Progressive Tiers**: Advance from Recruit to Overlord based on Total Referred Wager (TRW).
*   **Passive Income**: Commissions are automatically credited to your GP balance.
*   **Exclusive Benefits**: Unlock custom Discord roles and early access to features.

### 🛡️ Provably Fair System
*   **Transparency**: Every game outcome is predetermined using a combination of Server Seed, Client Seed, and Nonce.
*   **Verification**: Users can verify any bet result using our cryptographic fairness tool.
*   **Security**: Server seeds are hashed before play to ensure zero manipulation.

### 🌐 RSPS Integration
*   **Seamless Sync**: Real-time GP balance synchronization between the web platform and the RSPS server.
*   **Account Management**: Unified login for both the game and the gambling hub.
*   **Live Logs & Chat**: A global chat box and live bet logs to keep the community engaged.

### 🤖 Discord Setup Bot (AIO)
*   **Auto-Setup**: Creates all required channels, roles, and permissions with a single command.
*   **Web Dashboard**: Flask app for monitoring and management.
*   **Secure & Fast**: Complete server setup in under a minute.

---

## 🛠️ Technical Stack
*   **Backend**: Python (Flask), Flask-Session, Flask-CORS.
*   **Frontend**: HTML5, Tailwind CSS, JavaScript (ES6+).
*   **Database**: JSON-based flat-file system (Production-ready for Redis/SQL migration).
*   **RSPS**: Java-based 317 server with custom network protocols.

---

## 📦 Installation & Setup

### Prerequisites
*   Python 3.11+
*   Java 8+ (for RSPS server/client)

### Web Platform Setup
1.  Clone the repository:
    ```bash
    git clone https://github.com/No6love9/CloutScape.git
    cd CloutScape
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Configure environment variables in a `.env` file:
    ```env
    SECRET_KEY=your-secret-key
    DISCORD_TOKEN=your-discord-token
    ADMIN_ID=your-discord-id
    ```
4.  Run the Flask server:
    ```bash
    python3 app.py
    ```

### RSPS Server Setup
1.  Navigate to the `rsps/server` directory.
2.  Compile and run the server:
    ```bash
    ./run-server.sh
    ```

### RSPS Client Setup
1.  Navigate to the `rsps/client` directory.
2.  Compile the client:
    ```bash
    ./compile-client.sh
    ```
3.  Run the client to connect to `cloutscape.org`.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing
We welcome contributions from the elite. Fork the repo, make your changes, and submit a PR.

---
**Version**: 3.0.0 (Gambling & Syndicate Integrated)
**Last Updated**: February 2026
**Status**: Production Ready

*Engineered for the elite community by the CloutScape Team.*
