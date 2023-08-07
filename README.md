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
