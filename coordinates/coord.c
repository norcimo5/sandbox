#include <stdio.h>
#include <stdint.h>

typedef union {
    struct {
        uint16_t y;
        uint16_t x;
    };
    uint32_t offset;

} coord_t;

int main(void) {
    coord_t point = { 65534, 65535 };

    printf("(%d, %d) = %X\n", point.x, point.y, point.offset);
    return 0;
}
