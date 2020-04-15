## TA Instructions

Please see https://ocrmail.ca for our project report. We used web hosting to display our final project. Our objective was to show how OCR algorithms can be used with E-commerse for businesses. 

A few things to note: 

- We could not get a SSL certificate, so if you open the site, it will probably say: security risk, as https could not be used
  on our part. Either you can click 'accept risk,' or try openning our site locally by cloning our github repo. I used atom and  php-server to get everything running. Otherwise our web app is not doing anything fishy, and has been working well for us!
  
- We could not link run the OCR model through the website, as the web host wont allow us to run python scripts on there without
  our dependencies. You can run the ocr_mail.py script locally on your machine. make sure line 15 is updated with the location of your test image :) 
  
- We did not have enough time to implement the 'find closest post office' php function, but the 'find rate' function is enough
  to show how OCR can be used with E-commerce. 
