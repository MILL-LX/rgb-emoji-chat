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
    python3-pip \
    pipx
```

#### Turn off Pi Audio

There is a conflict between the LED matrix library and the audio hardware on the Pi.

Edit `/boot/firmware/config.txt` and set `dtparam=audio=off` then reboot the Pi.

## Cloning the repository

This project depends on our fork of the [flaschen-taschen](https://github.com/MILL-LX/flaschen-taschen.git) project. It is included as a submodule in the [dependencies](dependencies) folder of this project. As such, make sure to use the `--recursive` option when cloning this repo onto your Raspberry Pi:

`git clone --recursive https://github.com/MILL-LX/rgb-emoji-chat.git`

## Building and running the flaschen-taschen server

The flaschen-tashen server provides a network interface to the display that it manages. We need to build the version manages an RGB LED Matrix and copy the binary to where we keep the runtime files for this project: 

```bash
$ cd dependencies/flaschen-taschen/server
$ make FT_BACKEND=rgb-matrix
```

There is a symbolic link from `runtime/ft-server` to the newly built server. Instructions for installing the server as a systemd service are available in [runtime/systemd/README.md](runtime/systemd/README.md).
