# AI Reflections

## Positive Experience
I was really impressed the first time I used Gemini. I wanted it to simplify the book I was reading so I uploaded the entire PDF onto it and had it create a side by side translation into simple English and because of that I was able to better understand the concepts and themes the author was trying to convey.
## Negative Experience
I tried having Deepseek solve some issues on my Unity project last semester and it lead me around a loophole where it never solved my problem but instead increased the complexity of it. I was trying to have it so that when the player clicked with their mouse it would trigger a sound.
## Class Discussion notes
During the previous lesson, we shared our presentations about our selected AI song contestants. It was interesting that some of the artists we chose had very technical approaches to using AI (for example, mine or Shao's) where there were many ways of utilizing them, whereas a couple of us (David, Henry) stuck with commercial AI tools with straightforward approaches to them.
## Takeaways from discussion
Takeaway 1: Latent space is an area worth researching about throughout the semester, as this is the way GAN models generate new content. I think utilizing dependent local models to generate samples in music (like Sarah's Dj Swami or my Aiphex Twin song) is an ethical way of implementing AI into workflow.

Takeaway 2: I learnt that the order or arrangement of things when coding in tensors affects the results. For example, although 5 x 3 is the same as 3 x 5, (W1 @ input) is not the same as (input @ W1). This is because input and w1 are not single numbers, but grids where you are matching up the slots.

Takeaway 3: Similarly, with these three tensors, the number of brackets determines the shapes.

input = torch.tensor([ -1,   5,   3 ])
input = torch.tensor([[-1], [5], [3]])
input = torch.tensor([[-1,   5,   3]])

The first line would print a simple flat line with one set of brackets, whereas the second would print a column. The third line would be similar to the first line but with two sets of brackets.


## Aspiration
How can I teach AI to compose music?
How can I use AI to create code that generates music?
How do I create a workflow utilizing AI?

