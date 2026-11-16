/*
 * added_space_proof.c - plants one sprite that points at the first tile of the
 * Added Space (graphics-set growth, ticket 04).
 *
 * Build C only. The CMake option KOF2003_ADDED_SPACE_PROOF adds this file to the
 * player and defines the macro of the same name, which is what makes the renderer
 * call kof2003_plant_added_space_sprite() before it draws a line. Builds A and B
 * have neither the file nor the macro.
 *
 * The game rewrites sprite memory every frame, so one write at start-up would be
 * gone by the time anything is drawn: everything below is written again before
 * each line. The palette entries go with it, because a tile drawn in colours the
 * game happens to have left in that palette could be invisible.
 */
#include <stdint.h>

/* The runtime's video memory and its palette port. Declared here instead of
 * included, so this file copies none of the toolkit's code. */
extern uint16_t lspc_vram[0x10000];
void pal_write(uint32_t addr, uint16_t value);

/* The last of the 381 sprites: it is drawn over the others, and no later sprite
 * can carry the sticky bit that would chain itself onto it. */
#define PROOF_SPRITE   380
#define PROOF_PALETTE  1          /* palette 1, pens 1..15 */
#define PROOF_TILE     0x80000u   /* the first tile of the Added Space */
#define PROOF_X        152        /* screen column of the sprite's left edge */
#define PROOF_Y        96         /* screen row of its top edge */
#define FIRST_VISIBLE  16         /* the first scanline the screen shows */
/* The BIOS tests video memory and palette RAM while the board boots: it writes a
 * pattern, reads it back, and stops if what it reads differs. Planting during that
 * test leaves the game on a blank screen, so nothing is planted before this frame,
 * which is late enough for the attract mode to be running. */
#define PROOF_FIRST_FRAME 1000
#define LINES_PER_FRAME   224     /* visible lines, i.e. calls to this function */

void kof2003_plant_added_space_sprite(void) {
    static uint64_t lines;
    if (++lines <= (uint64_t)PROOF_FIRST_FRAME * LINES_PER_FRAME) return;
    uint32_t scanline = PROOF_Y + FIRST_VISIBLE;
    /* SCB2: vertical shrink $FF and horizontal shrink $F, i.e. no shrink at all. */
    lspc_vram[0x8000 + PROOF_SPRITE] = 0x0FFF;
    /* SCB3: the sprite's screen position counts down from $200, and the low six
     * bits are its height in tiles. One tile tall, and not sticky. */
    lspc_vram[0x8200 + PROOF_SPRITE] = (uint16_t)(((0x200u - scanline) << 7) | 1u);
    /* SCB4: the column, in the top nine bits. */
    lspc_vram[0x8400 + PROOF_SPRITE] = (uint16_t)((uint32_t)PROOF_X << 7);
    /* The sprite's tile list: 64 words per sprite, a tile number and its
     * attributes per tile. The tile number's low 16 bits are the first word; bits
     * 16-19, which only a grown Graphics Set can reach, come from attribute bits
     * 4-7. No auto-animation bits and no flip, so what is drawn is this tile. */
    uint32_t list = (uint32_t)PROOF_SPRITE << 6;
    lspc_vram[list] = (uint16_t)(PROOF_TILE & 0xFFFFu);
    lspc_vram[list + 1] = (uint16_t)((PROOF_PALETTE << 8) | ((PROOF_TILE >> 12) & 0xF0u));
    /* The same words added_space_tiles.ng_colour() writes out: four high bits per
     * gun, no dark bit, so the fifteen pens are distinct and none is black. */
    for (uint32_t pen = 1; pen < 16; pen++)
        pal_write((PROOF_PALETTE * 16u + pen) * 2u,
                  (uint16_t)((pen << 8) | ((15u - pen) << 4) | ((7u * pen) % 16u)));
}
