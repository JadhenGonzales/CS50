#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>

#define LENGTH 45

typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

const unsigned int N = 997;
node *table[N];

unsigned int hash(const char *word);
bool load(void);

int main(void)
{

    bool loaded = load();
    return 0;
}

unsigned int hash(const char *word)
{
    long hash = 0;
    hash += ((toupper(word[0]) - 'A') * 37);

    if (word[1] != '\0')
    {
        hash += (abs(toupper(word[1]) - 'A') * 37 * 37);
    }

    int value = hash % 997;
    return value;
}

bool load(void)
{
    // Initialize table
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // Try to open dictionary
    FILE *file = fopen("dictionaries/small", "r");
    if (file == NULL)
    {
        printf("Could not open dictionary.\n");
        return false;
    }

    // Add words from dictionary to hash table
    char c;
    int letter = 0;
    int hash_value;
    node *new_word;
    int highest_hash = 0;
    while (fread(&c, sizeof(char), 1, file) == sizeof(char))
    {
        // Copy until a word is formed
        if (c != '\n')
        {
            if (letter == 0)
            {
                new_word = malloc(sizeof(node));
            }
            new_word->word[letter] = c;
            letter++;
        }
        else if (letter > 0)
        {
            new_word->word[letter] = '\0';
            letter = 0;

            // add word to hash table
            hash_value = hash(new_word->word);
            if (hash_value > highest_hash)
            {
                highest_hash = hash_value;
            }
            new_word->next = table[hash_value];
            table[hash_value] = new_word;
        }
    }
    fclose(file);
    printf("H_hash: %i\n", highest_hash);
    return true;
}