# Life Safety System Prediction Model (Dummy Data Version)

This repository contains a simplified version of a real-life system used to predict **Life Safety Systems** (e.g., Fire Alarms, Fire Sprinklers) for fire departments. This version uses dummy data and generic file names but retains the core functionality of the prediction system.

## Overview

The **Life Safety System Prediction Model** is an AI-based tool designed to predict safety systems in various premises using machine learning and keyword-based rules. This simplified version is based on the actual model utilized by fire departments to automate the process of system type assignments, improving accuracy and efficiency in fire safety compliance.

The original version of this model processes real-world data and is capable of assigning various system types to buildings, enhancing reporting and compliance for fire inspections.

## How It Works

This script uses a pre-trained machine learning model to predict safety system types based on the "Business Name" or "Premise Name" column from an Excel file. The model combines machine learning predictions with keyword-based rules to make its assignments.

### Workflow:
1. **Data Input**: The script reads a file named `input_data.xlsx`, containing business or premise names.
2. **Model Prediction**: The script uses the pre-trained model to make system type predictions.
3. **Keyword Rules**: It applies a set of keyword-based rules to ensure certain premises (like restaurants or schools) are assigned relevant system types.
4. **Output**: Predictions are saved to `output_predictions.xlsx` along with confidence scores for each prediction.

## Requirements

- Python 3.x
- Required Libraries: `pandas`, `joblib`, `openpyxl`

Install the required libraries with:

```bash
pip install pandas joblib openpyxl
