import requests

def fetch_all_trains():
    url = "https://api-v3.amtraker.com/v3/trains"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve trains. Status code: {response.status_code}")
            return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

def fetch_train(train_id: str):
    train_number = train_id.split('-')[0]  # This gets '238' from '238-3'
    url = f"https://api-v3.amtraker.com/v3/trains/{train_number}"
    train_details = []  
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            train_data = response.json()  # Parse the JSON response

            if train_number in train_data:
                train_info = train_data[train_number][0]  
                
                # Check if the trainID matches
                if train_info.get('trainID') == train_id:
                    details = {
                        "trainNum": train_info.get('trainNum'),
                        "routeName": train_info.get('routeName'),
                        "trainID": train_info.get('trainID'),
                        "lat": train_info.get('lat'),
                        "lon": train_info.get('lon'),
                        "status": train_info.get('statusMsg'),
                        "stations": train_info.get('stations', [])
                    }
                    train_details.append(details)  # Append the details to the list
                else:
                    print(f"Train ID mismatch. Expected: {train_id}, Found: {train_info.get('trainID')}")
            else:
                print(f"No data found for Train Number: {train_number}.")
        else:
            print(f"Failed to retrieve train {train_number}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return train_details  # Return the list of train details

if __name__ == "__main__":
        
    all_trains = fetch_all_trains()

    empire_service_trains = []

    for train_id, train_info in all_trains.items():
        for train in train_info:
            if train.get('routeName') == "Empire Service":
                empire_service_trains.append({
                    "routeName": train['routeName'],
                    "trainNum": train['trainNum'],
                    "trainID": train['trainID']
                })

    if empire_service_trains:
        for train in empire_service_trains:
            print(f"\nFetching details for Train ID: {train['trainID']}")
            train_data = fetch_train(train['trainID'])

            if train_data:  # Check if train_data is not empty
                for t in train_data:
                    print(f"Train Number: {t['trainNum']}, Route Name: {t['routeName']}, Train ID: {t['trainID']}")
                    # Print station details if needed
                    for station in t['stations']:
                        print(f"  Station: {station['name']}, Status: {station['status']}")
            else:
                print(f"No details found for Train ID: {train['trainID']}.")
else:
    print("No Empire Service trains found.")