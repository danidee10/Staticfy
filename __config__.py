# config file to add support for new frameworks in flask
#key => framework, value => pattern to use when staticfying

frameworks = {
    'flask':  "{{ url_for('%(static_endpoint)s', filename='%(asset_location)s') }}",
    'django':"{%% static '%(asset_location)s' %%}",
    'laravel': "{{ URL::asset('%(asset_location)s') }}"
}
