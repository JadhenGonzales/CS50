#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

// Define BYTE, an 8-bit unsigned integer
typedef uint8_t BYTE;

// Create variable block_size
int block_size = 512;

bool is_jpeg(BYTE *b);

int main(int argc, char *argv[])
{
    // Check proper file usage
    if (argc != 2)
    {
        printf("Usage ./recover image\n");
        return 1;
    }

    // Open file
    FILE *infile = fopen(argv[1], "r");
    if (infile == NULL)
    {
        fclose(infile);
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }


    BYTE *buffer = malloc(block_size * sizeof(BYTE));
    char *file_name = malloc(8 * sizeof(char));
    int file_number = 0;
    bool writing = false;
    bool starting = false;
    bool new_jpeg;
    FILE *outfile;

    // Loop reading per 512 BYTES (placing them in buffer)
    // If a new start of jpeg is found
        // Start writing to a file named ###.jpg
        // If next BYTE does not contain jpg markers, continue writing
        // Else stop
        // exit ###.jpg

    while (fread(buffer, sizeof(BYTE), block_size, infile) == block_size)
    {
        new_jpeg = is_jpeg(buffer);

        if (writing && new_jpeg)
        {
            fclose(outfile);
            writing = false;
            file_number += 1;
        }

        if (writing && !new_jpeg)
        {
            fwrite(buffer, sizeof(BYTE), block_size, outfile);
        }

        if (!writing && new_jpeg)
        {
            writing = true;
            sprintf(file_name, "%03i.jpg", file_number);

            outfile = fopen(file_name, "w");
            if (outfile == NULL)
            {
                fclose(outfile);
                printf("Could not create %s.\n", file_name);
                return 2;
            }

            fwrite(buffer, sizeof(BYTE), block_size, outfile);
        }
    }
    free(buffer);
    fclose(infile);
    return 0;
}

bool is_jpeg(BYTE *b)
{
    // If first three BYTES are 0xff 0xd8 0xff and fourth BYTE is
    // 0xe0, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xeb, 0xec, 0xed, 0xee, or 0xef.
    // Put another way, the fourth BYTE’s first four bits are 1110.
    if (b[0] == 0xff && b[1] == 0xd8 && b[2] == 0xff && b[3] >= 0xe0 && b[3] <= 0xef)
    {
        return true;
    }
    return false;
}