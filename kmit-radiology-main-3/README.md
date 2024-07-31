# kmit-radiology

Make sure you are using **LINUX** OS and make a seperate folder (For development purpose) and a seperate virtual environment.

**Ignore the '$' symbols, they represent commands to type in terminal**

To install virtualenv in your OS,
```
$ pip3 install virtualenv
```

Make sure you have python3 and pip3 installed in your OS,
To check it type,
```
$ python3 --version
```
Output: python3.x.x (x = the version of python3)

To check pip3 it type,
```
$ pip3 --version
```
Output: pip3 x.x (x = the version of pip3)

If pip3 is not installed, install it by,
```
$ sudo apt-get install pip3
```

Now all the basic installtion is done, now navigate to your newly created folder and open terminal and make a new virtualenv by,
```
$ python3 -m virtualenv <name-of-your-env>
```
**name-of-your-env: This is the name of your virtual environment, name it according to your wish, but name it appropriately**

Activate the environment,
```
$ source <name-of-your-env>/bin/activate
```
You can see the environment activated as:
```
(<name-of-your-env>) new-folder:
```
If you can see your environment name in the brackets then the environment is activated.

Now, clone the kmit-radiology repo in the New Folder you have created,
```
$ git clone https://github.com/himavanthnightrider/udaan-kmit-radiology.git
```
Now, install all the required packages in your virtual environment, to so so,
```
$ cd kmit-radiology

$ pip3 install -r requirements.txt
                or
$ pip install -r requirements.txt
```

Now to run your Application,
**Use python or python3 whichever your system allows, I'll write python here but change it accordingly to what your system allows you.**
```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```
Then you can view the application in the specified PORT in your browser.

But to view the facilities you hae to create an admin user, to do so,
```
$ python manage.py createsuperuser
```
Follow the steps and create your user.

Then, run the application and go to LOGIN and **LOGIN AS DOCTOR/RADIOLOGIST** and then you can use the facilities.


