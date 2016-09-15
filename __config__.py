
frameworks = {
    'flask':  "{{ url_for('%(endpoint)s', filename='%(attr_name)s') }}",
    'django':"{%% static '%(attr_name)s' %%}"
}
