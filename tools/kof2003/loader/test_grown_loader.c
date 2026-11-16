/*
 * Synthetic test of the graphics loader and the tile decoder at the grown
 * 128 MiB Graphics Set size (spec graphics-set-growth, issue 03).
 *
 * It uses no game data. It includes the toolkit's video.c so it can read the
 * decoder's private state; the toolkit is third-party code that stays under
 * private/ and is found through -I (see run_loader_test.py).
 *
 * Usage: test_grown_loader WORK_DIR   (WORK_DIR receives 80 MiB of temporary files, five 16 MiB pairs)
 */
#include "video.c"        /* toolkit src/: decode_sprites, s_spr, s_spr_tiles_mask */
#include "romload.h"      /* ng_load_crom */
#include <neogeorecomp/neogeo.h>

uint16_t lspc_vram[0x10000];
uint8_t  lspc_anim_counter;

#define MIB (1024u * 1024u)
#define PAIR_FILE_BYTES (8u * MIB)          /* 8 MiB per file, 16 MiB per pair */
#define ADDED_SPACE_TILE 0x80000u

static int s_failures;
#define CHECK(cond, msg) do { if (!(cond)) { fprintf(stderr, "FAIL: %s\n", msg); s_failures++; } \
                              else printf("ok:   %s\n", msg); } while (0)

static int write_file(const char *dir, const char *name, const uint8_t *data, size_t n) {
    char path[1024];
    snprintf(path, sizeof path, "%s/%s", dir, name);
    FILE *f = fopen(path, "wb");
    if (!f) return 0;
    int ok = fwrite(data, 1, n, f) == n;
    return fclose(f) == 0 && ok;
}

/* Pair i: file A is a pattern of 0x11 + i, file B of 0x22 + i, except where a
 * test marker is placed. */
static int make_pair(const char *dir, int i, const uint8_t *a_head, const uint8_t *b_head, size_t head) {
    char na[32], nb[32];
    snprintf(na, sizeof na, "syn-c%d-a.bin", i);
    snprintf(nb, sizeof nb, "syn-c%d-b.bin", i);
    uint8_t *a = malloc(PAIR_FILE_BYTES), *b = malloc(PAIR_FILE_BYTES);
    if (!a || !b) return 0;
    memset(a, 0x11 + i, PAIR_FILE_BYTES);
    memset(b, 0x22 + i, PAIR_FILE_BYTES);
    if (a_head) memcpy(a, a_head, head);
    if (b_head) memcpy(b, b_head, head);
    int ok = write_file(dir, na, a, PAIR_FILE_BYTES) && write_file(dir, nb, b, PAIR_FILE_BYTES);
    free(a); free(b);
    return ok;
}

static void fill_names(char names[8][2][32], int pairs) {
    for (int i = 0; i < pairs; i++) {
        snprintf(names[i][0], 32, "syn-c%d-a.bin", i);
        snprintf(names[i][1], 32, "syn-c%d-b.bin", i);
    }
}

static void decode_all(const uint8_t *crom, size_t size) {
    free(s_spr);
    decode_sprites(crom, size);
}

/* One decoded pixel of a tile, addressed as the renderer does (code masked). */
static uint8_t tile_pixel(uint32_t code, int y, int x) {
    return (s_spr + ((size_t)(code & s_spr_tiles_mask) << 8))[y * 16 + x];
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s WORK_DIR\n", argv[0]); return 2; }
    const char *dir = argv[1];

    /* Markers: first bytes of the first pair (tile 0) and of the fifth pair
     * (tile $80000). Tile 0 gets A0=0x00, B0=0xFF (A1=B1=0) -> colour 4 on the right half of row 0.
     * Tile $80000 gets A0=0xFF, B0=0xFF (A1=B1=0) -> colour 5 there. */
    static const uint8_t t0_a[4] = {0x00, 0x00, 0x02, 0x03}, t0_b[4] = {0xFF, 0x00, 0x06, 0x07};
    static const uint8_t t5_a[4] = {0xFF, 0x00, 0x0A, 0x0B}, t5_b[4] = {0xFF, 0x00, 0x0E, 0x0F};

    /* Files: four 16 MiB pairs fill 64 MiB; the fifth pair is the Added Space. */
    for (int i = 0; i < 5; i++)
        if (!make_pair(dir, i, i == 0 ? t0_a : i == 4 ? t5_a : NULL, i == 0 ? t0_b : i == 4 ? t5_b : NULL, 4)) {
            fprintf(stderr, "cannot write synthetic files in %s\n", dir);
            return 2;
        }

    ng_game_t g;
    memset(&g, 0, sizeof g);
    char names[8][2][32];
    fill_names(names, 5);
    for (int i = 0; i < 5; i++) { g.crom_pairs[i][0] = names[i][0]; g.crom_pairs[i][1] = names[i][1]; }

    /* ---- 128 MiB ---- */
    g.crom_size = 128u * MIB;
    uint8_t *crom = ng_load_crom(dir, &g);
    CHECK(crom != NULL, "128 MiB: five synthetic pairs load");
    if (!crom) return 1;

    /* Interleave: even byte from the first file of the pair, odd from the second. */
    size_t p5 = 64u * MIB;
    CHECK(crom[0] == 0x00 && crom[1] == 0xFF && crom[4] == 0x02 && crom[5] == 0x06,
          "128 MiB: pair 1 bytes interleave (even byte from file A, odd from file B)");
    CHECK(crom[16u * MIB] == 0x12 && crom[16u * MIB + 1] == 0x23 && crom[48u * MIB + 1] == 0x25,
          "128 MiB: pairs are laid end to end, 16 MiB apart");
    CHECK(crom[p5] == 0xFF && crom[p5 + 1] == 0xFF && crom[p5 + 4] == 0x0A && crom[p5 + 5] == 0x0E,
          "128 MiB: the fifth pair starts at byte 64 MiB, interleaved");
    CHECK(crom[p5 + 16u * MIB - 2] == 0x15 && crom[p5 + 16u * MIB - 1] == 0x26,
          "128 MiB: last two bytes of the fifth pair come from its files A and B");

    int zero = 1;
    for (size_t k = p5 + 16u * MIB; k < 128u * MIB; k++) if (crom[k]) { zero = 0; break; }
    CHECK(zero, "128 MiB: the part no file covers reads as zero");

    decode_all(crom, g.crom_size);
    CHECK(s_spr_tiles_mask == 0xFFFFFu, "128 MiB: tile mask has 20 bits");
    CHECK(tile_pixel(ADDED_SPACE_TILE, 0, 8) == 5, "128 MiB: tile $80000 is the tile at the first byte of the fifth pair");
    CHECK(tile_pixel(0, 0, 8) == 4, "128 MiB: tile 0 is the first pair's tile");
    CHECK(tile_pixel(ADDED_SPACE_TILE, 0, 8) != tile_pixel(0, 0, 8), "128 MiB: tile $80000 differs from tile 0 (no wrap)");
    int tail_zero = 1;
    uint32_t first_unfilled = (uint32_t)((p5 + 16u * MIB) / 128);
    for (int y = 0; y < 16 && tail_zero; y++)
        for (int x = 0; x < 16; x++) if (tile_pixel(first_unfilled, y, x)) { tail_zero = 0; break; }
    CHECK(tail_zero, "128 MiB: a tile in the uncovered part decodes as blank");
    free(crom);

    /* ---- 64 MiB: the wrap the growth ends ---- */
    memset(g.crom_pairs[4], 0, sizeof g.crom_pairs[4]);     /* the original four pairs only */
    g.crom_size = 64u * MIB;
    crom = ng_load_crom(dir, &g);
    CHECK(crom != NULL, "64 MiB: four synthetic pairs load");
    if (!crom) return 1;
    decode_all(crom, g.crom_size);
    CHECK(s_spr_tiles_mask == 0x7FFFFu, "64 MiB: tile mask has 19 bits");
    CHECK(tile_pixel(ADDED_SPACE_TILE, 0, 8) == tile_pixel(0, 0, 8) && tile_pixel(ADDED_SPACE_TILE, 0, 8) == 4,
          "64 MiB: tile $80000 wraps to tile 0");
    CHECK(tile_pixel(ADDED_SPACE_TILE + 1, 5, 3) == tile_pixel(1, 5, 3),
          "64 MiB: a tile number at or above $80000 wraps to the low half");
    free(crom);

    /* ---- the fifth pair does not fit the 64 MiB size ---- */
    g.crom_pairs[4][0] = names[4][0]; g.crom_pairs[4][1] = names[4][1];
    CHECK(ng_load_crom(dir, &g) == NULL, "64 MiB: a fifth pair is refused (it needs the grown size)");

    printf(s_failures ? "\n%d check(s) failed\n" : "\nall checks passed\n", s_failures);
    return s_failures ? 1 : 0;
}
