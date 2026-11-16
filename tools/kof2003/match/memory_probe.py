"""Measure a Windows process's memory while it runs (graphics-set growth, ticket 02).

    run_measured(command, stream) -> MemoryReport

It polls the process's working set (RAM in use) and commit charge (memory the process
has asked the system to back), and keeps the system's own peak counters, so a short
spike between two polls is still counted. Windows only; it uses no extra packages.
"""
import ctypes
import statistics
import subprocess
import time
from ctypes import wintypes
from dataclasses import dataclass

MIB = 1 << 20


@dataclass(frozen=True)
class MemoryReport:
    peak_working_set: int  # bytes, highest RAM use
    peak_commit: int  # bytes, highest commit charge
    steady_working_set: int  # bytes, median RAM use over the second half of the run
    samples: int


def summarize(working_sets, peak_working_set, peak_commit):
    """Reduce polled samples. `steady` is the median of the second half of the run."""
    if not working_sets:
        raise ValueError("no samples; the process ended before it could be measured")
    half = working_sets[len(working_sets) // 2:]
    return MemoryReport(
        peak_working_set=max(peak_working_set, max(working_sets)),
        peak_commit=peak_commit,
        steady_working_set=int(statistics.median(half)),
        samples=len(working_sets))


class _Counters(ctypes.Structure):
    _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t),
                ("PrivateUsage", ctypes.c_size_t)]


def total_physical_memory():
    """Installed RAM in bytes (Windows)."""
    class Status(ctypes.Structure):
        _fields_ = [("dwLength", wintypes.DWORD), ("dwMemoryLoad", wintypes.DWORD),
                    ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
    status = Status()
    status.dwLength = ctypes.sizeof(Status)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
    return status.ullTotalPhys


def run_measured(command, stream, interval=0.05):
    """Run `command` to completion, raising if it fails; return its MemoryReport."""
    counters = _Counters()
    counters.cb = ctypes.sizeof(_Counters)
    query = ctypes.windll.kernel32.K32GetProcessMemoryInfo
    process = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT)
    handle = wintypes.HANDLE(int(process._handle))
    working_sets, peak_ws, peak_commit = [], 0, 0
    while process.poll() is None:
        if query(handle, ctypes.byref(counters), counters.cb):
            working_sets.append(counters.WorkingSetSize)
            peak_ws = max(peak_ws, counters.PeakWorkingSetSize)
            peak_commit = max(peak_commit, counters.PeakPagefileUsage)
        time.sleep(interval)
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, command)
    return summarize(working_sets, peak_ws, peak_commit)
