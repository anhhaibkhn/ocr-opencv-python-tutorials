# USAGE
# python easy_ocr.py --image images/arabic_sign.jpg --langs en,ar

# import the necessary packages
from easyocr import Reader
import argparse
import cv2

def cleanup_text(text):
	# strip out non-ASCII text so we can draw the text on the image
	# using OpenCV
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()


"""
--image: The path to the input image containing text for OCR.

--langs: A list of language codes separated by commas (no spaces). 
By default our script assumes English language (en). If you’d like to use the English and French models, 
you could pass en,fr. Or maybe you’d like to use Spanish, Portuguese, and Italian by passing es,pt,it. 
Be sure to refer to EasyOCR’s listing of supported languages.

--gpu: Whether or not you’d like to use a GPU. Our default is -1, meaning that we’ll use our CPU rather than a GPU.
If you have a CUDA-capable GPU, enabling this option will allow faster OCR result

"""
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-l", "--langs", type=str, default="en",
	help="comma separated list of languages to OCR")
ap.add_argument("-g", "--gpu", type=int, default=-1,
	help="whether or not GPU should be used")
args = vars(ap.parse_args())

# break the input languages into a comma separated list
langs = args["langs"].split(",")
print("[INFO] OCR'ing with the following languages: {}".format(langs))

# load the input image from disk
image = cv2.imread(args["image"])

# EasyOCR can take opencv default BGR, not like Tesseract. 
# OCR the input image using EasyOCR
print("[INFO] OCR'ing input image...")
reader = Reader(langs, gpu=args["gpu"] > 0)
results = reader.readtext(image)

# loop over the results, each EasyOCR result consists of a 3-tuple:
# bbox: The bounding box coordinates of the localized text
# text: Our OCR’d string
# prob: The probability of the OCR results
for (bbox, text, prob) in results:
	# display the OCR'd text and associated probability
	print("[INFO] {:.4f}: {}".format(prob, text))

	# unpack the bounding box
	(tl, tr, br, bl) = bbox
	tl = (int(tl[0]), int(tl[1]))
	tr = (int(tr[0]), int(tr[1]))
	br = (int(br[0]), int(br[1]))
	bl = (int(bl[0]), int(bl[1]))

	# cleanup the text and draw the box surrounding the text along
	# with the OCR'd text itself
	text = cleanup_text(text)
	cv2.rectangle(image, tl, br, (0, 255, 0), 2)
	cv2.putText(image, text, (tl[0], tl[1] - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)