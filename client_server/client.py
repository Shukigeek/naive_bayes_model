import requests

file = input("Enter file path: ")
file_type = input("Enter file type (csv/excel/json): ")
classified = input("Enter classified column name: ")

params = {
    "file": file,
    "file_type": file_type,
    "classified": classified
}

url = "http://127.0.0.1:8000/train_model"
response = requests.get(url, params=params)

if response.status_code == 200:
    response_data = response.json()
    print("✅ Model trained successfully!")
    print("📊 Features:", response_data["features"])
    print("🏷️ Labels:", response_data["labels"])
else:
    print(f"❌ Error {response.status_code}: {response.text}")
    exit()

# החיזוי
predict_data = {}
for feature in response_data["features"]:
    valid_values = response_data["options"].get(feature, [])

    while True:
        value = input(f"Enter value for '{feature}' (options: {valid_values}): ").strip().capitalize()
        if value in valid_values:
            predict_data[feature] = value
            break
        else:
            print(f"❌ Invalid value! Please choose from: {valid_values}")

url_predict = "http://127.0.0.1:8000/predict"
response_predict = requests.post(url_predict, json={"row": predict_data})

if response_predict.status_code == 200:
    prediction = response_predict.json()["prediction"]

    print("🔮 Prediction stats (in %):")
    total = sum(prediction.values())

    for label, prob in prediction.items():
        percentage = round(prob * 100 / total, 2)
        print(f"  {label}: {percentage}%")

    most_probable_label = max(prediction, key=prediction.get)
    print("✅ Most probable label:", most_probable_label)

else:
    print(f"❌ Error {response_predict.status_code}: {response_predict.text}")
