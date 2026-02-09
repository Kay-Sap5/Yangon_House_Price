import os
import sys
import yaml
import numpy as np
from src.logging.logger import logging
from src.exception.exception import CustomException
import pickle

def load_yaml_file(file_path):
    try:
        with open(file_path , 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise CustomException(e,sys)
    
def write_yaml_file(file_path , dictionary):
    try:
        with open(file_path , 'w') as file:
             yaml.safe_dump(dictionary , file)
    except Exception as e:
        raise CustomException(e,sys)
    
def feature_detail_dict(train , test) ->dict:
    try:
        final = {}
        df = {'Train':train , "Test":test}
        for text , data in list(zip(list(df.keys()) , list(df.values()))):
            column = {}
            for i in data.columns:
                if data[i].dtype == 'str' or len(list(data[i].unique()))<=20:
                    ind = data[i].value_counts().index
                    val = data[i].value_counts()
                    temp_dict = dict(zip(ind,list(val)))
                    column[i]=(temp_dict)
                else:
                    ind = data[i].describe().index
                    val = data[i].describe()
                    print(val)
                    temp_dict = dict(zip(ind,val))
                    column[i]=(temp_dict)
                   
            final[text] = column
        return final
    except Exception as e:
        raise CustomException(e,sys)
    

def save_arr_to_npy(file_path , arr):
    try:
        os.makedirs(os.path.dirname(file_path) , exist_ok=True)
        with open(file_path , 'wb') as file:
            np.save(file , arr)
            logging.info("Complete Save Arr To Numpy File , Successfully....")
    except Exception as e:
        raise CustomException(e,sys)
    
def load_npy_file(file_path):
    try:
        with open(file_path , 'rb') as file:
            arr = np.load(file , allow_pickle=True)
        return arr
    except Exception as e:
        raise CustomException(e,sys)
    
def save_pkl_file(file_path , obj):
    try:
        os.makedirs(os.path.dirname(file_path) , exist_ok=True)
        with open(file_path , 'wb') as file:
            pickle.dump(obj , file)
    except Exception as e:
        raise CustomException(e,sys)

def load_pkl_file(file_path):
    try:
        with open(file_path , 'rb') as file:
            obj_file = pickle.load(file)
        return obj_file
    except Exception as e:
        raise CustomException(e,sys)


