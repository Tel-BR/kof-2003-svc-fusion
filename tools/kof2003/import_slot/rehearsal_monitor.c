/* Optional diagnostic output. The launcher must redirect stderr into private/. */
#include <neogeorecomp/bus.h>
#include <neogeorecomp/neogeo.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void kof_rehearsal_monitor(long frame, const ng_input_t *input)
{
    static int enabled = -1;
    static uint8_t previous[6];
    static uint8_t previous_hover;
    static int seen;
    static uint8_t last_input, last_start, last_coin;
    static int lone_id = -1, lone_applied;
    uint8_t *ram;
    if (enabled < 0) {
        const char *option = getenv("KOF_REHEARSAL_LONE_ID");
        enabled = getenv("KOF_REHEARSAL_MONITOR") != NULL || option != NULL;
        if (option) {
            char *end;
            long value = strtol(option, &end, 0);
            if (*option && !*end && value >= 0 && value <= 0x3e) lone_id = (int)value;
            else fprintf(stderr, "[rehearsal] invalid lone fighter option\n");
        }
    }
    if (!enabled) return;
    ram = bus_wram();
    if (lone_id >= 0 && !lone_applied && ram[0x7d0c] != 0xff &&
        (ram[0x7d0c] & 0x3f) == lone_id && ram[0x7d0d] != 0xff &&
        ram[0x7d0e] != 0xff && !memcmp(ram + 0x7d0c, ram + 0x7d12, 3)) {
        ram[0x7d0d] = ram[0x7d0e] = 0xff;
        ram[0x7d13] = ram[0x7d14] = 0xff;
        lone_applied = 1;
        fprintf(stderr, "[rehearsal-lone] frame=%ld\n", frame);
        fflush(stderr);
    }
    if (getenv("KOF_REHEARSAL_TRACE")) {
        const unsigned base = 0x1080;
        fprintf(stderr, "[rehearsal-frame] %ld %04x %04x %04x %04x\n", frame,
                (ram[base + 0x1e] << 8) | ram[base + 0x1f],
                (ram[base + 0x20] << 8) | ram[base + 0x21],
                (ram[base + 0x22] << 8) | ram[base + 0x23],
                (ram[base + 0x64] << 8) | ram[base + 0x65]);
    }
    if (!seen || input->p1 != last_input || input->start1 != last_start || input->coin1 != last_coin) {
        last_input = input->p1;
        last_start = input->start1;
        last_coin = input->coin1;
        fprintf(stderr, "[rehearsal-input] frame=%ld p1=%02x start=%u coin=%u\n",
                frame, last_input, last_start, last_coin);
        fflush(stderr);
    }
    if (!seen || memcmp(previous, ram + 0x7d0c, sizeof(previous)) != 0 ||
        previous_hover != ram[0x35b0] || frame % 600 == 0) {
        memcpy(previous, ram + 0x7d0c, sizeof(previous));
        previous_hover = ram[0x35b0];
        fprintf(stderr, "[rehearsal] frame=%ld team=%02x,%02x,%02x/%02x,%02x,%02x hover=%02x\n",
                frame, previous[0], previous[1], previous[2],
                previous[3], previous[4], previous[5], previous_hover);
        fflush(stderr);
        seen = 1;
    }
}
