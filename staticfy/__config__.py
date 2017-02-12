"""Config file that hold patterns for new frameworks."""

frameworks = {
    'flask':  "{{ url_for('%(static_endpoint)s', filename="
    "'%(asset_location)s') }}",

    'django': "{%% static '%(asset_location)s' %%}",
    'laravel': "{{ URL::asset('%(asset_location)s') }}"
}
