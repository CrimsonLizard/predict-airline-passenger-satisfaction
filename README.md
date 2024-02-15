Project Name: Airline Passenger Satisfaction Prediction

Data source - https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction
The result of the model deployment is here https://airline-passenger-satisfaction.onrender.com (The server is slow cause it's free, so please wait around 20-50 seconds).

This repository contains code for a machine learning project that predicts airline passengers' satisfaction based on a model trained on the Kaggle dataset. The project includes a Flask web application for deployment and utilizes Docker for easy hosting. Below is a brief overview of the project structure:

Model Deployment
  Folders:
    - static: Contains CSS styles for HTML pages.
    - templates: Includes HTML pages for the Flask web application.
    - tests: Holds tests for the predict.py file.

  Files:
    - Dockerfile: Configuration file for building a Docker image to deploy the Flask app.
    - flask_airline_best_model_12.02.2024.bin: Binary file containing the trained machine learning model.
    - predict.py: Implements the prediction logic, loading the model and generating outputs.
    - requirements.txt: Lists Python dependencies required for the app to run.
  
Model Training
  Folders:
    - data: Contains folders with train and test datasets from this resource - https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction

  Files:
   - Airline_Passenger_Satisfaction.ipynb: Jupyter notebook with the data analysis, feature engineering, and model training process.
    
README.md: This file (you're reading it).
