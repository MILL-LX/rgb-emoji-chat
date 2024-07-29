# Systemd Service Installation

This application can start up automatically on reboot of your Raspberry Pi. Use the following commands to install the service, start the application, and enable it to start up on reboot:

```bash
cd /home/rpi/rgb-emoji-chat
sudo cp runtime/systemd/ft-server.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl stop ft-server.service
sudo systemctl start ft-server.service
sudo systemctl enable ft-server.service
```