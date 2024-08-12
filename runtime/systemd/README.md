# Systemd Service Installation

This application is comprised of two services that can start up automatically on reboot of your Raspberry Pi. Use the following commands to install the services, start them, and enable them to start up on reboot:

```bash
cd /home/rpi/rgb-emoji-chat
sudo cp runtime/systemd/ft-server.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl stop ft-server.service
sudo systemctl start ft-server.service
sudo systemctl enable ft-server.service

sudo cp runtime/systemd/rgb-emoji-chat.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl stop rgb-emoji-chat.service
sudo systemctl start rgb-emoji-chat.service
sudo systemctl enable rgb-emoji-chat.service
```
