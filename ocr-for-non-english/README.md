## Usage
Example 1: python easy_ocr.py --image images/arabic_sign.jpg --langs en,ja
Example 2: python easy_ocr.py --image images/arabic_sign.jpg --langs en,ar
Example 3: python easy_ocr.py --image images/swedish_sign.jpg --langs en,sv
Example 4: python easy_ocr.py --image images/turkish_sign.jpg --langs en,tr

Source: [Pyimagsearch](https://www.pyimagesearch.com/) 

### 1. Using EasyOCR package to easily perform Optical Character Recognition and text detection with Python
- ocr-for-non-english\easy_ocr.py

Note 1: The following error may appear when opencv-python installation went wrong. 
```` 
cv2.imshow("Image", image)
 ....
cv2.error: OpenCV(4.5.3) C:\Users\runneradmin\AppData\Local\Temp\pip-req-build-au50kd6q\opencv\modules\highgui\src\window.cpp:1274: error: (-2:Unspecified error) The function is not implemented. Rebuild the library with Windows, GTK+ 2.x or Cocoa support. If you are on Ubuntu or Debian, install libgtk2.0-dev and pkg-config, then re-run cmake or configure script in function 'cvShowImage'

Tentative workarounds are to run the following commands:
pip uninstall opencv-python-headless -y 
pip uninstall opencv-python
pip install opencv-python --upgrade
````

Note 2: To display **non-Unicode** such as Japanese on CMD, do the following steps:
```` 
1. open the Control Panel;
2. click Region and Language;
3. on the Administrative tab, under Language for non-Unicode programs, click "change system locale...";
4. set the Current system locale as "Japanese(Japan)".
````

### 2. Checking Tesseract OCR for Non-English Languages:
- ocr-for-non-english\ocr_non_english.py

Note 1: The origional code had some errors:
''''
File "C:\Program Files\Python39\lib\urllib\request.py", line 641, in http_error_default
    raise HTTPError(req.full_url, code, msg, hdrs, fp)
urllib.error.HTTPError: HTTP Error 404: Not Found
''''
To fix it, we need to modify the TextBlob's translate.py file:
''''
url = "http://translate.google.com/translate_a/t?client=webapp&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&otf=2&ssel=0&tsel=0&kc=1"
''''
then change above code in translate.py to following:
''''
url = "http://translate.google.com/translate_a/t?client=te&format=html&dt=bd&dt=ex&dt=
''''

Note 2:
- This file needs to use Tesseract data for dealing with multiple languages. I added a new parser argument --tessdata-dir to avoid changing the TESSDATA_PREFIX environment variable. From this point, you can navigate the tesseract data where you cloned from the original GitHub data. 
