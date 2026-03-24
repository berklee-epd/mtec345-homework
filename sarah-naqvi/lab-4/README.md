# Lab 4: Neural Networks in PyTorch

## 1. Study Process Overview

I started by trying to read through each line of code and I tried to see if I could get a general understanding of what each line was doing. If there was a particular line that I thought I knew what it's purpose was but I wasn't completely sure, I'd ask Gemini for confirmation. I found this to be quite helpful since even in those instances where maybe I sort of knew what the purpose of the code was, Gemini helped to clarify my understanding. In other instances, I would have no idea what certain lines were used for, in which case I'd also ask Gemini for an explanation. 

For example, an instance in which I was asking for confirmation included lines 87 and 88 in the code which are as follows: 
```
X = torch.stack([encode_sequence(inp) for inp, _ in all_pairs])
y = torch.tensor([stoi[tgt] for _, tgt in all_pairs])
```
I asked Gemini if the purpose of these lines of code is just making the tensors with the training pairs so the neural network can use the data and it responded back by agreeing and then giving a more in depth explanation. It explained that X is the inputs that is converting the list of chords into a mathematical matrix and Y is the targets. It also helped to clarify the specificity of the process by explaining that 'stoi[tgt]' looks up the integer ID for the chord, which I had not realized. 

I also liked the analogies used by Gemini to explain certain concepts. For example, I understood that the model needed training pairs and testing pairs but I wasn't certain I understood exactly what 'perm' and 'n-train' were in lines 90 and 91. Gemini helped me understand this concept by explaining it in terms of a deck of cards. It explained that 'perm' is shuffling the deck of cards, which is the data of songs, and 'n-train' is splitting the deck so that 80 percent is going to the train group and the rest is going to the test group. This makes sense since it si best to randomize the data the model is trained on in the case that the data is ordered, which would make it more difficult for the model to make predictions about all the songs if it is only trained on one artists' songs that are at the begining of the dataset. 

I found that Gemini wasn't too helpful with concepts that I didn't have a strong base understanding of. For concepts where I have some base knowledge or an idea of what the code is contributing, it was much easier for me to grasp the smaller details provided by Gemini. An instance when I had a much more difficult time with understanding Gemini's explaination was when I had asked about lines 195 to 197. 
```
mask = y_test == i
    if mask.sum() > 0:
        acc = (preds[mask] == y_test[mask]).float().mean().item()
```
Gemini was able to explain how these lines were calculating per-class accuracy to indicate the accuracy for predicting specific chords; however, its in depth explanation of how exactly the code was calculating this was very confusing to me. I still feel that I don't have a strong understanding of these lines of code work because I found the explanations to be a bit too surface level when explaining the syntax. I understand that the first line of code is a boolean tensor that is essentially filtering and isolating specific chord examples, but I don't really understand how that is being done by the assignment operators since Gemini only explained what individual components of the code such as '''mask''' means. But this isn't helpful when trying to understand and connect these lines of code together. 



## 2. Understanding Inventory

### What I Understand
#### Most of the Hyperparameters
I feel comfortable explaining what most of the hyperparameters are doing, especially since I learned about the main concept first from my research project. The window size is determining the number of chords the model is using to help it predict the target chord and this number is what the sliding window code is referring to later on in the code. Hidden dim is the number of nodes in the hidden layer of the model, similar to our class neural network diagram's nodes in the middle layer. The batch size is the number of groups of chord progressions the model is using and epochs are read throughs of all the data. 

#### One Hot Encoding 
I can explain how one hot encoding works and how it is being implemented by the code in step 2. Here, the chords are being turned into a list of zeros and the number 1 within that list of zeros is how that particular chord is identified. Then in the encode function, the 2D tensor is being flattened into a 1D tensor with all the chords represented in numbers so that they can be understood and used by the model. Then, in decode, the code is translating or decoding the tensors with the numbers back into an identifiable and readable chord. 

#### Sliding Window 
The sliding window is building training pairs by first taking a look at a number of chords specified by the window size. The chords in this window will be used to predict the target chord which is the next chord in the progression. Since our window size is 4, our code instructs to make the input 4 chords and the target chord is going to be the input index plus 4 because that's the size of our window. It is a sliding window because it will continue for the full length of the chord progression in the song.

#### Defining the Model
We're defining the model so it is the same kind of structure as the neural network diagram we've seen in class that utilizes layers of nodes. We utilize ```nn.Module``` and create the first layer where the input is being taken in as the window size times the vocabulary size which is the 10 chord options. Then, this outputs to 16 hidden nodes and the activation function ReLu is used so that there won't be values less than 0. Then, the last line of code in this method is the output layer which is the predictions for each possible chord. 

### What I Don't Understand

#### LR Hyperparameter 
I learned from Gemini that the LR, learning rate, is how much the weights and biases are changed but I still don't quite understand how you're supposed to determine this number because Gemini also explained that having it too low will cause the model to get stuck, but having it too high will cause the model to learn to fast. I'm not really sure how these issues of learning too slow versus too fast actually causes issues, especially since I would think learning slowly would make the model more accurate. How can it just get stuck? I think I need to see this visually to understand it better.

#### Step 6:  ```torch.no_grad```
I still don't have a solid understanding of what ```torch.no_grad``` is doing and why we want it to tell PyTorch to stop recording the history. The history of what? Don't we need the model to be trained and therefore shouldn't we want it to record the history for training purposes? Is it actually necessary or just for efficiency? I understand that we're not training the model yet but I still don't understand why this step is necessary. 

#### Step 6: Optimizer + LR
I think I understand that the optimizer helps to adjust the weights and biases to make our model more correct but I'm confused about how it does this based on the learning rate. How does the Adam algorithm use this? Is the LR specific for this particular algorithm, so are certain algorithms requiring a specific LR?

#### Evaluating in Step 7
It's very uncertain what the code block in Step 7 is doing specifically, especially since there are so many syntactical things that I'm confused about such as the use of 
```
mask = y_test == i
    if mask.sum() > 0:
        acc = (preds[mask] == y_test[mask]).float().mean().item()
```
I understand that in this step this block of code is for when the model is in evaluation mode but what does that really mean and how is that different from when it is training? I understand that this block of code is figuring out the accuracy for predicting each chord but how exactly is ```mask = y_test == i``` creating a filter? What are we filtering, the 10 chords? Why do we need to filter those if yes, don't we already know what those 10 chords are?


## 3. Model Limitations

#### Complex Chords
A limitation is that this model is only using a limited number of chord possibilities based on the dataset. This means that more complex chords such as polychords or chords with tensions won't be predicted or even considered since they don't exist within the dataset. 

#### Chords from other genres 
Another limitation is that the model is being trained on a dataset that is specific to Western pop music. This means it does not have the ability to predict chords in other genres such as jazz or genres from other cultures such as in Bollywood music, for example. 

#### Accurate Chord Prediction Does Not Mean Good Progressions
Though this model might be decent at predicting chords in Western pop music, this does not indicate that it will be useful to produce a satisfying progression. Even in pop music, there is still some variability within chord progressions and uncommon chords are still used for the sake of engaging the listener. 

## 4. Improvement or Experiment

#### LR Hyperparameter Experiment
After working through the original code, I decided to change the learning rate hyperparameter, since this is one that I struggled to understand. When I drastically increased the LR to .80, this changed the final progression results to be far less accurate, as it scored a 30.5% on overall test accuracy. The model had 100% accuracy in predicting the I chord and 0% for every other chord. I then experimented with changing the LR to a much lower value of 0.0001. This time, the overall test accuracy was 52.3%. Once again, the I chord had the highest percentage of 95% accuracy and the IV accuracy also improved to 73%; however, other chords had 0% accuracy. Though this provided more accurate results in comparison to when the LR was .80, it wasn't as accurate as the original setting of LR = 0.01. Through my experimentation, I learned that the LR shouldn't be too high nor too low, in order to account for the overall test accuracy; however, I'm still not sure about how I'm supposed to know what the best LR value should be. Do I need to just guess and check a new LR every single time? Or is there a standard value that most people use as a starting point when developing these models?

## 5. Creative Possibilities
Something I'd like to explore further is having multiple datasets train this predictor model separately so that within the user interface, the user can click a dropdown menu to select what kind of chord progression they'd want predicted. Some options of datasets/setting styles for the user to choose could include Western pop music, jazz, classical music, Samba, and Bollywood music. 
