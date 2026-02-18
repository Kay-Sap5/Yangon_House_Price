from fastapi import FastAPI , HTTPException , APIRouter
from fastapi.responses import JSONResponse
from src.logging.logger import logging
from src.exception.exception import CustomException
from src.prediction.input_validation import InputValidation_Model
from src.prediction.prediction import Prediction
import sys
import pandas as pd

app = FastAPI()
prediction = Prediction()

@app.get("/")
def welcome():
    return {'message':'welcome from api'}

@app.post("/prediction")
def input(data : InputValidation_Model) -> dict:
    data_dict = data.model_dump(mode='python')
    df = pd.DataFrame([data_dict])
    y_pred = prediction.initiate_prediction(df)
    y_pred = round(y_pred[0],2)
    
    return JSONResponse(status_code=200 , content=({'Prediction':y_pred}))
    
