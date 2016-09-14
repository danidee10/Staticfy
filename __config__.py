def func(endpoint=None, attr_name=None):
    return endpoint, attr_name

frameworks = {
    'flask': {
        'format': "{{ url_for('%(endpoint)s', filename='%(attr_name)s') }}"
    },
    'django': {
        'format': "{%% static '%(attr_name)s' %%}"
    }
}
