#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get user name
    string name = get_string("What's your name: ");

    // Print Hello, name
    printf("hello, %s\n", name);
}