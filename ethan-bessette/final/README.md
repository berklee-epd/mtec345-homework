# Gesture based experience in Unity


## Documentation

First, I converted the web example to allow multiple people to be recognized. I also added pose recognition in addition to hand and face recognition. I then tried to implement it in python and ran into some issues with documentation.

I was curious how difficult it would be to get working in Unity. I ended up using YOLO instead of MediaPipe because it was easier for me to get into .onnx format.

Steps:

1. Export YOLO pose recognizer to onnx, import to Unity
2. Follow the webcam documentation combined with help from a coding agent to get the proper permissions to select a camera and use it in Unity.
3. Test the camera in Unity, create a small scene that shows the camera.
4. Write a script to stream the webcam data to the pose recognizer. Format the data in an easy to read way
    - make landmarks into an enum
    - make a struct for keypoints to easily name them in the inspector and pair them with their position
    - make a class pose to hold instances of all the key point structs to make it easier to work with a list of all people recognized
    - create logic to only add a pose to the list if the confidence rating is above a threshold. Send 0s for all key point positions if their confidence is below a threshold.
    - use multiple workers, one to run the model, and the other for everything else
    - convert the webcam data to tensor with shape TensorShape(1, 3, height, width) # batch, RGB, pixel H and W
    - a list of raw landmarks that I studied to understand the format to convert into the pose class and landmark structs I mentioned earlier

5. Implement Dynamic Time Warping
    - I downloaded a package with a useful UI for training models within Unity that saves the weights to a JSON file. It works similar to wekinator, you can add samples, train on the samples, then enter prediction mode
    - It wasn't using actual DTW, so I got help from a coding agent to modify it use use true DTW
    - I tested the training a little and it worked! I didn't save the training though because I was sitting and I want to be standing
