# StatusSimulator

This project simulates a job processing system with a server that handles job requests and a client that interacts with the server to start jobs and retrieve their statuses. The logs for the server and client are stored in a logs folder for debugging purposes.


## Prerequisites
- Python 3.11.5 (recommended).
- Basic understanding of Python's virtual environment (venv).


## Getting Started
### 1. Clone the Repo
    ```
    git clone <repo link from above>
    cd <repo_directory>
    ```
### 2. Activate your environment
    ```
    python -m venv venv
    source venv/bin/activate   <!-- On mac/linux-->
    source venv\Scripts\activate  <!-- On Windows-->
    ```
### 3. Install python packages
    ```
    pip install -r requirements.txt
    ```
### 4. Setup .env file
    ```
    SERVER_URL="http://127.0.0.1:5000"
    ```
.env file should be in client folder
### 5. Project structure
    
├── client/
│   ├── client.py
│   └── .env
├── server/
│   ├── server.py
├── logs/
│   ├── client.log
│   ├── server.log
├── requirements.txt
└── README.md    

### 6. How to run it? 
- stay on statussimulator
- to run server : python/server/server.py
- to run client : python/client/client.py (In separate terminal)

The client will:

Start a job.
Poll the server for the job's status.
Log and display the final status of the job.


### 7. Errors logs
Logs are automatically saved to the logs folder for both the server and the client:

- Server Logs: Stored in server/logs/server.log.
- Client Logs: Stored in client/logs/client.log.