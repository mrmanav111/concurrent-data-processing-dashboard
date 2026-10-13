"""Assessment 1 automated tests."""

import threading

import pytest

from app.data_processor import load_records, process_records
from app.shared_state import SharedState


def test_normal_case_example():
    """Normal case: several records in two categories are totalled correctly."""
    records = [
        {"category": "A", "value": 10.0},
        {"category": "A", "value": 5.0},
        {"category": "B", "value": 2.5},
    ]
    result = process_records(records)
    assert result["record_count"] == 3
    assert result["totals_by_category"]["A"] == 15.0
    assert result["totals_by_category"]["B"] == 2.5
    assert result["grand_total"] == 17.5


def test_boundary_case():
    """Boundary case: the smallest valid input is exactly one record."""
    progress_values = []
    records = [{"category": "A", "value": 0.0}]

    result = process_records(records, progress_callback=progress_values.append)

    assert result["record_count"] == 1
    assert result["totals_by_category"] == {"A": 0.0}
    assert result["grand_total"] == 0.0
    assert progress_values == [100]  # progress jumps straight to 100%


def test_invalid_case():
    """Invalid case: an empty list must raise a ValueError."""
    with pytest.raises(ValueError):
        process_records([])


def test_invalid_value_in_csv(tmp_path):
    """Invalid case: a non-numeric value in a CSV file must be rejected."""
    bad_file = tmp_path / "bad.csv"
    bad_file.write_text(
        "record_id,category,description,value\n"
        "X-001,Hardware,Bad row,not_a_number\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_records(tmp_path)


def test_supplied_data_grand_total():
    """Normal case with the real data: 45 records and the expected grand total."""
    records = load_records("data")
    assert len(records) == 45
    result = process_records(records)
    assert result["grand_total"] == pytest.approx(6092.21)


def test_shared_state_is_thread_safe():
    """Synchronisation: 10 threads x 1000 updates must give exactly 10000."""
    state = SharedState()

    def add_many():
        for _ in range(1000):
            state.mark_completed("done")

    threads = [threading.Thread(target=add_many) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert state.completed_jobs == 10000