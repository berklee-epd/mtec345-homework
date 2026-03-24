# Lab 4: Neural Networks in PyTorch

## 1. Study Process Overview

[Describe how you used AI to study `nn_2.py`. What questions did you ask? What did it help you understand?]

I tried throwing the entire code into Gemini and although this was discouraged in the assignment and it wasn't specific in its answer, it did break down the code into each step, e.g. Step 1 was setting it up and loading the data, step 2 was teaching the AI to break the songs down into bite-size training examples using a "sliding window" approach. 

Of course, I wasn't fully satisfied with this so instead I placed each cell individually. This gave me more specific results and I was able to understand each step in more detail. For example, I ran step 1 through Gemini and here's what it said:

    This cell is where your program actually ingests the raw musical data and formats it into something Python can easily manipulate.

    Here is the line-by-line breakdown:

    Loading and Formatting the Data
    df = pd.read_csv("./billboard_numerals_simple.csv"):
    This line uses Pandas (pd) to read your CSV spreadsheet file. It takes all that data and stores it in a table structure called a DataFrame (abbreviated here as df).

    df["chords"] = df["chords"].str.split("|"):
    This is a crucial data-cleaning step. In your original CSV file, the chord progressions are likely saved as one long text string separated by vertical pipes (for example: "I|vi|IV|V"). This line tells Pandas to look at the "chords" column, find every pipe (|), and split the text apart into a clean Python list: ["I", "vi", "IV", "V"]. This is necessary because your neural network will need to look at chords as individual items, not one giant sentence.

    print(f"Loaded {len(df)} songs"):
    This simply counts the number of rows in your DataFrame (len(df)) and prints a message to the screen so you know exactly how many songs you are working with.

    df.head():
    This is a standard debugging command in data science. It prints out the first 5 rows of your DataFrame so you can visually verify that the data loaded correctly and the split operation worked exactly as you intended.

## 2. Understanding Inventory


### What I Understand

In the first step, the code opens the spreadsheet of songs and does some cleanup, putting them all into a DataFrame (df). It turns the squished-together chords (e.g. "I|vi|IV|V") and makes it neater in a Python list ( ["I", "vi", "IV", "V"] ) through Pandas. Pandas is basically an Excel but for Python. After doing this, it counts how many songs it found and shows the first five rows to show you what you're working with.

In the next step, the code dumps every chord into a giant pile. Afterwards, it removes all the duplicates and turns the remaining chords into a list. A specific ID number is then assigned to the number of each chord (e.g. "I" becomes 0, "IV" becomes 1) so the computer is able to proccess htem.

One-hot encoding is when the words are turned into numbers so a computer can understand them. You define the encode function, which will turn a chord like "I" into a long list of mostly 0s, with the exception of a "1" which acts like a flag to mark which specific chord it is. The decode function then does the exact opposite, translating the numbers back into string, before the encode_sequence function takes a 4-chord progression and glues all their flags into one sequence.

This is then followed by the creation of "flashcards". The AI takes the song's entire chord progression and turns the first 4 chords into a flashcard question, and the 5th chord into a flashcard answer. These pairs are saved, and it slides over one chord and repeats the proccess. This would turn a 100 chord song into 96 separate mini lessons. This proccess is then repeated over every single song in the spreadsheet until we have one giant deck of cards. It goes through each song to make sure that it has at least five chords, and then chops it up into a question and answer pair. Finally, a pile is made (all_pairs) and prints out the grand total of study material the AI has to work with.




### What I Don't Understand

[List specific parts that remain unclear. Include concrete questions. Write 2–3 sentences per gap.]

## 3. Model Limitations

[Identify at least 2–3 limitations. For each: name it, explain why it matters, and optionally suggest improvements. 2–3 sentences per limitation.]

Too predictable in chords. 

## 4. Improvement or Experiment

[Describe what you changed and what you learned. Write at least 2–3 full sentences.]

## 5. Creative Possibilities

[Describe at least one idea you would want to explore further.]
