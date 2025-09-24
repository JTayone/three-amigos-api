# Three Amigos Trading API

A FastAPI-based backend system for algorithmic trading.  
It processes market data from CSV files, stores it in memory, and generates trading signals based on EMA (Exponential Moving Average) rules.  

This project was built as a technical test for the "Three Amigos" brokerage firm.

## 🚀 Features

- Upload CSV files containing trading bar data.
- Store data in memory as unique DataSeries (per Instrument + TimeFrame).
- Retrieve stored DataSeries in JSON format.
- Generate trading signals based on EMA9 and EMA21 comparisons.
- Mock email sending to demonstrate notifications.
- Graceful error handling and validation.

## 🛠 Tech Stack

- **Python 3.9+**
- **FastAPI** – API framework
- **Pydantic** – Data validation and modeling
- **Uvicorn** – ASGI server


## ⚙️ Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/JTayone/three-amigos-api.git
   cd three-amigos-api

2.Create a virtual environment and install dependencies:
  python -m venv venv
  source venv/bin/activate   # macOS/Linux
  venv\Scripts\activate      # Windows
  pip install -r requirements.txt

3. Run the API:
  uvicorn main:app --reload

4. Open your browser:
http://127.0.0.1:8000/docs


---

## 📌 API Endpoints

### 1. Load CSV
**POST** `/load_csv/`  
Uploads a CSV file and stores it as a DataSeries in memory.  

### 2. Get DataSeries
**GET** `/data_series/?instrument={instrument}&timeframe={timeframe}`  
Retrieves a stored DataSeries in JSON format.  

### 3. Generate Signal
**POST** `/generate_signal/`  
Checks for trading signals (Long/Short) based on EMA rules and simulates sending an email.  

## 📂 Example CSV Format

```csv
open,low,high,close,volume,ema9_value,ema21_value,bar_datetime
100,95,105,102,500,101,99,2025-09-23T10:00:00
102,96,106,104,600,103,100,2025-09-23T10:01:00

