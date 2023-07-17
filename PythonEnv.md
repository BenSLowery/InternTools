## Creating a Python Environment (in Windows)
The following was checked on 17/07/2023. Given Linux/Mac is much easier to set up and has far more documentation this is just instructions for Windows users.

#### Step 1. Installing PyEnv-windows
**Context**: [pyenv](https://github.com/pyenv-win/pyenv-win) is a python version management tool. Its originally designed for UNIX based systems (Mac and Linux) however, it has been ported to windows. Its main use is to allow self contained python versions which is great for when we may want to test code in previous versions of python, OR, if we want to safely migrate code to a version of python without risking losing the old set up. 

**Install**
First, we need permission to execute powerscripts (doesn't seem to be be the default case with thr Lancaster laptops). To do this, open `Windows Powershell` and run the following:

```bash
C:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
This should then allow to install `pyenv` for windows. In the same `Powershell` terminal run the following:

```bash
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

Then if you close the `Powershell` and open either a new `Powershell` or a regular `command prompt`, you should be able to enter `pyenv` which will give a list of commands to use.

**Create a Python Environment**
We now have access to install any Python version, for this project we will use python version `3.10.6` which has been used for my current inventory model development. In a terminal run:
```bash
pyenv install 3.10.6 -q
```
The `-q` command stops a pop-up installation wizard from occuring. 

Note, if python has been installed already on the windows computer, the keyword `python` would have already been taken by this installation, [there are way to get round this if you want](https://stackoverflow.com/questions/64138572/pyenv-global-interpreter-not-working-on-windows10), however the executable `python3` will be linked with the pyenv install. Further, in the next step we will enter a virtual environment, and this restores the use of `python` keyword to follow what is installed through pyenv. So we just need to use `python3` instead of `python` when we are out of a virtual environment.

To switch our installation to this python version, run the following:
```bash
pyenv global 3.10.6
python3 -V
```
this should then return `3.10.6`. You can see more you can do with PyEnv [here](https://github.com/pyenv-win/pyenv-win#usage). However this is suffice for us to move forward.


#### Step 2. Creating a virtual enviroment with `venv`
**Context:** Virtual environments let us keep self contained list of packages and settings for a project. Say we have two projects, each requiring a different version of some python package. A virtual environment lets us install the package independently with its prefered versions for both projects. It is also useful for sharing and deploying code as, if someone else wants to use the project on their machine, they'll have a pre-made environment we know the python code runs on. 

**Usage**
We first ensure we're in the correct python environment. I.e. check that `pyenv global` returns `3.10.6`.

Then, create and enter a project folder we'll do all our work from. From that we create a new virtual envioronment. Give it a short, recognisable name representing our project.

```bash
mkdir InvControl && cd InvControl
python3 -m venv InvEnv
````
To enter a virtual environment we use the following command.
```bash
InvEnv\Scripts\activate
```
To ensure we have entered the environment, we should have `(InvEnv)` at the start of the terminal prompt. From here we have a fresh empty python environment. We can use `python` instead of `python3` from now on.

#### Step 3. Installing packages
In this installation we should have no packages over than those installed by default. We can check with `pip freeze` which should return empty. To install packages we do this the conventional python way of `pip install [package]`. To save time, i've made a `requirements.txt` file in this repo which contains a list of packages you'll likely need. Download the file into the project folder and run:

```bash
pip install -r requirements.txt
```

If we run `pip freeze` we should now get the following list returned to us:
```bash
asttokens==2.2.1
backcall==0.2.0
colorama==0.4.6
contourpy==1.1.0
cycler==0.11.0
Cython==3.0.0
decorator==5.1.1
executing==1.2.0
fonttools==4.41.0
ipython==8.14.0
jedi==0.18.2
kiwisolver==1.4.4
matplotlib==3.7.2
matplotlib-inline==0.1.6
numpy==1.25.1
packaging==23.1
pandas==2.0.3
parso==0.8.3
pickleshare==0.7.5
Pillow==10.0.0
prompt-toolkit==3.0.39
pure-eval==0.2.2
Pygments==2.15.1
pyparsing==3.0.9
python-dateutil==2.8.2
pytz==2023.3
scipy==1.11.1
six==1.16.0
stack-data==0.6.2
traitlets==5.9.0
tzdata==2023.3
wcwidth==0.2.6
```
Notice how it's installed some more packages then in the requirements.txt list; these are just dependencies to the core packages

