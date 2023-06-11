#include <cs50.h>
#include <stdio.h>

int get_height(void);
void print_space(int l);
void print_block(int h, int r);

int main(void)
{
    // ask user for the height of the pyramid
    int height = get_height();

    // print the pyramids
    for (int row = height; row > 0; row--)
    {
        print_space(row);
        print_block(height, row);
    }
}



int get_height(void)
{
    // get height between 1 and 8
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);
    return n;
}



void print_space(int r)
{
    // print spaces relative to row number
    for (int s = r - 1; s > 0; s--)
    {
        printf(" ");
    }
}



void print_block(int h, int r)
{
    // print first batch of hashtags based on row number
    for (int b = r - 1 ; b < h; b++)
    {
        printf("#");
    }

    printf("  ");

    // print second batch of hastags
    for (int b = r - 1; b < h; b++)
    {
        printf("#");
    }
    printf("\n");
}