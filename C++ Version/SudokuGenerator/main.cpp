#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <bits/stdc++.h>
#include <vector>
#include <array>
#include <random>
#include <algorithm>

using namespace std;

// Number of large squares in one side which is 3 for a standard sudoku
const int N = 3;
// Number of solutions which is valid for an answer
int solutions;
// grid of sudoku puzzle
int a[N*N][N*N];
// empty positions on the puzzle grid
vector<array<int, 2>> positions;
// shuffled numbers 1 to N^2 to use while creating puzzle
vector<int> sourceNumbers;


bool valid(int row, int col, int number)
{
    // checks if the number is valid for that position

    // same column
    for (int y = 0; y < N*N; y++)
        if (a[y][col] == number)
            return false;

    // same row
    for (int x = 0; x < N*N; x++)
        if (a[row][x] == number)
            return false;

    //same block
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            if (a[row-row%N+i][col-col%N+j] == number)
                return false;

    return true;
}

void solveForSolutions()
{
    // this function checks that how many solutions exist at the point it was called
    // after this function called solutions variable is either
    // 0 (which represents no solution exists),
    // 1 (only 1 solution exists),
    // 2 (more than 1 solutions exist).
    for (int row = 0; row < N*N; row++)
        for (int col = 0; col < N*N; col++)
            if (a[row][col] == 0){
                for (int number = 1; number <= N*N; number++)
                    if (valid(row, col, number)){
                        a[row][col] = number;
                        solveForSolutions();
                        a[row][col] = 0;
                        if (solutions > 1)
                            return;
                    }
                return;
            }

    solutions++;
}

bool solveForAnswer()
{
    // this function solves for the actual answer and sets the array variables as in the solution
    for (int row = 0; row < N*N; row++)
        for (int col = 0; col < N*N; col++)
            if (a[row][col] == 0){
                for (int number = 1; number <= N*N; number++)
                    if (valid(row, col, number)){
                        a[row][col] = number;
                        if (solveForAnswer())
                            return true;
                        a[row][col] = 0;
                    }
                return false;
            }
    return true;
}

void countSolutions()
{
    // updates number of solutions which is valid
    solutions = 0;
    solveForSolutions();
}

void show()
{
    // displays the puzzle
    cout << endl;
    for (int i = 0; i < N*N; i++){
        for (int j = 0; j < N*N; j++)
            cout << a[i][j] << " ";
        cout << endl;
    }
}

void shuffleSource()
{
    // shuffles source
    random_shuffle(sourceNumbers.begin(), sourceNumbers.end());
}

bool create()
{
    // this code creates the puzzle from an empty array until it has a unique solution
    countSolutions();
    if (solutions == 0) // if you want a hard puzzle just add => ( || N*N*N*N-positions.size() > [some number about 22])
        return false;
    else if (solutions == 1)
        return true;
    while (true){
        int posIndex = rand() % positions.size();
        array<int, 2> position = positions[posIndex];
        int positionY = position[0], positionX = position[1];
        positions.erase(positions.begin()+posIndex);

        shuffleSource();
        for (int number: sourceNumbers)
            if (valid(positionY, positionX, number)){
                a[positionY][positionX] = number;
                if(create())
                    return true;
                a[positionY][positionX] = 0;
            }
        positions.insert(positions.begin()+posIndex, position);
    }
}

void reset()
{
    for (int i = 0; i < N*N; i++){
        sourceNumbers.push_back(i);
        for (int j = 0; j < N*N; j++){
            a[i][j] = 0;
            positions.push_back({i, j});
        }
    }

    srand(unsigned(time(0)));

}

int main()
{
    reset();

    cout << "Creating Sudoku... (This process may take a while)" << endl << endl;
    create();
    countSolutions();

    cout << "Sudoku Puzzle: " << endl;
    if (solutions == 0) cout << "No Solution Exists." << endl;
    else if (solutions == 1) cout << "1 Solution Exists." << endl;
    else cout << "Several Solutions Exist." << endl;


    show();
    solveForAnswer();

    cout << endl << "Press Enter For Solution.";
    cin.get();

    show();


    return 0;
}
