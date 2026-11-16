"""Reducing memory samples. Plain numbers, no process is started."""
import pytest

from match.memory_probe import summarize


def test_peak_comes_from_the_system_counter_when_polling_missed_it():
    report = summarize([100, 200, 300], peak_working_set=900, peak_commit=1200)

    assert report.peak_working_set == 900
    assert report.peak_commit == 1200


def test_peak_is_at_least_the_highest_sample():
    assert summarize([100, 700, 300], peak_working_set=500, peak_commit=0).peak_working_set == 700


def test_steady_is_the_median_of_the_second_half():
    # second half of [1000, 1000, 400, 500, 600, 900] is [500, 600, 900]
    report = summarize([1000, 1000, 400, 500, 600, 900], peak_working_set=1000, peak_commit=0)

    assert report.steady_working_set == 600
    assert report.samples == 6


def test_no_samples_is_an_error():
    with pytest.raises(ValueError, match="no samples"):
        summarize([], peak_working_set=0, peak_commit=0)
