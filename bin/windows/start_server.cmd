@echo off

echo Start MongoDB
start start_mongoDB

cd ../../src/
python -m app
