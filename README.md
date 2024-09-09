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
    bash \
    git \
    python3 \
    python3-pip
```

The following looks scary beacuse of the `--break-system-packages` flag. This should be the only thing that we need to install this way as it will help up manage our project's virtual environment.

```bash
pip3 install --user pipenv --break-system-packages
```

Add `/home/rpi/.local/bin` to your `PATH` in your shell's startup script, e.g. `~/.bashrc`

#### Configure Pi Hardware

There is a conflict between the LED matrix library and the audio hardware on the Pi.

Edit `/boot/firmware/config.txt` and set `dtparam=audio=off`.

To slightly improve display update, addn`isolcpus=3`at the end of `/boot/firmware/cmdline.txt`.

Reboot the Pi

## Clone the repository

This project depends on our fork of the [flaschen-taschen](https://github.com/MILL-LX/flaschen-taschen.git) project. It is included as a submodule in the [dependencies](dependencies) folder of this project. As such, make sure to use the `--recursive` option when cloning this repo onto your Raspberry Pi:

`git clone --recursive https://github.com/MILL-LX/rgb-emoji-chat.git`

## Install the Python Application Dependencies

In the project directory:

```bash
pipenv install
```

## Build and run the flaschen-taschen server

The flaschen-tashen server provides a network interface to the display that it manages. 
```bash
cd dependencies/flaschen-taschen/server
```

On the Pi, we need to build the version of the server that manages an RGB LED Matrix: 
```bash
make FT_BACKEND=rgb-matrix
```

On the development machine, we need to build the version of the server that runs in the terminal: 

```bash
make FT_BACKEND=terminal
``` 

There is a symbolic link from `runtime/ft-server` to the newly built server. Instructions for installing the server as a systemd service are available in [runtime/systemd/README.md](runtime/systemd/README.md).

