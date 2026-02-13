# 🐉 Kali WSL2 Setup Guide for CloutScape

Since you are running **Kali Linux on WSL2 (Windows)**, follow these specific instructions to ensure the CloutScape platform runs smoothly.

## 1. Docker Desktop Integration
For the best experience, use **Docker Desktop for Windows** with the WSL2 backend:
1. Open Docker Desktop Settings.
2. Go to **Resources -> WSL Integration**.
3. Ensure **"Enable integration with my default WSL distro"** is checked.
4. Toggle the switch for your **Kali-Linux** distribution to **ON**.

## 2. Local Development (WSL2)
When running the platform locally in WSL2:
- **Accessing the Web App**: You can access the Flask app at `http://localhost:5000` directly from your Windows browser. WSL2 automatically handles the port forwarding.
- **Database Connection**: If you run Postgres inside Docker, use `localhost` or `127.0.0.1` as the host in your `.env` file.

## 3. Playwright in WSL2
The price scraper uses Playwright, which requires specific system dependencies in Kali:
```bash
# Install dependencies in your Kali terminal
sudo apt update
sudo apt install -y libgbm1 libnss3 libatk-bridge2.0-0 libgtk-3-0 libasound2
```

## 4. Port Forwarding (External Access)
If you want to access your WSL2-hosted site from another device on your network:
1. Find your WSL2 IP: `hostname -I`
2. In Windows PowerShell (Admin), run:
   ```powershell
   netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=[YOUR_WSL_IP]
   ```

## 5. Common WSL2 Issues
- **Memory Usage**: WSL2 can consume a lot of RAM. Create a `.wslconfig` file in your Windows User folder (`%USERPROFILE%`) to limit it:
  ```ini
  [wsl2]
  memory=4GB
  processors=4
  ```
- **Systemd**: If you need to use `systemctl` (for the legacy services), ensure systemd is enabled in your Kali WSL:
  Edit `/etc/wsl.conf`:
  ```ini
  [boot]
  systemd=true
  ```
  Then restart WSL: `wsl --shutdown` in PowerShell.

## 🚀 Running the Pro Platform in Kali WSL
```bash
cd platform
# Ensure Docker integration is active
docker-compose up -d
```

---
*Optimized for Kali Linux on Windows 10/11 via WSL2.*
