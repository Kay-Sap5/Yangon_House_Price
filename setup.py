from setuptools import setup,find_packages
import os

def get_requires(file_path):
    with open(file_path,'r') as file:
        lst = list(file.readlines())
        
        lst = [i.strip() for i in lst]

        if '-e .' in lst:
            lst.remove('-e .') 
        return lst

setup(
        name='Yangon House Price',
        version='0.0.1',
        description="""
                    This is the House Price Prediction Project , Based on the real world data , the data is from Shweproperty house 
                    selling website.
            """,
        author="Kay Sap Bhetwal",
        author_email="tboy4198@gmail.com",
        packages=find_packages(),
        install_requires=get_requires('requirements.txt')
)