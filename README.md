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

Some packages may not be required but are specified in the [hzeller rpi-rgb-led-matrix library repo](https://github.com/hzeller/rpi-rgb-led-matrix) on which this project depends.

<!-- TODO: verify the actual requirements of the LED Matrix Library, or maybe just poin to the requirements in the library's repo. -->

```bash
sudo apt install \
    git \
    python3 \
    python3-pip \
```
