# import the necessary packages
from textblob import TextBlob
import pytesseract
import argparse
import cv2

"""
--image: The path to the input image to be OCR’d.
--lang: The native language that Tesseract will use when ORC’ing the image.
--to: The language into which we will be translating the native OCR text.
--psm: The page segmentation mode for Tesseract. Our default is for a page segmentation mode of 13, 
which treats the image as a single line of text. For our last example today, we will OCR a full block of text of German. 
For this full block, we will use a page segmentation mode of 3 which is fully 
automatic page segmentation without Orientation and Script Detection (OSD).
"""
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-l", "--lang", required=True,
	help="language that Tesseract will use when OCR'ing")
ap.add_argument("-t", "--to", type=str, default="en",
	help="language that we'll be translating to")
ap.add_argument("-p", "--psm", type=int, default=13,
	help="Tesseract PSM mode")
# Adding argument to direct to tesseract data 
data_path = "C:/Users/nguyenngochai/trial_projects/tessdata"
ap.add_argument("--tessdata-dir", "--data", type=str, default=data_path,
	help="Tesseract language database location")

args = vars(ap.parse_args())

# load the input image and convert it from BGR to RGB channel
# ordering
image = cv2.imread(args["image"])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# OCR the image, supplying the country code as the language parameter
options = "-l {} --psm {} --tessdata-dir".format(args["lang"], args["psm"], args["data"])
text = pytesseract.image_to_string(rgb, config=options)
# show the original OCR'd text
print("ORIGINAL")
print("========")
print(text)
print("")


# translate the text into a different language
tb = TextBlob(text)
translated = tb.translate(to=args["to"])
# show the translated text
print("TRANSLATED")
print("==========")
print(translated)