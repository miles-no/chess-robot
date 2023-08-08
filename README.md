# Set up

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

**Windows:**

```
pip install virtualenv
python -m virtualenv --python C:\Path\To\Python\python.exe venv
.\venv\Scripts\activate
```

To deactivate:

```
venv\scripts\deactivate
```

**MAC:**

```
pip install virtualenv
```

```
virtualenv venv
```

or

```
python -m virtualenv venv
```

```
source venv/bin/activate
```

To deactivate:

```
deactivate
```

### Install requirements

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

```
createuser username --createdb

psql postgres -c "CREATE ROLE username WITH LOGIN PASSWORD 'password'; ALTER ROLE username CREATEDB;"

psql postgres -c "CREATE DATABASE databasename;"

psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE databasename TO username;"
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

In backend terminal:

```
cd backend
python server.py
```

In frontend terminal:

```
cd frontend
npm start
```
