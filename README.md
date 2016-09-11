# Staticfy
Have you ever been annoyed by the amount of time you spend manually changing the links in a html template you bought or downloaded until all the static files and assets are properly linked and the file looks exactly like the demo you saw online?
with Staticfy you can save that time (and some of your hair) by automatically converting the static urls in your template to dynamic flask url's that wouldn't break if you decide to move your file to another location.

`<img src="img/staticfy.jpg" />` ===> `<img src="{{ url_for('static', filename='img/staticfy.jpg') }}" />`

# Usage
`./staticfy.py staticfy.html --static-endpoint=static --template-folder='templates'`

 `--static-endpoint` and `--template-folder` are optional

Before Staticfying
![alt tag](assets/before.png)
---------------------------------------------------------------------------------------------------------------------------------
After Staticfying
![alt tag](assets/after.png)

Notice how it preserves the font-awesome css link at the top of the file?, external resources (font-awesome, google-fonts, bootstrap files, disqus e.t.c) which aren't hosted locally with your website won't be staticfied. Staticfy also accepts an optional argument `--static-endpoint` in case you're not using the default static endpoint, you can also specify a `--template-folder` where your html template is located, instead of chunking the file location into the filename argument.

# Batch operation
When you specify `--template-folder` without providing any filename, staticfy searches through the specified folder and staticfies all the (html | htm) files it finds, this saves you more time if you want to staticfy a bunch of files at once. you could just create a new folder containing the files you want to staticfy and leave the rest to staticfy.

`./staticfy.py --template-folder='templates'`

It should be noted that sub folders containing html templates won't be staticfied, only templates that exist in the specified directory will be staticfied. (this might change in the future)

Whenever you run staticfy on a template or on a folder, a staticfy folder is generated in the present working directory and the staticfied file(s) is placed in that folder, you also need to copy the file(s) over to the appropriate directory to overwrite the existing file with the new one.

# Tests
The tests are located in the `test.py` file and can be run with
`./test.py`

# Requirements and 3rd party stuff
Beautiful soup 4
`pip3 install bs4`
or you can use the requirements file `pip3 install -r requirements.txt`
