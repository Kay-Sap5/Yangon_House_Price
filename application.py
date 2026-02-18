from fastapi import FastAPI , HTTPException , APIRouter
from fastapi.responses import JSONResponse
from src.logging.logger import logging
from src.exception.exception import CustomException
from src.prediction.input_validation import InputValidation_Model
from src.prediction.prediction import Prediction
from src.update_database.main import Run_Update_DataBase


import pandas as pd
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


def update_db():
        print("Updating Database")
        Run_Update_DataBase()
        
@asynccontextmanager
async def lifespan(app : FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_db , 'interval' , days = 2)
    scheduler.start()
    yield
    scheduler.shutdown() 

app = FastAPI(lifespan=lifespan)

prediction = Prediction()

@app.get("/")
def welcome():
    return {'message':'welcome from api'}

@app.post("/prediction")
def input(data : InputValidation_Model) -> dict:
    data_dict = data.model_dump(mode='python')
    df = pd.DataFrame([data_dict])
    y_pred = prediction.initiate_prediction(df)
    y_pred = round(float(y_pred[0]),2) 
    print(y_pred)
    return JSONResponse(status_code=200 , content={'Prediction':y_pred})    



        

