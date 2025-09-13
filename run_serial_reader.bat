@echo off
echo Installing required packages...
pip install -r requirements_serial.txt

echo.
echo Starting ESP32 Serial Reader...
echo Make sure your ESP32 is connected via USB!
echo.
python serial_reader.py

pause
