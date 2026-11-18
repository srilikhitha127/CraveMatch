# CraveMatch quick start (Windows)

1. Extract the ZIP file.
2. Open the extracted `CraveMatch` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Run the following commands one by one:

```cmd
py -3.12 -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

5. Open `http://127.0.0.1:8000`.
6. Check `http://127.0.0.1:8000/health` to verify the API.

If `py -3.12` is not available, use `python -m venv venv` only if `python --version` reports Python 3.12.

To stop the server, press `Ctrl + C` in the terminal.
