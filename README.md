# Staticfy
Have you ever been annoyed by the amount of time you spend manually changing the links in a html template you bought or downloaded until all the static files and assets are properly linked and the file looks exactly like the demo you saw online?
with Staticfy you can save that time (and some of your hair) by automatically converting the static urls in your template to dynamic flask url's which would not break if you decide to move your file to another location.

`<img src="img/staticfy.jpg" />` -----> `<img src="{{ url_for('static', filename='img/staticfy.jpg') }}" />`

# Usage
`./staticfy.py --filename=staticfy.html --static-endpoint=static --template-folder='templates'`
 
 --static-endpoint and --template-folder are optional
 
Before staticfy
![alt tag](assets/before.png)
---------------------------------------------------------------------------------------------------------------------------------
After staticfy
![alt tag](assets/after.png)

Notice how it preserves the font-awesome css link at the top of the file, staticfy also accepts an optional argument `--static-endpoint` in case you're not using the default static endpoint, you can also specify a `--template-folder` where your html template is located, instead of chunking the file location into the filename argument
 
# Requirements and 3rd party stuff
Beautiful soup 4
`pip3 install bs4` or you can use the requirements file `pip3 install -r requirements.txt`
