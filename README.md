## TA Instructions

Please see https://ocrmail.ca for our project report. We used web hosting to display our final project. Our objective was to show how OCR algorithms can be used with E-commerse for businesses. 

A few things to note: 

- We could not get a SSL certificate, so if you open the site, it will probably say: security risk, as https could not be used
  on our part. Either you can click 'accept risk,' or try openning our site locally by cloning our github repo. I used atom and  php-server to get everything running. Otherwise our web app is not doing anything fishy, and has been working well for us!
  
- We could not link run the OCR model through the website, as the web host wont allow us to run python scripts on there without
  our dependencies. You can run the ocr_mail.py script locally on your machine. make sure line 15 is updated with the location of your test image :) 
  
- We did not have enough time to implement the 'find closest post office' php function, but the 'find rate' function is enough
  to show how OCR can be used with E-commerce. 
  
## Dependencies
- Preferably create a new python >=3.6 and run 'pip install -r requirements.txt'

## Sources

Cohen, G., Afshar, S., Tapson, J., & van Schaik, A. (2017). EMNIST: an extension of MNIST to handwritten letters. Retrieved from http://arxiv.org/abs/1702.05373

Kane, Frank. “Machine Learning in Python (Data Science and Deep Learning).” Udemy, Mar. 2020, www.udemy.com/course/data-science-and-machine-learning-with-python-hands-on. CNN structure with keras

“Image Segmentation Using OpenCV - Extracting Specific Areas of an Image.” Edited by Madhav, OpenCV Image Segmentation: Tutorial for Extracting Specific Areas of an Image, 13 Mar. 2019, circuitdigest.com/tutorial/image-segmentation-using-opencv.

Chandra, Akshay L. “Alphabet_Recognition_Gestures.” GitHub, 17 Apr. 2019, github.com/acl21/Alphabet_Recognition_Gestures.
