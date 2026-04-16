# Lab 5

## The Algorithm

The algorithm I wanted to make was some sort of [cellular automaton](https://en.wikipedia.org/wiki/Cellular_automaton), but I didn't know exactly how I wanted to approach this, but I ended up wanting to do a game of life style thing, where you would apply it to a midi file and it would evolve one step on that midi, and also I wanted to make the x and y the pitch and time like it is usually displayed in things like Ableton or Reaper. Another thing I wanted to do is make it so you could apply this to only sections of the midi, and I recently learned how to use Ableton midi transformers in max and I liked this approach for this because it lets you edit midi in place rather than live and you could see the output visually. I also wanted it to transform the midi in the "scale space".

The algorithm is similar to [game of life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) but not exactly, its my own modification. This is how it works

1. Any "alive" 16th note that has fewer than 2 neighbors, gets deleted.
2. Any "alive" 16th note that has 2 or 3 neighbors, stays alive
3. Any "alive" 16th note that has more than 3 neighbors dies or gets deleted.
4. Any dead cell with exactly 3 or exactly 6 becomes alive.

The other rules include

1. If two or more 16th notes are next to each other, they get merged into one longer note so you don't get lots of repetition.
2. The grid resolution is half step or scale degree on the y axis, and 16th notes on the x axis

My difference, other than the notes specific stuff, is the addition of the 6 neighbors become alive, I thought this would make it so the grid is a lot less sparse, and that it could make things more interesting.

## Output Editing

The way that is works in Ableton, is that you can select any midi in a clip and click transform to go to the next iteration. So how the workflow worked, is I would draw a huge amount of random notes in the midi clip, then I would use cmd+a to select every midi note, then I would click generate on the midi transform 10 to 20 times, until I got some interesting looking midi and I would play it. Then, what I did is find midi that didn't sound too good, and only select that midi, and then I would only generate the next iteration on that selection until I got midi I liked.

For the drums, I generated a bunch of midi using this algorithm, then I listened to it and picked the best sounding midi, and just only used that stuff.

I also could select all the midi notes and duplicate them a bunch of times to make a huge amount of midi notes and then selected all of them to generate another interesting large amount of game of life style midi.

## Score to Audio

I kept my song to under 8 tracks, and what I did is find 8 sounds that I liked in the Ableton library and in my personal sound library that sounded interesting, and then I chose an interesting sound to make an introductory midi clip for and followed the workflow described in output editing, then I would add midi to a different instrument of the 8 that I selected.

