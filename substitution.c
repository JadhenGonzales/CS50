#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

string encrypt(string key, string plaintext);
int check_alphabetic(string key);
int check_repeating(string key);

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
        // Check key length, alphabetic, non-repeating
        if (strlen(argv[1]) != 26 || check_alphabetic(argv[1]) || check_repeating(argv[1]))
        {
            printf("Key must contain 26 non-repeating alphabetic characters.\n");
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

int check_alphabetic(string key)
{
    int non_alphabetic = 0;
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        if (!isalpha(key[i]))
        {
            non_alphabetic = 1;
        }
    }
    return non_alphabetic;
}

int check_repeating(string key)
{
    int repeating = 0;
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        for (int j = i + 1, m = n; j < m; j++)
        if (key[i] == key[j])
        {
            repeating = 1;
        }
    }
    return repeating;
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