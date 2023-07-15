## Creating a Python Environment (in Windows)
The following was checked on 15/07/2023

#### Step 1. Installing PyEnv-windows
Context: [pyenv](https://github.com/pyenv-win/pyenv-win) is a python version management tool. Its originally designed for UNIX based systems (Mac and Linux) however, it has been ported to windows. Its main use is to allow self contained python versions which is great for when we may want to test code in previous versions of python, OR, if we want to safely migrate code to a version of python without risking losing the old set up. 

#### Step 2. Creating a virtual enviroment with `venv`
Context: Virtual environments let us keep self contained list of packages and settings for a project. Say we have two projects, each requiring a different version of some python package. A virtual environment lets us install the package independently with its prefered versions for both projects. It is also useful for sharing and deploying code as, if someone else wants to use the project on their machine, they'll have a pre-made environment we know the python code runs on. 
First its best to create a project directory. 

Virtual environments (or `venv`) come pre-packaged with python so we can utilise it straight out the box. 

* Step 3. Entering the environment and installing packages

