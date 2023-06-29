#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

string encrypt(string key, string plaintext);

int main(int argc, string argv[])
{
    // Check user input.
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else
    {
        // Check key length.
        if (strlen(argv[1]) != 26)
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }
        else
        {
            // Ask user for plaintext the print ciphertext.
            string plaintext = get_string("plaintext: ");
            //printf("ciphertext: %s\n", plaintext);
            printf("ciphertext: %s\n", encrypt(argv[1], plaintext));
        }
    }
}

string encrypt(string key, string plaintext)
{
    string ciphertext = plaintext;
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        if (isupper(ciphertext[i]) && isalpha(ciphertext[i]))
        {
            ciphertext[i] = toupper(key[plaintext[i] - 65]);
        }
        else if (islower(ciphertext[i]) && isalpha(ciphertext[i]))
        {
            ciphertext[i] = tolower(key[plaintext[i] - 97]);
        }

    }
    return ciphertext;
}