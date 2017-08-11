"""Config file that hold patterns for new frameworks."""

frameworks = {
    'flask':  "{{ url_for('%(namespace)s%(static_endpoint)s', filename="
    "'%(asset_location)s') }}",

    'django': "{%% static '%(namespace)s%(asset_location)s' %%}",
    'laravel': "{{ URL::asset('%(namespace)s%(asset_location)s') }}"
}
