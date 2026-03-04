# Lab 4 Documentation

## Study Process
I commented up the code for what I understood, and used AI chat agent to explain code I didn't quite understand. Lines I asked about are listed in this section, and the explanation in my words is in the Understanding Inventory section.

CHORDS = sorted(set(all_chords))
- set: creates a set of the data (removes duplicates)
- sorted: creates a new ordered list (eg ascending by number or alphabetical)

stoi = {chord: i for i, chord in enumerate(CHORDS)}
- dictionary comprehension

## Understanding Inventory

Load the data: store the csv in a pandas dataframe, re-save the chords column into lists split around the | character

Build the vocabulary: 
- create a new list all_chords, if a song contains a list of chords, concatenate them into the new list so that it is a list of all the chords in the dataset from all the songs back to back
- create a new list CHORDS of all unique chords in ascending order
- create a new int VOCABULARY_SIZE the number of unique chords
- create a dictionary stoi
    - chord: i is the actual mapping
    - for i, chord is like (i, chord)
    - enumerate returns pairs of index and the chord at that index
    - so it returns the chord and its index for the mapping
    - in other words, maps each chord to its index

Define Encoding Functions:
- encode
    - get index of each chord from dictionary
    - make a vector full of zeros the size of all unique chords
    - replace the vector position of the chord index with 1.0

- decode
    - get the indices of the max value of the vector (this will be the index of the chord in the list of unique chords)
    - returns the chord at that index

- encode_sequence
    - concatenates each one hot encoding into a new tensor and flattens it so it becomes 1 dimension

