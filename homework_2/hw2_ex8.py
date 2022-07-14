from urls import API_LONGTIME_JOB
from time import sleep
import requests

# Arrange: create a task
task_response_obj = requests.get(API_LONGTIME_JOB).json()

token = task_response_obj["token"]
seconds = task_response_obj["seconds"]
request_data = {"token": token}

task_not_ready_obj = requests.get(API_LONGTIME_JOB, params=request_data).json()

# Check if task is not ready
not_ready_status = "Job is NOT ready"
assert task_not_ready_obj[
           "status"] == not_ready_status, f"{task_not_ready_obj['status']} should equal {not_ready_status}"

sleep(seconds)

# Request task after it's completed
task_after_wait_obj = requests.get(API_LONGTIME_JOB, params=request_data).json()

# Check if task status is ready and result is present in the response
ready_status = "Job is ready"
assert task_after_wait_obj[
           "status"] == ready_status, f"{task_after_wait_obj['status']} should equal {ready_status}"
assert task_after_wait_obj["result"], "'result' field should be in response"

non_exist_token = "ashdjbqw1234"
data_with_non_exist_token = {"token": non_exist_token}
non_exist_task_obj = requests.get(API_LONGTIME_JOB, params=data_with_non_exist_token).json()

# Check if non-existing task was accessed
try:
    assert non_exist_task_obj[
               "error"] == "No job linked to this token", "'error' should equal 'No job linked to this token'"
except KeyError:
    print("'error' key is not present in response")
