def default_context(request = None):
    return {
        'servers': {
            'server0' : 'https://rfid-kassa.com',
            'server1' : 'https://www.sys-monitoring.kz',
        },
    }