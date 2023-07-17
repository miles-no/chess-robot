#!/bin/bash

psql --version

brew install postgresql 

brew services start postgresql 

#psql postgres 


createuser postgres --createdb

psql postgres -c "CREATE ROLE chess WITH LOGIN PASSWORD 'moxonrobot123'; ALTER ROLE chess CREATEDB;"


psql postgres -c "CREATE DATABASE chess_db;"

psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE chess_db TO chess;"


