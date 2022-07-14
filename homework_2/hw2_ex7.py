from urls import API_COMPARE_QUERY_TYPE
import requests

# 1. POST request without method
print("Task 1: POST request without method")
post_response = requests.post(API_COMPARE_QUERY_TYPE)
print(f"{post_response.status_code = }, {post_response.text = }\n")

# 2. PATCH request (not from the list of allowed methods)
print("Task 2: PATCH request (not from the list of allowed methods)")
patch_params = {"method": "PATCH"}
patch_response = requests.patch(API_COMPARE_QUERY_TYPE, data=patch_params)
print(f"{patch_response.status_code = }, {patch_response.text = }\n")

# 3. Correct request with method in params
print("Task 3: Correct request with method in params")
get_params = {"method": "GET"}
get_response = requests.get(API_COMPARE_QUERY_TYPE, params=get_params)
print(f"{get_response.status_code = }, {get_response.text = }\n")

# 4. Combinations of allowed methods and params
params_values = ["GET", "POST", "PUT", "DELETE"]

print("Task 4: Combinations of allowed methods and params")
print("GET request")
for value in params_values:
    params_for_test = {"method": value}
    get_response_1 = requests.get(API_COMPARE_QUERY_TYPE, params=params_for_test)
    print(f"Method value: {value}, {get_response_1.status_code = }, {get_response_1.text}")
print("\n")

print("POST request")
for value in params_values:
    params_for_test = {"method": value}
    post_response_1 = requests.post(API_COMPARE_QUERY_TYPE, data=params_for_test)
    print(f"Method value: {value}, {post_response_1.status_code = }, {post_response_1.text}")
print("\n")

print("PUT request")
for value in params_values:
    params_for_test = {"method": value}
    put_response = requests.put(API_COMPARE_QUERY_TYPE, data=params_for_test)
    print(f"Method value: {value}, {put_response.status_code = }, {put_response.text}")
print("\n")

print("DELETE request")
for value in params_values:
    params_for_test = {"method": value}
    delete_response = requests.delete(API_COMPARE_QUERY_TYPE, data=params_for_test)
    print(f"Method value: {value}, {delete_response.status_code = }, {delete_response.text}")

# Method value: GET, delete_response.status_code = 200, {"success":"!"} is invalid for DELETE method
