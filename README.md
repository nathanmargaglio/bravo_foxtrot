# bravo_foxtrot
#### Or:  How I learned to Love Again.


# Preliminary Stuff:

First things first:  this project requires quite a bit of dependencies.  I don't think any of it is TOO bad (nothing more than pip installing and a couple of more in depth packages), but most of it should be straight forward.  The following list are essentials:

  - numpy
  - pandas
  - pyplot
  - theano
  - keras
  
Next, consider that the project is in 'rapid' development, and will be updated and modified a whole bunch.  Since none of the individual files are far from complete, there is going to be a lot of hoping around.  You're just going to have to deal with it and commit accordingly.

Finally, understand that the scope of the project is very large.  I'm looking at something on the lines of commercial use, so don't expect portions of it to be straight forward.  The math is far from trivial, and the concepts involved can be daunting (but, frankly, intuitve).  You're gonna have to understand the basic algorithm for training neural networks for any of this to make sense.  But it's not too bad.

With that being said, let's run through the program.

# Structure and Rundown
### Or:  Another preliminary, basically.

At this point, you should have downloaded the repository and installed the dependencies.  To check this, run 'main.py' as a python file (of course).  It doesn't need any arguments, but you can optionally give it one name argument which is used for identifiying outputs.  If it runs and successfully produces at least one plot (which will be located in logs/<name of instance>/img/), then you're all set.

The project currently contains five core files and a data folder.  The "logs" folder will be generated on the first run, but the contents of the directory are required for running the website (but aren't needed for the core program).

The five core files are: datahandle.py, logger.py, main.py, neuralnet.py, and plotdevice.py.

The core program is initiated through main.py.  This file contains a very simple version of the training algorithm.  The way it works is when you run main.py, it creates a new DataHandle class (located in datahandle.py).  The DataHandle class handles the data (as one might have suspected).  Currently, we are only using one data set, so everything is a bit hard coded.  As we progress, we'll need to allow for more datasets to be added.  For now, the 2015 data provided will be sufficient.

The DataHandle class takes care of a lot of things when it is initialized.  As we progress, we'll need to add more options to it.  For now, let it do it's things.  The main function involved with the class will be 'getWorkingData' and 'getRawData', which are used to actuall access the full data (raw data) and the training data (working data).

The next class to be used is the NeuralNet class located in neuralnet.py.  The use of this one is less straightforward, but, as above, most of the leg work is done automatically.  You need to give the class the length of the input vector when you intialize it (done in the code through 'wi_vec.shape[1]') but the rest is taken care of from there.  If you did give an arguement name to main.py, then it is at this point the name is prepended to the neural networks name (which is a number representing the date time as a single integer).

After this, we get the topoloy, learning_rate, and epochs using the neural networks (nn) 'getTopology' function.  Then we get the actual neural network model using the nn's getModel function.  These will be used later when we plot and log.  Next, we create an instance of a plotDevice (a class located in plotdevice.py).  We set it's parameters using it's setParams function, and we directly pass in the DataHandler's training parameters using it's 'getTrainingParameters' function.  Some hard coded numbers are set, then we instatiate a Logger instance (a class located in logger.py).  We pass it some parameters for book keeping, and we are all set.

Up to this point, we have merely set up the environment needed to do the actual deep learning.  The next step enters the loop of the learning process.

# Training

### Or:  Is this joke over yet?

We have made it to the bread and butter of the program: training our neural network to predict some value based on some parameters we have already set up in the previous portion.  Now, most of the code following the 'for loop' is keeping track of things like error and convergence (things you don't need to worry about).  But we'll take a quick look at what's going on here.

First, we call our model's 'fit' function with parameters 'wi_vec, wo_vec, verbose=0, nb_epoch=epochs.'  The key components here are the 'wi_vec' and 'wo_vec' inputs.  These came from the DataHandler instance, and represent our "working input vector" and "working output vector" respectably.  The first, wi_vec, is an array of arrays.  Each array in it is of length wi_vec.shape[1], and contains a series of floats normalized between -1 and 1.  The output vector, wo_vec, is an array of arrays (who are just length 1 for now).  These contain the values we want to predict.

The fit function performs gradient descent on the model using the vectors 'epochs' numbers of times.  This process is very math, and I'll have to explain the inner workings of this function some other time.  For now, consider the fit function a magical device which trains our artifical neural network.

We then use the partially trained nn to predict the values of the input arrays.  The amount it is wrong is the error.  We want that to be minimal.  We also do the same thing, but for a separate pair of vectors called 'vi_vec' and 'vo_vec.'  These are our 'verification input vector' and 'verification output vector.'  We use these to test the quality of the neural network.  This is a very important step, but I'd need to explain in better detail why we do it some other time.

Every iteration plots the data to a file located in logs/<name of instance>/img.  If the loop meets any of the exiting conditions (basically, convergence), then we plot one more image of the final pass through to logs/static, and we exit (returning the last error).

Then we repeat.

# Conclusions
### Or: pls clap.

The program runs, and really isn't running too bad.  But a lot of work needs to go into it before it is ready to go.  This README should only be considered as a basic walkthough so you can see the mechanisms of the project, but we'll need to go into detail about what's going on with these classes and how you can help me make it better.
