"""Exercise the development-only shortcut with invented RAM in a tiny player."""
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
MONITOR = ROOT / 'tools/kof2003/import_slot/rehearsal_monitor.c'
INCLUDE = Path(os.environ.get('NEOGEORECOMP_SOURCE',
                              ROOT / 'private/work/samsho-runtime-source/neogeorecomp')) / 'include'

HARNESS = r'''
#include <neogeorecomp/neogeo.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
static uint8_t ram[65536];
uint8_t *bus_wram(void) { return ram; }
void kof_rehearsal_monitor(long, const ng_input_t *);
int main(int argc, char **argv) {
    ng_input_t input = {0};
    int scenario = argc > 1 ? atoi(argv[1]) : 0;
    memset(ram, 0xff, sizeof(ram));
    ram[0x7d0c] = scenario == 2 ? 0x1e : 0x30;
    ram[0x7d0d] = 1; ram[0x7d0e] = 2;
    memcpy(ram + 0x7d12, ram + 0x7d0c, 3);
    if (scenario == 3) ram[0x7d14] = 0xff;
    kof_rehearsal_monitor(100, &input);
    if (scenario == 1) {
        return !(ram[0x7d0c] == 0x30 && ram[0x7d0d] == 0xff &&
                 ram[0x7d0e] == 0xff && ram[0x7d13] == 0xff && ram[0x7d14] == 0xff);
    }
    return !(ram[0x7d0d] == 1 && ram[0x7d0e] == 2 && ram[0x7d13] == 1);
}
'''


def test_shortcut_changes_only_a_complete_matching_team():
    compiler = shutil.which('clang')
    if not compiler or not INCLUDE.is_dir():
        pytest.skip('requires clang and the private runtime headers')
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temporary:
        source, player = Path(temporary) / 'player.c', Path(temporary) / 'player.exe'
        source.write_text(HARNESS)
        subprocess.run([compiler, '-I', str(INCLUDE), str(source), str(MONITOR), '-o', str(player)], check=True)
        base = {key: value for key, value in os.environ.items() if not key.startswith('KOF_REHEARSAL_')}
        subprocess.run([str(player), '0'], env=base, check=True, capture_output=True)
        enabled = dict(base, KOF_REHEARSAL_LONE_ID='0x30')
        for scenario in ('1', '2', '3'):
            subprocess.run([str(player), scenario], env=enabled, check=True, capture_output=True)
