# Project Notes

## The Plan

I wanted to build a live CS2 round win predictor like the chess.com win probability bar, but for Counter Strike. The idea was to train a few different models on historical round data or snapshots, and then run them against a live game to see which one predict best.

The original plan had three parts:

1. **Data pipeline**
    - An Elixir web crawler to download demo files from HLTV, parse them with the awpy library in Python, and extract features into a big CSV. I wanted to start this early and let it run for days with 15 minute gaps between downloads so I wouldn't get rate limited.
2. **Research**
    - A Jupyter notebook project to train and compare models (Random Forest, MLP, GRU, LSTM) with parameter sweeps and visualizations.
3. **Live server**
    - A Python server listening to CS2's Game State Integration, running all models on each game state update, with either a Phoenix LiveView frontend showing the predictions.

I also looked into using Broadway in Elixir for distributed async data processing with backpressure, but realized even though it would be so fun to do data pipelining, the bottleneck was rate limiting on downloads, not processing speed. So I just wrote a simple module that takes a demo file and appends the extracted data to a CSV.

## Data Collection

I set up the crawler and let it run. Ended up downloading about a terabyte of demo files. The pipeline would extract every feature I could possibly want and append it to a giant CSV, so I had about 1+ TB of data ready if I needed it.

But when I actually started training models, I realized I didn't need that much data and couldnt even use it if I wanted to. The models I was running weren't good enough to use the data i had. Early stopping was kicking in way before the models could use everything. The open source OpenML CS:GO dataset (122k rounds) turned out to be good enough for what I was doing. (But I'm not eniterly sure so I would like to look into why early stoping was kicking in so early)

I might come back to the big dataset later, for example, I could train individual models per map so each one gets map specific data, then route to the right model based on which map is being played.

## Learning about Features

This is when I did the most learning. I talked to some people at work who know more about ML than I do and I started to actually understand what features are conceptually.

I used to think features were just inputs to a neural net. My understanding now is that a feature is an attribute of a thing, like the definition of feature in plain english. In the MNIST handwriting project, one pixel is a feature of the image, a circle is a feature of the number nine, and in CS2, a team's total health is a feature of the round state.

To my understanding, features state facts. Weights state relationships between facts. and biases adjust those relationships (still need to build an intuition here). I also now know that there is explicit features (ones we define, like a pixil of a 100 by 100 image of a number) and implicit features (ones the model discovers during training like the circle of a nine). What's interesting is that ML is trying to find hidden relationships between features that we might not know about.

One thing I noticed is that having an AK on CT side correlates highly with winning, but what that's really saying is "if you have money, you're more likely to win." There's a lot of domain knowledge I could use to engineer better features. note: that's something I want to explore in the future.

## Understanding Gradient Descent

One thing I spent a lot of time on was understanding gradient descent. I didn't need to go this deep, but I got interested enough that I spent a long time watching 3Blue1Brown videos and reading PyTorch documentation. What I realized is that when training a model, you're not trying to find a local minimum because the gradient descent algorithm already does that automatically. What you're really trying to do is construct a model (a function) that has deep local minimums generaly. The architecture and features define the this "terrain" and gradient descent just finds one of the values in the landscape you give it.

## Understanding Models

Understanding Models was the worst part of my knowledge going in. I didn't know the specifics of how to implement models in PyTorch and I don't know Python as well as I know other languages.

The models I found and decided to compare were: Random Forest, MLP, GRU, LSTM. I also looked at K-means clustering early on but didn't end up using it or looking into it much. I watched a bunch of YouTube videos and read PyTorch docs on RNNs to understand GRU and LSTM conceptually. I also did an easyer Andrej Karpathy tutorial (the transformer one went over my head in quite a few areas).

I found an older project that used random forest and neural nets to predict round winners in CS:GO. It wasn't up to date, so I read through it, tryed to understand every line, and updated it to Pytorch. That taught me a lot. For example, I learned you can find correlations between features and outputs even without knowing the relationships, and sort by the most useful features.

I'm fully aware that because I'm still learning, a model performing poorly could be user error on my part rather than the model being bad for the task, but i was focusing on getting the plumbing working more than the models working the best they could.

## The GSI Issue

I wanted to test if I could get live data from CS2, so I made a quick Elixir web server to receive Game State Integration data. but the issue was that there are two versions of GSI. One for server owners/tournament organizers with full access to all player data, and one for regular players where you can't see enemy positions or weapons because that would be cheating or whatever lol.

So what I desided to do, was use a the CS2 built in HLTV match preview system made for esports presenters. You can watch any previous match with full data access because its acculy running a new game with the series of events and just running them in order. So I could use that to feed the prediction server with complete game state data. note: I'd want to see if I could train a model on only the data available to a player.

## Restarting

I started the project outside in by building the data pipeline first, then the live server stuff, then the models. This ate a lot of time before I had anything to show and left the hardest part for lator.

I restarted but this time inside out by understand the models first, train on literal random data that I put into a csv, then add real data, then add live data, then add ui. this was way easyer.

## The TUI

I originally wanted a Phoenix LiveView web interface, but while working on the python side I discovered pythons built in argparse library and the HTTP server framework, and that sounded way more fun because ive allready done a bunch of web stuff. I ended up making a live updating terminal UI instead of a web interface. It has a  bar showing all four models predictions side by side with a frame counter.

## Presentation Issues

I was running CS2 on my Windows desktop and sending GSI data over the local network to my MacBook running the python server. But for presenting, I needed everything on one machine that could screen share. Getting the python environment running on Windows was a bigger problem than expected.

## What I Built

- A python terminal app that listens to a running CS2 instance and predicts which side will win based on real time game data
- It runs four models simultaneously (Random Forest, MLP, GRU, LSTM)
- Four Jupyter notebooks that train and compare the models

## What I Learned

- How 3 different model work, how to impliment them, and what tasks they're good at
- How features, weights, and biases relate to each other conceptually
- How gradient descent actually works
- The python data science ecosystem, a bit of PyTorch, a small amount of scikit learn, and a little bit of pandas, matplotlib and Jupyter. I used to not like python but using Jupyter notebooks with pandas and PyTorch I get why its good now.
- The process of data science and how it differs from normal engineering. it's a lot more research and a lot less coding than I expected

## What I'd Do Differently

- Start inside out from day one and get a model working before building any code
- Spend more time on research and less on engineering. Once you have a model, implementing it is the easy part. That was one of the biggest mental hurdles I had with AI, and now that I've done it, I feel like I can start doing more interesting stuff on the model side
- Engineer better features using domain knowledge rather than just using raw game state data

## Future Ideas

- Finish the Phoenix LiveView web interface after I make it a bit better and find the model config that works the best
- Train models on only player accessible GSI data (not full tournament data)
- Train individual models per map and route predictions
- Handcraft better features
- Try the bigger dataset now that I understand the models better

## References

- [pnxenopoulos/awpy](https://github.com/pnxenopoulos/awpy)
- [scope.gg](https://scope.gg/), [refrag.gg](https://refrag.gg/), [csstats.gg](https://csstats.gg/)
- [3Blue1Brown](https://www.youtube.com/watch?v=aircAruvnKk&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)
- [machapraveen/csgo-round-winner-prediction](https://github.com/machapraveen/csgo-round-winner-prediction)
- [Andrej Karpathy -- Building makemore Part 2: MLP](https://www.youtube.com/watch?v=TCH_1BHY58I)
