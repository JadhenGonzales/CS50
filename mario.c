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
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);
    return n;
}



void print_space(int l)
{
    for (int s = l-1; s > 0; s--)
    {
    printf(" ");
    }
}



void print_block(int h, int r)
{
    for (int b = r-1; b < h; b++)
    {
    printf("#");
    }
    printf("  ");
    for (int b = r-1; b < h; b++)
    {
    printf("#");
    }
    printf("\n");
}