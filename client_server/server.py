from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict


from Data.interactor import DataLoader
from model.naive_bayes_model import Model
from model.prediction import Predict
import uvicorn

app = FastAPI()

trained_model = None
features = None
labels = None



@app.get("/train_model")
def train_model(file: str, file_type: str, classified: str):
    global trained_model
    global features
    global labels
    try:
        data_loader = DataLoader()
        data_loader.load_data(file, file_type)
        df = data_loader.get_df()
        if df is None:
            raise HTTPException(status_code=400, detail="Failed to load data — check file path and type")
        trained_model = Model(df, classified)
        trained_model.create_model()
        features = [str(f) for f in trained_model.features]
        labels = [str(l) for l in trained_model.labels]
        options = {}
        for feature in features:
            options[feature] = list(trained_model.model[feature].keys())
        return {
            "message": "Model trained successfully",
            "features": features,
            "labels": labels,
            "options": options
        }
    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


class PredictionRequest(BaseModel):
    row: Dict[str,str]



@app.post("/predict")
def predict(request: PredictionRequest):
    global trained_model
    if trained_model is None:
        raise HTTPException(status_code=400, detail="Model is not trained yet")

    prediction = Predict(trained_model)
    result = prediction.predict_row(request.row)
    return {"prediction": result}



if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
