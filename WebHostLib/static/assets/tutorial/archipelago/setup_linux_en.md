# Archipelago Setup Guide (Linux)

This guide is intended to provide an overview of how to install, set up, and run the Archipelago multiworld software on a Linux-based computer.
This guide is more in-depth than the windows guide as getting Archipelago running under Linux requires more setup.

## Acquiring Dependencies

Archipelago is a python program and will run on most computers that have Python installed. This includes most, if not all Linux distributions.

Python3.10, the current stable Python release & most commonly installed on modern distributions, may have problems. If you follow the below steps and you get an error,
you may need to install Python 3.9.

You will also need pip and the python development packages to obtain all required python dependencies. Python3.9 instructions are also currently provided.
- Arch Linux: ```# pacman -S python-pip```
  - Python3.9: [Arch Linux AUR (Python3.9)](https://aur.archlinux.org/packages/python39)


- Fedora (And Derivatives): ```# dnf install pip python-devel``` 
  - Python3.9:  ```# dnf install python3.9 python3.9-devel```


- Debian: ```apt-get python3-pip python3-dev```
  - Python3.9: ```# apt-get python3.9 python3.9-dev```


- Ubuntu: ```apt-get python3-pip python3-dev``` 
  - Python3.9: [ppa/deadsnakes repository](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa)

This guide cannot account for all distributions. If your distribution is not listed here, you will have to determine how to install Python3.9 on your own.

## Installing the Archipelago software

The most recent public release of Archipelago can be found on the GitHub Releases page. GitHub Releases
page: [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases).

Download the 'Source Code' archive and extract it somewhere on your computer.

Open the directory and run:

```$ python ./ModuleUpdate.py```

Note: python may have a different path depending on your system. You may need to enter ```python``` or `python3`.

If you had to install Python3.9, use `python3.9` in place of Python.

This program will set up your Python environment with the necessary packages to run a majority of the programs.

This is sufficient for a minimum Archipelago setup.

You will also require:
- [SNI](https://github.com/alttpo/sni/releases), required for SNIClient (any SNES game). Ensure that you download the linux-amd64 package. 
  - If you plan on using an SD2SNES, you will need to add the device to udev to ensure SNI can access it. Follow the directions on the [SNI Github page](https://github.com/alttpo/sni).
- [Enemizer](https://github.com/Ijwu/Enemizer), if you plan on generating ALTTP games. Ensure you download the Linux package.

Both of these folders must be extracted in the same folder you extracted your Archipelago instance into. This is also where
any ROM files must go.

### Program Overview

- Generator.py: The generator allows you to generate multiworld games on your computer. The ROM setups are required if anyone in the
game that you generate wants to play any of those games as they are needed to generate the relevant patch files.
  - Usage: ``` $ python ./Generate.py --help ``` for options.


- MultiServer.py: The server will allow you to host the multiworld on your machine. Hosting on your machine requires forwarding the port
you are hosting on. The default port for Archipelago is `38281`. If you are unsure how to do this there are plenty of
other guides on the internet that will be more suited to your hardware.
  - Usage: ```$ python ./MultiServer.py -h``` for options.


- Clients (SNIClient.py, CommonClient.py): The `Clients` are what are used to connect your game to the multiworld. If the game/games you plan to play are available
here go ahead and install these as well. If the game you choose to play is supported by Archipelago but not listed in
the installation check the setup guide for that game. Installing a client for a ROM based game requires you to have a
legally obtained ROM for that game as well.
  - ROM files must be located in place you extracted the Archipelago archive.
  - Usage: ```$ python ./SNIClient <path_to_your_patchfile>```
  
## Generating a game

### What is a YAML?

YAML is the file format which Archipelago uses in order to configure a player's world. It allows you to dictate which
game you will be playing as well as the settings you would like for that game.

YAML is a format very similar to JSON however it is made to be more human-readable. If you are ever unsure of the
validity of your YAML file you may check the file by uploading it to the check page on the Archipelago website. Check
page: [YAML Validation Page](/mysterycheck)

### Creating a YAML

YAML files may be generated on the Archipelago website by visiting the games page and clicking the "Settings Page" link
under any game. Clicking "Export Settings" in a game's settings page will download the YAML to your system. Games
page: [Archipelago Games List](/games)

In a multiworld there must be one YAML per world. Any number of players can play on each world using either the game's
native coop system or using Archipelago's coop support. Each world will hold one slot in the multiworld and will have a
slot name and, if the relevant game requires it, files to associate it with that multiworld.

If multiple people plan to play in one world cooperatively then they will only need one YAML for their coop world. If
each player is planning on playing their own game then they will each need a YAML.

### Gather All Player YAMLs

All players that wish to play in the generated multiworld must have a YAML file which contains the settings that they
wish to play with.

Typically, a single participant of the multiworld will gather the YAML files from all other players. After getting the
YAML files of each participant for your multiworld game they can be compressed into a ZIP folder to then be uploaded to
the multiworld generator page. Multiworld generator
page: [Archipelago Seed Generator Page](https://archipelago.gg/generate)

#### Rolling a YAML Locally

It is possible to roll the multiworld locally, using a local Archipelago installation. This is done by entering the
installation directory of the Archipelago installation and placing each YAML file in the `Players` folder. If the folder
does not exist then it can be created manually.

After filling the `Players` folder the `Generator.py` program should be run in order to generate a
multiworld. The output of this process is placed in the `output` folder.

#### Changing local host settings for generation

Sometimes there are various settings that you may want to change before rolling a seed such as enabling race mode,
auto-forfeit, plando support, or setting a password.

All of these settings plus other options are able to be changed by modifying the `host.yaml` file in the Archipelago
installation folder. The settings chosen here are baked into the `.archipelago` file that gets output with the other
files after generation so if rolling locally ensure this file is edited to your liking *before* rolling the seed.

## Hosting an Archipelago Server

The output of rolling a YAML will be a `.archipelago` file which can be subsequently uploaded to the Archipelago host
game page. Archipelago host game page: [Archipelago Seed Upload Page](https://archipelago.gg/uploads)

The `.archipelago` file may be run locally in order to host the multiworld on the local machine. This is done by
running `MultiServer.py` with a parameter leading to the path to the `.archipelago` file that was
generated.

## Running Games

Linux does not natively support all of the emulators and games that are supported on Windows. However, this does not mean that these games are unplayable.

Below is a list of current, common pressure-points on Linux and what can be done to make them work.

- NES/SNES/N64 Games
  - The recommended emulator for NES and SNES titles and the required emulator for N64 is BizHawk. As of writing, the Linux version of BizHawk does not support Lua Sockets.
    Therefore, running BizHawk will require Wine. I personally recommend using Lutris.
    - You will need to install `dotnet3.8` in BizHawk's prefix for the program to run.

- Z5Client
  - Z5Client is an Electron program, but the patching utility currently does not support Linux. It is recommended that you run Z5Client in WINE.

- Games
  - Some games may require some additional setup to get them or their mods working in Linux. This may involve using and configuring WINE.
    - Subnautica: ```winhttp.dll``` must be set to native in Subnautica's WINE prefix to load mods.
    - Super Mario 64 EX: Only the manual build is supported. The official guide for this game has Linux instructions.
    - VVVVVV: Must be run in WINE or built from source manually.