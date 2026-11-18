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
    static int force_from = -1, force_to = -1, force_applied;
    static long force_frame;
    static unsigned dump_start, dump_end;
    static long dump_from = -1, dump_to = -1;
    static int p2_team[3] = {-1, -1, -1}, p2_applied;
    static long poke_frame = -1;
    static unsigned poke_address[8], poke_value[8], poke_count;
    uint8_t *ram;
    if (enabled < 0) {
        const char *option = getenv("KOF_REHEARSAL_LONE_ID");
        const char *force = getenv("KOF_REHEARSAL_FORCE");
        const char *dump = getenv("KOF_REHEARSAL_DUMP");
        const char *p2 = getenv("KOF_REHEARSAL_P2_TEAM");
        const char *poke = getenv("KOF_REHEARSAL_POKE");
        enabled = getenv("KOF_REHEARSAL_MONITOR") != NULL || option != NULL;
        if (force) {
            int from, to;
            if (sscanf(force, "%i:%i@%ld", &from, &to, &force_frame) < 3) force_frame = 0;
            if (sscanf(force, "%i:%i", &from, &to) == 2 && force_frame >= 0 &&
                from >= 0 && from <= 0x3e && to >= 0 && to <= 0x3e) {
                force_from = from;
                force_to = to;
                enabled = 1;
            } else fprintf(stderr, "[rehearsal] invalid force option\n");
        }
        if (p2) {
            int a, b, c;
            if (sscanf(p2, "%i,%i,%i", &a, &b, &c) == 3 && a >= 0 && a <= 0x3e &&
                b >= 0 && b <= 0x3e && c >= 0 && c <= 0x3e) {
                p2_team[0] = a;
                p2_team[1] = b;
                p2_team[2] = c;
                enabled = 1;
            } else fprintf(stderr, "[rehearsal] invalid P2 team option\n");
        }
        if (poke) {
            const char *cursor = strchr(poke, ':');
            long first = strtol(poke, NULL, 0);
            while (cursor && poke_count < 8) {
                unsigned address, value;
                int used;
                if (sscanf(cursor + 1, "%i=%i%n", (int *)&address, (int *)&value, &used) != 2 ||
                    address >= 0x10000 || value > 0xff) break;
                poke_address[poke_count] = address;
                poke_value[poke_count++] = value;
                cursor = strchr(cursor + 1 + used, ',');
            }
            if (first >= 0 && poke_count) {
                poke_frame = first;
                enabled = 1;
            } else fprintf(stderr, "[rehearsal] invalid poke option\n");
        }
        if (dump) {
            int start, end;
            long first, last;
            if (sscanf(dump, "%i-%i@%ld-%ld", &start, &end, &first, &last) == 4 &&
                start >= 0 && start < end && end <= 0x10000 && end - start <= 0x400 && first <= last) {
                dump_start = (unsigned)start;
                dump_end = (unsigned)end;
                dump_from = first;
                dump_to = last;
                enabled = 1;
            } else fprintf(stderr, "[rehearsal] invalid dump option\n");
        }
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
    if (force_from >= 0 && !force_applied && frame >= force_frame && ram[0x7d0c] != 0xff &&
        (ram[0x7d0c] & 0x3f) == force_from && ram[0x7d0c] == ram[0x7d12]) {
        ram[0x7d0c] = ram[0x7d12] = (uint8_t)((ram[0x7d0c] & 0xc0) | force_to);
        force_applied = 1;
        fprintf(stderr, "[rehearsal-force] frame=%ld id=%02x\n", frame, force_to);
        fflush(stderr);
    }
    if (p2_team[0] >= 0 && !p2_applied && ram[0x7d0f] != 0xff && ram[0x7d10] != 0xff &&
        ram[0x7d11] != 0xff && !memcmp(ram + 0x7d0f, ram + 0x7d15, 3)) {
        int slot;
        for (slot = 0; slot < 3; slot++)
            ram[0x7d0f + slot] = ram[0x7d15 + slot] =
                (uint8_t)((ram[0x7d0f + slot] & 0xc0) | p2_team[slot]);
        p2_applied = 1;
        fprintf(stderr, "[rehearsal-p2] frame=%ld team=%02x,%02x,%02x\n", frame,
                ram[0x7d0f], ram[0x7d10], ram[0x7d11]);
        fflush(stderr);
    }
    if (frame == poke_frame) {
        unsigned index;
        for (index = 0; index < poke_count; index++) ram[poke_address[index]] = (uint8_t)poke_value[index];
        fprintf(stderr, "[rehearsal-poke] frame=%ld count=%u\n", frame, poke_count);
        fflush(stderr);
    }
    if (dump_from >= 0 && frame >= dump_from && frame <= dump_to) {
        static const char digits[] = "0123456789abcdef";
        char line[2 * 0x400 + 2];
        unsigned address, length = 0;
        for (address = dump_start; address < dump_end; address++) {
            line[length++] = digits[ram[address] >> 4];
            line[length++] = digits[ram[address] & 15];
        }
        line[length++] = '\n';
        fprintf(stderr, "[rehearsal-dump] %ld ", frame);
        fwrite(line, 1, length, stderr);
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
