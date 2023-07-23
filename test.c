#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>

#define LENGTH 45
#define DICTIONARY "dictionaries/small"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Dictionary word count
int dictionary_words;

bool load(const char *dictionary);

int main(int argc, char *argv[])
{
    if (argc != 2 && argc != 3)
    {
        printf("Usage: ./speller [DICTIONARY] text\n");
        return 1;
    }
    char *dictionary = (argc == 3) ? argv[1] : DICTIONARY;
    bool loaded = load(dictionary);

    node *ptr = malloc(sizeof(node));
    int num = 1;
    for (int i = 0; i < N; i++)
    {
        ptr = table[i];
        while (ptr != NULL)
        {
            printf("%i. %s\n", num, ptr->word);
            ptr = ptr->next;
            num++;
        }
    }
}

unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}


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
    node *new_word = malloc(sizeof(node));
    while (fread(&c, sizeof(char), 1, file) == sizeof(char))
    {
        // Copy until a word is formed
        if (c != '\n')
        {
            new_word->word[letter] = c;
            letter++;
        }
        else if (letter > 0)
        {
            new_word->word[letter + 1] = '\0';
            letter = 0;
            dictionary_words++;

            // add word to hash table
            hash_value = hash(new_word->word);
            new_word->next = table[hash_value];
            table[hash_value] = new_word;

            new_word = malloc(sizeof(node));
        }
    }
    fclose(file);
    return true;
}