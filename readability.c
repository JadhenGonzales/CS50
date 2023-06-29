#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>


int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");
    // Coleman-Liau index
    // printf("Letters: %i\nWords: %i\nSentences: %i\n", count_letters(text), count_words(text), count_sentences(text));
    int index = (0.0588 * (count_letters(text) * 100.0 / count_words(text))) - (0.296 * (count_sentences(text) * 100.0 / count_words(text))) - 15.8;
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        index = round(index);
        printf("Grade %i\n", index);
    }

}


int count_letters(string text)
{
    int letter_count = 0;
    // check every character and count alphabetical characters
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letter_count++;
        }
    }
    return letter_count;
}


int count_words(string text)
{
    // word count starts at  because there is no space at the beginning of the first word
    int word_count = 1;
    // check every character and count blank spaces
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isblank(text[i]))
        {
            word_count++;
        }
    }
    return word_count;
}


int count_sentences(string text)
{
    int sentence_count = 0;
    // check every character and count punctuations
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentence_count++;
        }
    }
    return sentence_count;
}