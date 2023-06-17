#include <cs50.h>
#include <stdio.h>

bool prime(int number);

int main(void)
{
    int min;
    do
    {
        min = get_int("Minimum: ");
    }
    while (min < 1);

    int max;
    do
    {
        max = get_int("Maximum: ");
    }
    while (min >= max);

    for (int i = min; i <= max; i++)
    {
        if (prime(i))
        {
            printf("%i\n", i);
        }
    }
}

bool prime(int number)
{
    // TODO
    int prime = 1;
    for (int factor = 2; factor < number; factor++)
    {
        if (number % factor == 0)
        {
            prime = 0;
        }
    }
    if (prime == 0)
    {
        return false;
    }
    else
    {
        return true;
    }
}
