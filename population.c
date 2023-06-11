#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size

    int p;
    do
    {
        p = get_int("Start size: ");
    }
    while (p < 9);

    // TODO: Prompt for end size

    int f;
    do
    {
        f = get_int("End size: ");
    }
    while (f < p);

    // TODO: Calculate number of years until we reach threshold
    int t = 0;
    do
    {
        p = p + (p / 3) - (p / 4);
        t++;
    }
    while (p < f);

    // TODO: Print number of years
    printf("Years: %i\n", t);

}
