/* Optional per-frame memory probe for the native player (ticket 08).
 *
 * Compiled into the private runtime copy only with the CMake option KOF2003_NATIVE_PROBE,
 * and called after each frame by the hook that probe_hook.py adds. Even then it does
 * nothing unless KOF_NATIVE_PROBE is set:
 *
 *   KOF_NATIVE_PROBE        "0xADDRESS:SIZE[,0xADDRESS:SIZE...]", SIZE 1, 2 or 4, up to 16
 *   KOF_NATIVE_PROBE_LOG    output file, one "<frame>\t<hex>\t<hex>..." line per frame
 *   KOF_NATIVE_PROBE_FIRST  optional first frame to log (default 0)
 *
 * The format matches probe.lua's PROBE_ADDRESSES mode and match/probe_log.py. Reads use
 * bus_peek16, which has no side effects and covers work RAM and NEO-PVC RAM, so the probe
 * cannot change the run. The log holds game memory: keep it under private/. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PROBE_MAX 16

uint16_t bus_peek16(uint32_t a); /* neogeorecomp/bus.h */

static uint32_t s_address[PROBE_MAX];
static int s_size[PROBE_MAX];
static int s_count;

static int parse(const char *text)
{
    const char *p = text;
    s_count = 0;
    for (;;) {
        char *end;
        unsigned long address;
        long size;
        while (*p == ' ') p++;
        if (p[0] != '0' || (p[1] != 'x' && p[1] != 'X') || s_count == PROBE_MAX) return 0;
        address = strtoul(p + 2, &end, 16);
        if (end == p + 2 || end - (p + 2) > 6 || *end != ':') return 0;
        size = strtol(end + 1, &end, 10);
        if ((size != 1 && size != 2 && size != 4) || (size > 1 && (address & 1))) return 0;
        s_address[s_count] = (uint32_t)address;
        s_size[s_count++] = (int)size;
        while (*end == ' ') end++;
        if (*end == '\0') return 1;
        if (*end != ',') return 0;
        p = end + 1;
    }
}

static uint32_t peek(uint32_t address, int size)
{
    uint16_t word;
    if (size == 4) return ((uint32_t)bus_peek16(address) << 16) | bus_peek16(address + 2);
    if (size == 2) return bus_peek16(address);
    word = bus_peek16(address & ~1u);
    return (address & 1) ? (word & 0xffu) : (uint32_t)(word >> 8);
}

void kof_native_probe(long frame)
{
    static enum { NOT_STARTED, OFF, LOGGING } state = NOT_STARTED;
    static FILE *log;
    static long first;
    int i;
    if (state == NOT_STARTED) {
        const char *spec = getenv("KOF_NATIVE_PROBE");
        const char *path = getenv("KOF_NATIVE_PROBE_LOG");
        const char *from = getenv("KOF_NATIVE_PROBE_FIRST");
        state = OFF;
        if (!spec) return;
        if (!parse(spec)) {
            fprintf(stderr, "[probe] invalid KOF_NATIVE_PROBE; nothing will be logged\n");
            return;
        }
        if (!path || !*path) {
            fprintf(stderr, "[probe] KOF_NATIVE_PROBE_LOG is not set; nothing will be logged\n");
            return;
        }
        first = from ? strtol(from, NULL, 10) : 0;
        log = fopen(path, "w");
        if (!log) {
            fprintf(stderr, "[probe] cannot write %s\n", path);
            return;
        }
        fprintf(stderr, "[probe] logging %d addresses from frame %ld\n", s_count, first);
        state = LOGGING;
    }
    if (state != LOGGING || frame < first) return;
    fprintf(log, "%ld", frame);
    for (i = 0; i < s_count; i++)
        fprintf(log, "\t%0*lx", 2 * s_size[i], (unsigned long)peek(s_address[i], s_size[i]));
    fputc('\n', log);
    fflush(log);
}
