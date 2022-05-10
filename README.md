This is a test task for admission to the Department of ISP RAS.

    Using the Tesseract segmentation tool, run an image of the document through it (example below),
    get a set of bounding boxes for words and try to combine individual words into lines.

    User interaction is as follows:
      $textline_drawer input_image.png output_image.png
    
    - inpyt_image.png is the path to the input document
    - output_image.png is the path where the program will write the image with markup.
    
    
  For developers:

    Libraries:
      tesserocr (https://github.com/sirfz/tesserocr)/pytesseract (https://github.com/madmaze/pytesseract),
      opencv (https://pypi.org/project/opencv-python/), 
      numpy (https://pypi.org/project/numpy/),
      
      argparse, imutils, pillow, setuptools

    Project structure:
      - textline.py - startup file
      - recognition.py - module with recognition functions
      - corectness.py - module for check data correctness
      - constants.py - module with project constants
      
