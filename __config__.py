
frameworks = {
    'flask': {
        'format': "{{ url_for('%(endpoint)s', filename='%(attr_name)s') }}"
    },
    'django': {
        'format': "{%% static '%(attr_name)s' %%}"
    }
}
