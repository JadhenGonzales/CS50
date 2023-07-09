#include <cs50.h>
#include <stdio.h>
#include <strings.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
int get_victory_strength(pair checked_pair);
bool check_trail(int checked, int loser);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // TODO
    for (int i = 0, n = candidate_count; i < n; i++)
    {
        if (strcasecmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // TODO
    // Loops over all preferences, adds 1 for every pairing
    for (int i = 0, n = candidate_count; i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            preferences[ranks[i]][ranks[j]] += 1;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    for (int i = 0, n = candidate_count; i < n; i++)
    {
        for (int j = i; j < n; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count += 1;
            }
            else if (preferences[i][j] < preferences[j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count += 1;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // TODO
    int choice;
    pair placeholder;
    for (int i = 0; i < pair_count; i++)
    {
        choice = i;
        for (int j = i + 1; j < pair_count; j++)
        {
            if (get_victory_strength(pairs[j]) > get_victory_strength(pairs[i]))
            {
                choice = j;
            }
        }
        if (choice != i)
        {
            placeholder = pairs[i];
            pairs[i] = pairs[choice];
            pairs[choice] = placeholder;
        }
    }
    return;
}

// Get by how much winner wins
int get_victory_strength(pair checked_pair)
{
    return preferences[checked_pair.winner][checked_pair.loser];
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // TODO
    for (int i = 0; i < pair_count; i++)
    {
        if (check_trail(pairs[i].winner, pairs[i].loser))
        {
        locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
    return;
}

// Check if the pair will create a cycle
bool check_trail(int checked, int loser)
{
    // If the initial (checked) is the same with the loser, a loop will be created
    if (loser == checked)
    {
        return false;
    }

    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[loser][i] == 1)
        {
            if (!check_trail(checked, i))
            {
                return false;
            }
        }
    }

    return true;

}

// Print the winner of the election
void print_winner(void)
{
    // TODO
    // Check which column in the locked array only contains zeroes
    bool contains_one;
    for (int locked_column = 0; locked_column < candidate_count; locked_column++)
    {
        contains_one = false;
        for (int locked_row = 0; locked_row < candidate_count; locked_row++)
        {
            if (locked[locked_row][locked_column] != 0)
            {
                contains_one = true;
            }
        }
        if (!contains_one)
        {
            printf("%s\n", candidates[locked_column]);
            return;
        }
    }
    return;
}