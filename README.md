### Status
[![Build Status](https://travis-ci.org/danidee10/Staticfy.svg?branch=master)](https://travis-ci.org/danidee10/Staticfy)

# Staticfy
Have you ever been annoyed by the amount of time you spend manually changing the links in a html template you bought or downloaded until all the static files and assets are properly linked and the file looks exactly like the demo you saw online?
with Staticfy you can save that time (and some of your hair) by automatically converting the static urls in your template to dynamic flask url's that wouldn't break if you decide to move your file to another location.

`<img src="img/staticfy.jpg" />` ===> `<img src="{{ url_for('static', filename='img/staticfy.jpg') }}" />`

# Usage
make the script executable with
`sudo chmod +x staticfy.py`

and run it

`./staticfy.py staticfy.html --static-endpoint=static --template-folder=templates`

using `./` runs Staticfy with python3, if you're running windows or you want to use another version of python e.g python2, you can just run

`python2 staticfy.py staticfy.html --static-endpoint=static --template-folder=templates`

 `--static-endpoint` and `--template-folder` are optional

### Before Staticfying
![alt tag](assets/before.png)
---------------------------------------------------------------------------------------------------------------------------------
### After Staticfying
![alt tag](assets/after.png)

Notice how it preserves the font-awesome css link at the top of the file?, external resources (font-awesome, google-fonts, bootstrap files, disqus e.t.c) which aren't hosted locally with your website won't be staticfied. Staticfy also accepts an optional argument `--static-endpoint` in case you're not using the default static endpoint, you can also specify a `--template-folder` where your html file is located, instead of chunking the file location into the filename argument.

Staticy also preserves the indentation and formatting of any html file given to it

# Batch operation
When you specify `--template-folder` without providing any filename, staticfy searches through the specified folder and staticfies all the (html | htm) files it finds, this saves you more time if you want to staticfy a bunch of files at once. you could just create a new folder containing the files you want to staticfy and leave the rest to staticfy.

`./staticfy.py --template-folder='templates'`

It should be noted that sub folders containing html files won't be staticfied, only html files that exist in the specified directory will be staticfied. (this might change in the future)

Whenever you run staticfy on a template or on a folder, a staticfy folder is generated in the present working directory and the staticfied file(s) is placed in that folder, you also need to copy the file(s) over to the appropriate directory to overwrite the existing file with the new one.

# Tests
The tests are located in the `test.py` file and can be run with
`./test.py`

# Python support
Staticfy supports both python2 and python3
python 2.7 >

# Requirements and 3rd party stuff
Beautiful soup 4
`pip3 install bs4`
or you can use the requirements file `pip3 install -r requirements.txt`

if you have issues with importing HTML.parser on python 3.5, run this
`pip install --upgrade beautifulsoup4`

# Contribution
Pull requests and issues are welcome, if you're making a pull request, make sure
you respect the surrounding code style and write tests to show that your code
works, in your PR and commit also describe clearly what your PR attempts to
fix/improve/add
