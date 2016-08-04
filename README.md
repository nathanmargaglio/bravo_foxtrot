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
