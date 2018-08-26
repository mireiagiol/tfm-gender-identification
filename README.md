# tfm-gender-identification

## Introduction

(Note that these instructions -only- apply to **Ubuntu 16.04**, for this project has been developed and tested exclusively on that environment. Running this project on another environment may lead to unexpected results.)

This project creates an **arff file**, from a **text input file**, so as to be read by the data mining tool, Weka. The input file contains a **collection of 5400 tweets** alongside **their PoS tags**, provided by **Freeling** in a previously performed analysis.

## Installing

### Git

To install the project, first **clone this repository** using the git command line or whatever GUI tool of your preference (SourceTree, GitKraken, SmartGit).

Install the git command line tool following [these](https://git-scm.com/downloads) instructions.

Now you can open a terminal and type:

`$ git clone https://github.com/mireiagiol/tfm-gender-identification.git`

This will create a folder named "tfm-gender-identification" where you execute the command.

### Python

Now you will need Python to actually run the project and get the arff file. It's important to install **Python 3** and not Python 2 because otherwise the execution will fail.
**Ubuntu 16.04** already comes with the two versions of Python, so we only need to check that everything is up to date:

Open a terminal and type:

`$ sudo apt-get update`

`$ sudo apt-get -y upgrade`

If everything is correct you will be able to call Python 3 by typing `$ python3` from any folder. To test it type `$ python3 -V` and you should see the installed version number on screen.

Then you will need to install the project dependencies such as nltk and Freeling. The fastest way to do it is to set up a **virtual environment**. To create a virtual environment you need to install the command line tool corresponding to this version of Python.

To install virtualenv open a terminal and type:
`$ sudo apt-get install -y python3-venv`

Create an environment by typing:
 `$ python3 -m  venv  <name_of_virtual_environment>`
 
To activate this environment and enter their command promt, type:
`$ source <name_of_virtual_environment>/bin/activate`

Notice the new command prompt with the name of the virtual environment between brackets at the beginning of each line.
Now you can easily install the required dependencies with the **pip package manager** by typing:

### NLTK

`$ pip install nltk`

Before using NLTK you will need to do an **extra step** to download the data that the package uses, as for instance, to tokenize sentences. Run the Python interpreter by typing `$ python3`. Inside the interpreter write this simple script:

`>>> import nltk` (Enter)

`>>> nltk.download()`(Enter)

This will download all necessary data for NLTK to work.

### Freeling

Go to this page and download the corresponding version of the package (in this case [freeling-4.1-xenial-amd64.deb](https://github.com/TALP-UPC/FreeLing/releases/download/4.1/freeling-4.1-xenial-amd64.deb)).
Ensure that you are working with the **exact version** of the downloaded binary package, otherwise it will not work.

You can install Freeling by double clicking the downloaded file. This will place the **analyzer** script on the path */usr/bin/analyzer* and all the Freeling installation and data on the path */usr/share/freeling*.

## Running

To run the project you have to execute the main script i.e. *feature_extraction_arff_file.py* by typing on a terminal `$ python3 feature_extraction_arff_file.py`.

After following all the described steps, two arff files are created inside the project folder: one corresponding to the Bag of Words and another one to the rest of the feature set.