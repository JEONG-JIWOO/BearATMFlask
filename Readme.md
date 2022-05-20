# Simple ATM service
Simple ATM service with Python Flask Server


# Features
1. Insert Card 
2. PIN number 
3. Select Account 
4. See Balance/Deposit/Withdraw


# Requirements

1. We may want to integrate it with a real bank system in the future
2. You don't need to implement any REST API, RPC, network communication etc, but just functions/classes/methods, etc.


# Install & Run

### Run ATM server

    docker-compose up

### Run Client_example

    python3 -m pip install requests
    python3 client_example.py

### Run Test

    python3 -m pip install requests
    python3 test.py


# Example code
Watch "client_example.py"



# Project Structure
   - app.py : main Flask Server code 
   - bankapi.py : Banking Api Code, For now it Works as Dummy 
   - test.py : unit test Module 
   - example.py : simple ATM client code