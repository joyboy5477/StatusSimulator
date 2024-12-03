from flask import Flask, jsonify, request
import random
import time
import threading
import uuid
import os
import logging

# Set up llogger
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = Flask(__name__)

# Thread-safe job storage
jobs = {}
jobs_lock = threading.Lock()


def process_job(job_id, delay):
    time.sleep(delay)
    result = random.choice(["completed", "error"])
    with jobs_lock:
        jobs[job_id]['status'] = result
    message = f"Job {job_id} processed with result: {result}"
    logging.info(message)
    print(message)  


@app.route("/start", methods=["POST"])
def start_job():
    try:
        min_delay = 5  # seconds
        max_delay = 10  # seconds
        delay = random.randint(min_delay, max_delay)

        job_id = str(uuid.uuid4())
        job_data = {
            "start_time": time.time(),
            "delay": delay,
            "status": "pending"
        }

        with jobs_lock:
            jobs[job_id] = job_data

        threading.Thread(target=process_job, args=(job_id, delay), daemon=True).start()

        message = f"Job {job_id} started with a delay of {delay} seconds"
        logging.info(message)
        print(message)  
        return jsonify({"message": "Job started", "job_id": job_id}), 202
    except Exception as e:
        message = f"Error in start_job: {e}"
        logging.error(message)
        print(message)  
        return jsonify({"error": "Failed to start job"}), 500


@app.route("/status", methods=["GET"])
def get_status():
    try:
        job_id = request.args.get('job_id')
        if not job_id:
            return jsonify({"error": "Job ID is required"}), 400

        with jobs_lock:
            job_data = jobs.get(job_id)

        if not job_data:
            return jsonify({"error": "Invalid Job ID"}), 404

        message = f"Job {job_id} status retrieved: {job_data['status']}"
        logging.info(message)
        print(message)  
        return jsonify({"result": job_data['status']})
    except Exception as e:
        message = f"Error in get_status: {e}"
        logging.error(message)
        print(message)  
        return jsonify({"error": "Failed to retrieve job status"}), 500


if __name__ == "__main__":
    print("Starting the Flask server...")  
    app.run(debug=True)
