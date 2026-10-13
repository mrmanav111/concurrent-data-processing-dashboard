# Advanced Programming - Assessment 1 Starter Project

## Scenario
You have been given a partially completed **Concurrent Data Processing Dashboard**.
The program loads CSV files and calculates category totals. The supplied starter
version works, but it performs its processing synchronously in the GUI thread,
causing the interface to become unresponsive.

You must complete and improve the project in line with the official assessment brief.

## Supplied files
- `main.py` - application entry point.
- `app/main_window.py` - starter PyQt GUI.
- `app/data_processor.py` - supplied data loading/processing functions.
- `app/shared_state.py` - simple shared-state scaffold for the synchronisation task.
- `tests/test_template.py` - starter automated-test template.
- `data/` - supplied local CSV files.
- `.gitignore` - starter ignore file.
- `requirements.txt` - required Python packages.

## Getting started
1. Create/activate your Python environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`
4. Click **Load Data Folder** and select the supplied `data` folder.
5. Click **Start Processing** and observe the responsiveness problem.
6. Complete the tasks in the official assessment brief.

## Important
- Do not delete or rename the supplied data columns.
- You may reorganise the code into additional modules/classes where appropriate.
- You are expected to use Git during the assessment and create meaningful commits.
- The starter code is intentionally incomplete. TODO comments identify some, but not all, areas requiring work.
