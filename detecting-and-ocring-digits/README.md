## Detecting and OCR’ing Digits with Tesseract and Python

[Source](https://www.pyimagesearch.com/2021/08/30/detecting-and-ocring-digits-with-tesseract-and-python/)

Learning Objectives:

- Gain hands-on experience OCR’ing digits from input images
- Extend our previous OCR script to handle digit recognition
- Learn how to configure Tesseract to only OCR digits
- Pass in this configuration to Tesseract via the pytesseract library


### Digit Detection and Recognition?
As the name suggests, digit recognition is the process of OCR’ing and identifying only digits, purposely ignoring other characters. Digit recognition is often applied to real-world OCR projects (a montage of which can be seen in the below picture), including:

- Extracting information from business cards
- Building an intelligent water monitor reader
- Bank check and credit card OCR


<img src="https://929687.smushcdn.com/2407837/wp-content/uploads/2021/06/detect_ocr_digits.jpg?size=630x390&lossy=1&strip=1&webp=0"
     alt="this is an optional description of the image to help the blind and show up in case the
          image won't load"
     style="display:block; /* override the default display setting of `inline-block` */
            float:none; /* override any prior settings of `left` or `right` */
            /* set both the left and right margins to `auto` to center the image */
            margin-left:auto;
            margin-right:auto;
            width:75%; /* optionally resize the image to a screen percentage width if you want too */
            ">