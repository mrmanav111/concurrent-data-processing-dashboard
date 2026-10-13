

# Concurrent Data Processing Dashboard

A Python desktop application developed for **Advanced Programming – Assessment 1**.

The application loads records from CSV files, processes the data, calculates totals by category, and displays the results through a PyQt6 graphical user interface. Background processing is implemented using `QThread` so that the GUI remains responsive while processing is running.

## Features

- Load multiple CSV files from a selected folder
- Process CSV records and calculate category totals
- Calculate the overall grand total
- Display processing progress using a progress bar
- Run data processing in a background thread
- Keep the GUI responsive during processing
- Cancel processing while a job is running
- Display processing errors
- Clear processing results
- Thread-safe shared state using `threading.Lock`
- Automated testing with `pytest`

## Technologies Used

- **Python 3**
- **PyQt6** – graphical user interface
- **QThread** – background processing
- **pytest** – automated testing
- **CSV** – data input format
- **threading** – thread-safe shared state

## Project Structure

```text
Concurrent-Data-Processing-Dashboard/
│
├── app/
│   ├── __init__.py
│   ├── data_processor.py
│   ├── main_window.py
│   ├── shared_state.py
│   └── worker.py
│
├── data/
│   ├── records_1.csv
│   ├── records_2.csv
│   └── records_3.csv
│
├── tests/
│   └── test_template.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## How It Works

1. The user selects a folder containing CSV files.
2. The application loads the records from the CSV files.
3. The user starts the processing task.
4. The processing task runs in a background `QThread`.
5. Progress updates are sent back to the GUI.
6. The application calculates totals for each category.
7. The grand total is calculated.
8. The final results are displayed in the application.
9. The user can cancel the processing task if required.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

### 2. Open the project folder

```bash
cd YOUR-REPOSITORY
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

Run:

```bash
python main.py
```

The application window will open.

Select the supplied `data` folder using **Load Data Folder**, then click **Start Processing**.

## Running Tests

The project uses `pytest` for automated testing.

Run:

```bash
python -m pytest -v
```

The current test report contains **6 passing tests** covering normal cases, boundary cases, invalid input, CSV values, the supplied data total, and thread-safe shared state.

## Concurrency

The application uses PyQt6's `QThread` to move the processing work away from the main GUI thread.

This prevents the interface from becoming unresponsive while the application performs longer-running data processing.

The worker communicates with the GUI using PyQt signals:

- `progress` – sends processing progress
- `finished` – returns the completed summary
- `error` – reports processing errors
- `cancelled` – reports when processing has been cancelled

## Thread Safety

The `SharedState` class uses Python's `threading.Lock` to protect shared values.

This ensures that updates to the completed job counter and last status message are performed safely when accessed from different threads.

## Author

**Manav Devani**

BSc Computing Student

Advanced Programming – Assessment 1

## License

This project was created for educational and academic purposes.
