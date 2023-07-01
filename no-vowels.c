// Write a function to replace vowels with numbers
// Get practice with strings
// Get practice with command line
// Get practice with switch

#include <cs50.h>
#include <stdio.h>
#include <string.h>

string replace(string word);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./no-vowels word\n");
        return 1;
    }

    printf("%s\n", replace(argv[1]));
}

string replace(string word)
{
    for (int letter = 0, n = strlen(word); letter < n; letter++)
    {
        switch (word[letter])
        {
            case 'a':
                word[letter] = '6';
                break;

            case 'e':
                word[letter] = '3';
                break;

            case 'i':
                word[letter] = '1';
                break;

            case 'o':
                word[letter] = '0';
                break;

            default:
                break;
        }
    }
    return word;
}