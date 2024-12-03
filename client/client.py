import requests
import time
import os
import logging
from dotenv import load_dotenv

# Loading env variables
load_dotenv()

# logger
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/client.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class TranslationClient:
    def __init__(self, server_url, max_retries=10, backoff_factor=2, total_timeout=60):
        self.server_url = server_url
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.total_timeout = total_timeout
        self.job_id = None

    def start_job(self):
        try:
            response = requests.post(f"{self.server_url}/start")
            response.raise_for_status()
            data = response.json()
            self.job_id = data.get("job_id")
            if not self.job_id:
                raise ValueError("Job ID not returned by the server.")
            message = f"Job started with ID: {self.job_id}"
            logging.info(message)
            print(message) 
        except requests.exceptions.RequestException as e:
            message = f"Failed to start job: {e}"
            logging.error(message)
            print(message) 
            raise
        except Exception as e:
            message = f"Unexpected error in start_job: {e}"
            logging.error(message)
            print(message) 
            raise

    def get_job_status(self, callback=None):
        if not self.job_id:
            self.start_job()

        retries = 0
        delay = 1
        start_time = time.time()

        while retries < self.max_retries and (time.time() - start_time) < self.total_timeout:
            try:
                response = requests.get(
                    f"{self.server_url}/status",
                    params={"job_id": self.job_id}
                )
                response.raise_for_status()
                response_json = response.json()
                result = response_json.get("result")

                if callback:
                    callback(result)

                if result in ["completed", "error"]:
                    return result

                message = f"Job status: {result}. Retrying in {delay} seconds..."
                logging.info(message)
                print(message) 
                time.sleep(delay)
                delay *= self.backoff_factor
                retries += 1

            except requests.exceptions.RequestException as e:
                message = f"Request error: {e}"
                logging.error(message)
                print(message) 
                retries += 1
                time.sleep(delay)
                delay *= self.backoff_factor
            except Exception as e:
                message = f"Unexpected error in get_job_status: {e}"
                logging.error(message)
                print(message) 
                raise

        raise TimeoutError("Job did not complete within the allowed retries or timeout.")


def status_callback(status):
    message = f"Status updated: {status}"
    logging.info(message)
    print(message) 


if __name__ == "__main__":
    server_url = os.getenv("SERVER_URL", "http://127.0.0.1:5000")
    client = TranslationClient(server_url=server_url)

    try:
        result = client.get_job_status(callback=status_callback)
        message = f"Final job status: {result}"
        logging.info(message)
        print(message) 
    except Exception as e:
        message = f"An error occurred: {e}"
        logging.error(message)
        print(message) 
