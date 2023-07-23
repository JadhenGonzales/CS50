// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 9973;

// Hash table
node *table[N];

// Dictionary word count
int dictionary_words;

// Prototype
bool free_list(node *list);

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    node *cursor = table[hash(word)];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    long hash = 0;
    hash += ((toupper(word[0]) - 'A') * 37);

    if (word[1] != '\0')
    {
        hash += (abs(toupper(word[1]) - 'A') * 37 * 37);

        if (word[2] != '\0')
        {
            hash += (abs(toupper(word[1]) - 'A') * 37 * 37 * 37);
        }
    }

    int value = hash % 9973;
    return value;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // Initialize table
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // Try to open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return false;
    }

    // Add words from dictionary to hash table
    char c;
    int letter = 0;
    int hash_value;
    dictionary_words = 0;
    node *new_word;
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
            dictionary_words++;

            // add word to hash table
            hash_value = hash(new_word->word);
            new_word->next = table[hash_value];
            table[hash_value] = new_word;
        }
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return dictionary_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        if (!free_list(table[i]))
        {
            return false;
        }
    }
    return true;
}

bool free_list(node *l)
{
    // Base case
    if (l == NULL)
    {
        return true;
    }

    else
    {
        // Recursively free the rest of the list
        free_list(l->next);

        // Free the current node
        free(l);
    }
    return true;
}