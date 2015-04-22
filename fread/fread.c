#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

typedef unsigned char BYTE;

int file_exists(char *filename)
{
    struct stat buffer;   
    return (stat (filename, &buffer) == 0);
}

BYTE * mp_readFile(char * filename) {
    if (!file_exists("./testfile.txt")) {
        fputs("File does not exist!\n", stderr);
        return 0;
    }

    // OPEN FILE
    FILE *f = fopen(filename, "rb");
    BYTE *buf = {0};
    
    // GET FILE SIZE
    do {
        if(fseek(f, 0, SEEK_END) == 0) {
            long fsize = ftell(f);
            if (fsize <= 0 || fseek(f, 0, SEEK_SET) != 0)
                break;
        
            // ALLOCATE HEAP MEMORY TO FILE SIZE
            buf = malloc(sizeof(BYTE) * (fsize + 1));
            if (buf == NULL) {
                fputs("Error allocating memory!\n", stderr); 
                break;
            }
        
            if (fread(buf, fsize, 1, f) == 0) {
                fputs("Error reading file!\n", stderr); 
                free(buf);
                break;
            }
        }
    } while (0);
    
    fclose(f);
    return buf;
}

int main(void)
{
    BYTE * buf = mp_readFile("./testfile.txt");

    if (buf){
        printf("[%s]\n", buf);
        free(buf);
    }

    return 0;
}
