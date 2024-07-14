# AGU Prediction System

## Table of Contents

- [Introduction](#introduction)
- [API Endpoints](#api-endpoints)
    - [Train](#train)
        - [Train model](#train-model)
    - [Predict](#predict)
        - [Predict model](#predict-model)
- [Input Models](#input-models)
    - [Train](#train-1)
        - [Training Input Model](#training-input-model)
    - [Predict](#predict-1)
        - [Prediction Input Model](#prediction-input-model)
- [Output Models](#output-models)
    - [Train](#train-2)
        - [Training Output Model](#training-output-model)
    - [Predict](#predict-2)
        - [Prediction Output Model](#prediction-output-model)
- [Error Messages](#error-messages)
    - [Error Message](#error-message)

## Introduction

This document outlines the API endpoints and how to make requests to say API.
The API is a simple REST API that allows to train and make prediction models for gas consumption.
The API is divided into endpoints, each responsible for a different part of the system.
This API is also a part of the AGU Data System, which is a managing system for gas consumption data.

## API Endpoints

The API has the following endpoints:

### Train

#### Train model

- **URL:** `/api/train`
- **Method:** `POST`
    - **Request Body:**
        - `application/json`
            - [Training Input Model](#training-input-model)
- **Success Response:**
    - **Content:**
        - `application/json`
            - [Prediction Output Model](#prediction-output-model)
- **Error Response:**
    - **Content:**
        - `application/json`
            - [Error Message](#error-message)
- **Sample Call:**
    ```shell
    curl -X GET "http://localhost:8080/api/train" -H "accept: application/json"
    ```

### Predict

#### Predict model

- **URL:** `/api/predict`
- **Method:** `POST`
    - **Request Body:**
        - `application/json`
            - [Prediction Input Model](#prediction-input-model)
- **Success Response:**
    - **Content:**
        - `application/json`
            - [Prediction Output Model](#prediction-output-model)
- **Error Response:**
    - **Content:**
        - `application/json`
            - [Error Message](#error-message)
- **Sample Call:**
    ```shell
    curl -X GET "http://localhost:8080/api/predict" -H "accept: application/json"
    ```

## Input Models

### Train

#### Training Input Model

- **Type:** `application/json`
- **Attributes:**
    - `temperatures` (string): The temperatures for the prediction.
    - `previousConsumptions` (string): The previous consumptions for the prediction.
- **Example:**
    ```json
    {
      "temperatures": {"date": ["2024-07-03", "2024-07-04", "2024-07-05", "2024-07-06", "2024-07-07", "2024-07-08", "2024-07-09", "2024-07-10", "2024-07-11"], "minTemps": [16, 15, 17, 14, 13, 16, 15, 17, 14], "maxTemps": [24, 23, 22, 24, 25, 24, 23, 22, 24]},
      "consumptions": {"date": ["2024-07-03", "2024-07-04", "2024-07-05", "2024-07-06", "2024-07-07", "2024-07-08", "2024-07-09", "2024-07-10", "2024-07-11"], "consumption":[2,3,4,2,2,3,2,3,4]}
    }
    ```

### Predict

#### Prediction Input Model

- **Type:** `application/json`
- **Attributes:**
    - `temperatures` (string): The temperatures for the prediction.
    - `previousConsumptions` (string): The previous consumptions for the prediction.
    - `coefficients` (List<Double>): The coefficients for the prediction.
    - `intercept` (Double): The intercept for the prediction.
- **Example:**
    ```json
    {
      "temperatures": {
        "date": [
          "2024-07-03", 
          "2024-07-04", 
          "2024-07-05", 
          "2024-07-06", 
          "2024-07-07", 
          "2024-07-08",
          "2024-07-09", 
          "2024-07-10", 
          "2024-07-11",
          "2024-07-12",
          "2024-07-13",
          "2024-07-14",
          "2024-07-15",
          "2024-07-16"
        ],
        "minTemps": [
          16, 
          15, 
          17, 
          14, 
          13, 
          16, 
          15, 
          17, 
          14,
          13,
          16,
          15,
          17,
          14
        ], 
        "maxTemps": [
          24, 
          23, 
          22, 
          24, 
          25, 
          24, 
          23, 
          22, 
          24, 
          25, 
          24, 
          23, 
          22, 
          24
        ]
      },
      "consumptions": {
        "date": [
          "2024-07-03",
          "2024-07-04", 
          "2024-07-05", 
          "2024-07-06",
          "2024-07-07", 
          "2024-07-08", 
          "2024-07-09", 
          "2024-07-10", 
          "2024-07-11"
        ], 
        "consumption":[
          2,
          3,
          4,
          2,
          2,
          3,
          2,
          3,
          4
        ]
      },
      "coefficients": [
        2.398851648470614, 
        1.4125466531591617, 
        -0.042812821903454396,
        -0.22633592977142003
      ],
      "intercept": 9.127584881596157
    }
    ```

## Output Models

### Train

#### Training Output Model

- **Type:** `application/json`
- **Attributes:**
    - `training` (string): The training result.
- **Example:**
    ```json
    {
      "training": {
        "R^2 Score": 0.7601530334519065, 
        "coefficients": [
          2.398851648470614, 
          1.4125466531591617, 
          -0.042812821903454396, 
          -0.22633592977142003
        ], 
        "intercept": 9.127584881596157
      }
    }
    ```

### Predict

#### Prediction Output Model

- **Type:** `application/json`
- **Attributes:**
    - `prediction` (string): The prediction result.
- **Example:**
    ```json
    {
      "predictionList":[
        {"date":"2024-07-12","consumption":3.6529593847},
        {"date":"2024-07-13","consumption":2.4118422404},
        {"date":"2024-07-14","consumption":2.1143649309},
        {"date":"2024-07-15","consumption":3.3485495564},
        {"date":"2024-07-16","consumption":3.8915138116}
      ]
    }
    ```

### Error Messages

#### Error Message

- **Type:** `application/json`
    - **Attributes:**
        - `error` (string): The error message.
- **Example:**
  ```json
  {
    "error": "Error message"
  }
  ```