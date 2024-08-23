from setuptools import setup, find_packages  

setup(  
    name='easyocr2',  
    version='0.1',  
    packages=find_packages(),  
    install_requires=[  
        'easyocr',  
        'pyautogui',  
        'Pillow',  
        'screeninfo',  
    ],  
    entry_points={  
        'console_scripts': [  
            'easyocr-app = my_easyocr_app.main:main',  # Adjust if needed  
        ],  
    },  
    author='Narimanamiri',  
    description='A Python application to read text under the mouse using OCR.',  
    url='https://github.com/narimanamiri/easyocr2',  # Replace with your GitHub URL  
)