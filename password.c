// Check that a password has at least one lowercase letter, uppercase letter, number and symbol
// Practice iterating through a string
// Practice using the ctype library

#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

bool valid(string password);

int main(void)
{
    string password = get_string("Enter your password: ");
    if (valid(password))
    {
        printf("Your password is valid!\n");
    }
    else
    {
        printf("Your password needs at least one uppercase letter, lowercase letter, number and symbol\n");
    }
}

// TODO: Complete the Boolean function below
bool valid(string password)
{
    bool contains_uppercase = false;
    bool contains_lowercase = false;
    bool contains_digit = false;
    bool contains_symbol = false;

    for (int i = 0, n = strlen(password); i < n; i++)
    {
        if (isupper(password[i]))
        {
            contains_uppercase = true;
        }
        else if (islower(password[i]))
        {
            contains_lowercase = true;
        }
        else if (isdigit(password[i]))
        {
            contains_digit = true;
        }
        else if (!isalnum(password[i]))
        {
            contains_symbol = true;
        }
    }
    if (contains_uppercase && contains_lowercase && contains_digit && contains_symbol)
    {
        return true;
    }
    else
    {
        return false;
    }
}
