# What if you want to play with the code in Windows?

## First Time Only

These are my suggestions for an environment where you
want to play with the code, but not really contribute 
to the project. The first time you should do all the following
steps:

1. Go to https://github.com/cscortes/crazyvaders and download
the zip file.
    * Decompress your zip to the desktop.
    * you should see a crazyvaders-master directory on your
    desktop.
1. Go to https://www.python.org/downloads/release/python-365/ and download Python 3.6.5 for windows, probably the executable version is what you need.
    * Don't forget to check the "include Python in the 
PATH" checkbox so that you can execute Python from the
console when you start the install. 
1. Start a Windows console: 
    * CD to your desktop 
    * then CD to crazyvaders-master
1. Install pipenv like so:
    * python -m pip install pipenv 
1. Use pipenv to download all Python dependencies for the crazyvaders like so:
    * python -m pipenv install 
1. Run pipenv to switch to your environment:
    * python -m pipenv shell
    (your prompt should change in the Windows console)
    * python crazyvaders 


If everything went right, you should be playing crazyvaders.

## The next day or when you login again

1. Start a Windows console:
    * CD to your desktop 
    * then CD to crazyvaders-master
1. Run pipenv to switch to your environment:
    * python -m pipenv shell
    * python crazyvaders 

I highly recommend Visual Code for a Python editor.  You can get it here: https://code.visualstudio.com/

