import os
try:
    os.remove('templates/privacy.html`')
    print('Successfully removed typoed file.')
except Exception as e:
    print(f'Error: {e}')
