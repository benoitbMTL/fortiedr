import os
import json
import fortiedr
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ######################################################
#                LIST OF TEST CASES                    #
# ######################################################

test_cases = [
    #{"actions": "Block", "itemsPerPage": 5, "firstSeenFrom": "2024-02-25 18:32:21", "firstSeenTo": "2025-02-26 18:32:21"},
    #{"actions": "SimulationBlock", "firstSeenFrom": "2025-02-21 18:48:30", "firstSeenTo": "2025-02-26 18:48:30"},
    {"actions": "Block", "itemsPerPage": 2},
    {"actions": "SimulationBlock", "itemsPerPage": 2},
    #{"actions": "Log", "itemsPerPage": 2},
    #{"itemsPerPage": 2}  # No action filter, general event retrieval
]

def authenticate():
    """ Authenticate to FortiEDR using credentials from .env """
    authentication = fortiedr.auth(
        user=os.getenv("FORTIEDR_USER"),
        passw=os.getenv("FORTIEDR_PASS"),
        host=os.getenv("FORTIEDR_HOST"),
        org=os.getenv("FORTIEDR_ORG")
    )

    if not authentication['status']:
        print("Authentication failed:", authentication['data'])
        exit()

    return authentication

def execute_test_cases(method, test_cases):
    """ Execute a list of method.list_events() test cases """
    
    for i, params in enumerate(test_cases, 1):
        print("\n" + "#" * 60)
        print(f"#  TEST CASE {i}: EXECUTING")
        print("#" * 60)

        # Convert the dictionary to a string representing the executed function
        api_call_str = f"method.list_events({', '.join(f'{k}={repr(v)}' for k, v in params.items())})"

        print(f"\nExecuting: {api_call_str}\n")

        # Execute the request
        data = method.list_events(**params)

        if data['status']:
            # Filter the data to include only the required fields
            filtered_data = [
                {
                    "eventId": entry["eventId"],
                    "process": entry["process"],
                    "classification": entry["classification"],
                    "firstSeen": entry["firstSeen"],
                    "lastSeen": entry["lastSeen"],
                    "device": entry["collectors"][0]["device"] if entry["collectors"] else None,
                    "action": entry["action"]
                }
                for entry in data["data"]
            ]

            # Print formatted JSON output
            print("\nTest Case Result:\n")
            print(json.dumps(data))

        else:
            print("\nError fetching data.\n")

        print("\n" + "#" * 60)
        print(f"#  END OF TEST CASE {i}")
        print("#" * 60 + "\n")

def main():
    authentication = authenticate()
    print("Authentication successful!")

    method = fortiedr.Events()
    
    # Execute all test cases
    execute_test_cases(method, test_cases)

if __name__ == "__main__":
    main()
