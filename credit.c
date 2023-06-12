#include <cs50.h>
#include <stdio.h>

string check_type(long n);
string check_validity(long n, string c);

int main(void)
{
    // get card number from user
    long card_number = get_long("Number: ");

    // check for possible card type
    string card_type = check_type(card_number);

    // check for card validity
    card_type = check_validity(card_number, card_type);

    printf("%s\n", card_type);
}



string check_type(long n)
{
    string s;
    // get last digits per card type
    long v = n / 1000000000000;
    long m = n / 100000000000000;
    long a = n / 10000000000000;
    // check for VISA 13- and 16-digit, start with 4
    if (v == 4 || v / 1000  == 4)
    {
        s = "VISA";
    }
    // check for MASTERCARD 16-digit, start with 51, 52, 53, 54, or 55
    else if (m == 51 || m == 52 || m == 53 || m == 54 || m == 55)
    {
        s = "MASTERCARD";
    }
    // check for AMERICAN EXPRESS 15-digit, start with 34 or 37
    else if (a == 34 || a == 37)
    {
        s = "AMEX";
    }
    else
    {
        s = "INVALID";
    }
    return s;
}



string check_validity(long n, string c)
{
    long d; // variable for each of the digits
    int sum;
    int t = 1;
    for (int i = 0; i < 16; i++)
    {
        d = (n / t) % 10;
        if (i % 2 == 1) // checks if i is an odd number
        {
            sum = sum + n;
        }
        else // if i is even we multiply by 2
        {
            sum = sum + (2 * n);
        }
        t = t * 10; // makes sure that we get the next digit for the next iteration
    }

    if (sum % 10 != 0)
    {
        c = "INVALID";
    }
    return c;
}