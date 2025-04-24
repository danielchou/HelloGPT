#include <stdio.h>

int main() {
    int i, j=0;
    printf("Starting loop...\n");
    for (i=0; i<128; i=i+j) {
        printf("Current values: i=%d, j=%d\n", i, j);
        j=i+1;
    }
    printf("Final values: i=%d, j=%d\n", i, j);
    printf("Press Enter to continue...\n");
    getchar();
    return 0;
}