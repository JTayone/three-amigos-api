from fastapi import FastAPI, UploadFile, File, HTTPException, status
from datetime import date, datetime
from typing import Dict, Tuple
import csv
import io

# Import models from a separate file for better organization
from models import DataSeries, BarData, Instrument, TimeFrame, BarType

app = FastAPI()

# Explicitly type the dictionary for clarity
data_series_store: Dict[Tuple[str, str], DataSeries] = {}

# --- Helper Functions ---
def get_data_series_key(instrument_name: str, timeframe_name: str) -> Tuple[str, str]:
    """Generates a unique key for the data series store."""
    return (instrument_name, timeframe_name)

# --- API Endpoints ---

@app.post("/load_csv/")
async def load_csv(
    file: UploadFile = File(...),
    instrument_name: str = "TEST_INSTRUMENT",
    expiration_date: date = date(2025, 12, 31),
    tick_currency_value: float = 1.0,
    timeframe_name: str = "1min",
    bars_type: BarType = BarType.MINUTE,
    timeframe_value: int = 1
):
    """
    Loads a CSV file into a DataSeries object in memory.
    """
    try:
        content = (await file.read()).decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))
        bars = [BarData(**row) for row in reader]  # Shorter list comprehension

        if not bars:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CSV file contains no bar data.")

        series = DataSeries(
            instrument=Instrument(name=instrument_name, expiration_date=expiration_date, tick_currency_value=tick_currency_value),
            timeframe=TimeFrame(name=timeframe_name, bars_type=bars_type, value=timeframe_value),
            list_of_bars=bars,
            init_date=bars[0].bar_datetime.date(),
            end_date=bars[-1].bar_datetime.date()
        )

        key = get_data_series_key(instrument_name, timeframe_name)
        data_series_store[key] = series

        return {"message": f"CSV for {key} loaded successfully.", "bars_count": len(bars)}
    except Exception as e:
        print(f"Error loading CSV: {e}") # Print error for debugging
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error processing CSV file.")

@app.get("/data_series/")
async def get_data_series(instrument: str, timeframe: str):
    """
    Retrieves a DataSeries object from memory.
    """
    key = get_data_series_key(instrument, timeframe)
    series = data_series_store.get(key)
    
    if not series:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DataSeries not found.")
    
    return series

@app.post("/generate_signal/")
async def generate_signal(instrument: str, timeframe: str, bar_datetime: datetime):
    """
    Generates a trading signal and mocks sending an email to the console.
    """
    key = get_data_series_key(instrument, timeframe)
    series = data_series_store.get(key)
    
    if not series:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DataSeries not found.")

    matching_bar = next(
        (bar for bar in series.list_of_bars if bar.bar_datetime == bar_datetime), 
        None
    )

    if not matching_bar:
        return {"message": "Request processed, but no matching BarData was found.", "status_code": status.HTTP_202_ACCEPTED}

    if matching_bar.ema9_value > matching_bar.ema21_value:
        signal_message = f"Long Entry at price {matching_bar.close}"
    elif matching_bar.ema9_value < matching_bar.ema21_value:
        signal_message = f"Short Entry at price {matching_bar.close}"
    else:
        signal_message = "No signal generated."
        return {"message": signal_message}

    print(f"\n--- MOCK EMAIL ---")
    print(f"To: amx@global-ops.net")
    print(f"Subject: Trading Signal")
    print(f"Body: {signal_message}")
    print(f"------------------\n")

    return {"message": f"{signal_message} EMAIL OF SIGNAL SENT"}