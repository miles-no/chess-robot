# Miles Chess Robot

- [Miles Chess Robot](#miles-chess-robot)
  - [Overview](#overview)
  - [Limitation](#limitation)
  - [Prerequisites](#prerequisites)
  - [System installation](#system-installation)
  - [Frontend](#frontend)
  - [Backend](#backend)
    - [Create a Virtual Python Environment](#create-a-virtual-python-environment)
    - [Install requirements](#install-requirements)
    - [Stockfish setup](#stockfish-setup)
    - [Database setup](#database-setup)
    - [Board setup](#board-setup)
- [Start application](#start-application)
- [Other information](#other-information)
    - [Deactivate virtualenv](#deactivate-virtualenv)
    - [Stop postgres server](#stop-postgres-server)


## Overview
This is an application that integrates robotics and chess. It utilizes a [uFactory Lite 6](https://www.ufactory.cc/lite-6-collaborative-robot/) robot arm and [Certabo chessboard](https://www.certabo.com/); a smart chessboard that uses RFID chips and LEDs to indicate what the chess engine has converged to as best move. The system uses [Stockfish](https://stockfishchess.org/) as chess engine to drive the robot's movement.  

>**Note** <br/> The uFactory robot and Certabo board is not originally compatible. This means that the original gripper may result in malfunctioning movement, due to various sizes and shapes of chess pieces.
> To remedy this custom made props including pieces and a 3D printed gripper extension are provided. 

## Limitation

As of now the board only allows for white to start at USB-side of the board. This means that the chosen color must be oriented towards the user by physically rotating the board. It's essential to ensure precise centering of the board for the robot to effectively handle the chess pieces. 

> **Piece placement** <br/> While playing, aim to position the pieces squarely in the middle of each chessboard square, maintaining an equal distance to all sides in the square.

>**Note** <br/> While playing make sure the side panels of the board remain free from pieces. This area is is used by the robot to store captured  pieces.

## Prerequisites
- Certabo chessboard.
- uFactory Lite 6 (with power supply).
- Emergency Stop button.
- PC or Tablet for Chess robot user interface.
- Ethernet cable (between robot and pc).
- USB cable (between chess board and pc).

## System installation
1. Press down the emergency stop button and connect this to the socket labeled **safety** on the backplane of the robot arm.
2. Attach the robot to a stable surface using the provided clamps.
3. Disconnect the AC lead in the power supply and connect the 24V connector to the socket labeled **ROBOT 24V** on the backplane of the robot arm.
4. Allign the board infront of the robot using the marks notated on the board, ensuring centering of the base of the robot and board.
5. Connect the ethernet cable from robot and the USB from the board to the computer.
6. Connect the power supply to a power source.  
7. Once plugged in and a beep sound is emitted, release the emergency stop button. 


> **CAUTION** <br/> The uFactory robot arm is strong and is suited for more than chess play and use various sensors to detect collision. <br/> <br/> However, as these collisions are occasionally identified with major delays, users have to be cautious when interacting with the robot. 
> >This collision sensivity can be altered through arm.set_collision_sensitivity(). 1-5, where 5 is most sensitive. 

## Frontend

Require `npm >= 9.5.1`

```
cd frontend
npm install
npm install --legacy-peer-deps
cd ..
```

## Backend

Require `Python >= 3.9.13` and `pip >= 23.2`

Install pip:

```
python install pip
```

### Create a Virtual Python Environment

```
cd backend
```

**MAC:**

```
pip install virtualenv
```

Create:

```
virtualenv venv
```

or

```
python -m virtualenv venv
```

Activate it:

```
source venv/bin/activate
```

**Windows:**

```
pip install virtualenv
python -m virtualenv --python venv
.\venv\Scripts\activate
```

### Install requirements

Make sure the virtualenv is activated before installing the requirements.

```
pip install -r requirements.txt
```

### Stockfish setup

Require `Stockfish`

**Installation for MAC:**

```
brew install stockfish
```

**Installation for Windows 64-bit:**

Install Stockfish for Windows 64-bit: https://stockfishchess.org/download/windows/

**Assign Stockfish Path:**

Create `config.py` in `/backend`.

Assign variable `STOCKFISH_PATH` to Stockfish installation location.

**Default path for MAC:**

`STOCKFISH_PATH = "/usr/local/opt/stockfish/bin/stockfish"`

or

`STOCKFISH_PATH = "/opt/homebrew/opt/stockfish/bin/stockfish"`

**Default path for Windows:**

Default path for Windows will be `stockfish-windows-x86-64.exe` location

### Database setup

Require `postgresql@14`

**Start postgres on MAC:**

```
brew services start postgresql@14
```

Check status

```
brew services
```

If error, check process for default port for postgresql, and terminate if in use, or change default port.
And then restart service.

```
brew services restart postgresql@14
```

**Start postgres on Windows:**

```
net start postgresql-x64-14
```

**To setup database for MAC and Windows**

Activate postgresql environment with user "postgres":

```
psql -U postgres
```

Run within psql environment:

```
CREATE ROLE username WITH LOGIN PASSWORD 'password'; ALTER ROLE username CREATEDB;

CREATE DATABASE databasename;

GRANT ALL PRIVILEGES ON DATABASE databasename TO username;
```

Create `database.ini` in `/backend/database` with the following content:

```
[postgresql]
host = localhost
database = databasename
user = username
password = password
```

### Board setup

Download Certabo board drivers from: https://www.certabo.com/download/

Follow the instructions provided on the download page.

For **Mac**, download `Certabo software - MAC OSx`.

For **Windows**, download `Certabo software – PC 4.1 – 64 bit`.

Within the `chess-robot` project folder in `/backend`, run the script and follow the instructions in the terminal

```
python setup.py
```

# Start application

Open two terminals, one for backend and one for frontend.

**In backend terminal:**

```
cd backend
```

Activate virtualenv

```
python server.py
```

**In frontend terminal:**

```
cd frontend
npm start
```

# Other information

### Deactivate virtualenv

**MAC:**

```
deactivate
```

**Windows**

```
venv\scripts\deactivate
```

### Stop postgres server

**MAC:**

```
brew services stop postgresql@14
```

**Windows:**

```
net stop postgresql-x64-14
```
