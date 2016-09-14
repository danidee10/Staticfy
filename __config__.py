# config file to add support for new frameworks in flask
#key => framework, value => pattern to use when staticfying

frameworks = {
            'flask': "{{{{ url_for('{}', filename='{}') }}}}",
            'django': "{{% {} '{}' %}}"
            }

