# CS2 Round Win Predictor

## What I Would Like to Do

Build a neural network that predicts which team will win the current round in [CS2](https://www.counter-strike.net/cs2), from any point in a round. The model gets game data up to a point and outputs a win probability for each team. Then I will display the output on a local website to make it look pretty.

## How I Will Do It

### Data and Training

- parse pro CS2 demo files to extract tick by tick data for a given round using [awpy](https://github.com/pnxenopoulos/awpy) and [demoparser](https://github.com/LaihoE/demoparser)
- features to extract
  - players alive per team
  - HP and armor per team
  - equipment value and utility per team
  - bomb planted status and time since plant
  - Round time remaining
  - player positions
- encode each snapshot with the actual round winner
- train a Feedforward neural network on snapshots as a baseline, then look into LSTM or GRU

### Live Prediction

- use CS2's built-in [Game State Integration (GSI)](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration) to stream live match data as json to a local server
- feed incoming game state into the trained model and output a win probability
- push predictions to a web UI over WebSocket, rerunning the model with each new update so the display is constantly refreshing

### Tech I might use

- **Python** — model training with PyTorch, and demo parsing
- **[Elixir](https://elixir-lang.org/)** / **[Go](https://go.dev/)** — GSI server and WebSocket backend
- **[Liveview](https://github.com/phoenixframework/phoenix/tree/v1.8.5)** and **[D3.js](https://d3js.org/)** for live websocket UI and good looking graphs
  - inspo from [espn](https://www.espn.com/mens-college-basketball/game/_/gameId/401820778/duke-nc-state) for ui
- **[CounterStrike2GSI](https://github.com/antonpup/CounterStrike2GSI)** — reference for GSI interface to make my own (C# library)

## Questions, Concerns, and Stretch Goals

### Concerns

- I don't know how clean the match data is, and might need to clean it.
- don't know yet how to handle variable length rounds
- How do I parse the data and make it a uniform token
- I don't know how to actually set up a neural net with good hyperparams

### Questions

- what should my output look like, one scalar for win% or two, one for each team
- what models should I look at to use, and which ones are better
- where do I look to learn how to set up good models

### Stretch Goals

- Live data interpretation that auto updates, pulling from my game
- Live visual update on the web
- Live UI overlay that sits on top of CS2 using [Godot](https://godotengine.org/)
- Individual performance model
  - could update the model to understand more data and understand whether an individual player is going to get more kills this game or not
- Could make a cool top-down UI showing where players are
