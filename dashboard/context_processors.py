def default_context(request = None):
    return {
        'servers': {
            'server0' : 'http://localhost:8000',
            'server1' : 'https://www.sys-monitoring.kz',
        },
    }