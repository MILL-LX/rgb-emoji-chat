# RGB Emoji Chat
An LED sign that displays emoji based on a chat conversation

## Set up the Pi

### OS

Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to create the OS image for your Pi.

This project has been developed on a Raspberry Pi 3 running *Bullseye - light* with SSH enabled and a public key installed. Installing the public key will make your life easier if you like to use the VSCode Remote SSH plugin to develop directly on the Pi.

### Tooling

#### Update the OS packages

```bash
sudo apt update
sudo apt full-upgrade
```

#### Install Tools and Dependencies

```bash
sudo apt install \
    git \
    python3 \
    python3-pip \
```

## Cloning the repository

This project depends on our fork of the [flaschen-taschen](https://github.com/hzeller/flaschen-taschen) project. It is included as a submodule in the [dependencies](dependencies) folder of this project. As such, make sure to use the `--recursive` option when cloning this repo onto your Raspberry Pi:

`git clone --recursive https://github.com/MILL-LX/rgb-emoji-chat.git`