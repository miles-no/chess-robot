# Set up

## Frontend

Require `npm`

```
cd frontend
npm install
npm install --legacy-peer-deps
cd ..
```

## Backend

Require `Python` and `pip`

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
virtualenv venv
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

### Board setup

Run the script and follow the instructions in the terminal

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
