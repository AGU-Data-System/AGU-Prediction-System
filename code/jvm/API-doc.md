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
      "temperatures": "temperatures",
      "previousConsumptions": "previousConsumptions"
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
      "temperatures": "temperatures",
      "previousConsumptions": "previousConsumptions",
      "coefficients": [1.0, 2.0, 3.0],
      "intercept": 1.0
    }
    ```

## Output Models

### Train

#### Prediction Output Model

- **Type:** `application/json`
- **Attributes:**
    - `training` (string): The training result.
- **Example:**
    ```json
    {
      "training": "training"
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
      "prediction": "prediction"
    }
    ```
