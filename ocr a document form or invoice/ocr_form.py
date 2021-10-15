from pyimagesearch.alignment.align_images import align_images 
from pyimagesearch.alignment.ocr import *
from collections import namedtuple
import pytesseract
import argparse
import imutils
import cv2


def cleanup_text(txt):
    """ strip out non-ACSII text to draw the text on image by opencv """
    return "".join([c if ord(c) < 128  else "" for c in txt]).strip()


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to input image using for template alignment")
ap.add_argument("-t", "--template", required=True,
    help="path to input template image")
ap.add_argument("-d", "--debug", required=False,
    help="For helping debug picture")

args = vars(ap.parse_args())

SHOW_TEXT = args["debug"] if args["debug"] else False

# create a named tuple which we can use to craete locations of the input doc 
OCRLocation = namedtuple("OCRLocation",["id", "bbox","filter_keywords"])

# define the locations of each area of the doc we need to OCR MANUALLY
OCR_LOCATIONS = [

	OCRLocation("step1_first_name", (119, 110, 215, 30),
		["middle", "initial", "first", "name"]),
	OCRLocation("step1_last_name", (346, 110, 215, 30),
		["last", "name"]),
	OCRLocation("step1_address", (120, 140, 215, 30),
		["address"]),
	OCRLocation("step1_city_state_zip", (120, 172, 480, 30),
		["city", "zip", "town", "state"]),
	OCRLocation("step5_employee_signature", (130, 810, 430, 55),
		["employee", "signature", "form", "valid", "unless",
		 	"you", "sign"]),
	OCRLocation("step5_date", (580, 815, 145, 50), ["date"]),
	OCRLocation("employee_name_address", (120, 870, 350, 60),
		["employer", "name", "address"]),
	OCRLocation("employee_ein", (590, 872, 448, 135),
		["employer", "identification", "number", "ein"]),
]

# load the input image and template from disk
print("[INFO] loading images...")
image = cv2.imread(args["image"])
template = cv2.imread(args["template"])
# align the images
print("[INFO] aligning images...")
aligned = align_images(image, template)
cv2.imshow("aligned",aligned)
cv2.waitKey(0)

# initialize a results list to store the document OCR parsing results
print("[INFO] OCR'ing document...")
parsingResults = []

# loop over the locations of the document we are going to OCR
for loc in OCR_LOCATIONS:
    # extract the OCR ROI from the aligned image
    (x, y, w, h) = loc.bbox
    roi = aligned[y:y + h, x:x + w]
    # OCR the ROI using Tesseract
    rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(rgb)
    print("extract text:", text)
    if SHOW_TEXT > 0:
        rgb_copy = rgb.copy()
        compare_text = get_text(rgb_copy)
        print("compare text:", compare_text)

        rgb_copy_next = rgb.copy()
        full_text = get_full_text_box(rgb_copy_next)

    # break the text into lines and loop over them
    for line in text.split("\n"):
        # if the line is empty, ignore it
        if len(line) == 0:
            continue

        # convert the line to lowcase and then check to see if the line contains key words
        # these keywords are part of the form and then should be ignored
        lower = line.lower()
        count = sum([lower.count(x) for x in loc.filter_keywords])

        # if the count is zero then we know we are *not* examining a
		# text field that is part of the document itself (ex., info,
		# on the field, an example, help text, etc.)
        if count == 0:
            # update our parsing results dictionary with the OCR'd
            # text if the line is *not* empty
            parsingResults.append((loc, line))



# initialize a dictionary to store our final OCR results
results = {}
# loop over the results of parsing the document
for (loc, line) in parsingResults:
	# grab any existing OCR result for the current ID of the document
	r = results.get(loc.id, None)
	# if the result is None, initialize it using the text and location
	# namedtuple (converting it to a dictionary as namedtuples are not
	# hashable)
	if r is None:
		results[loc.id] = (line, loc._asdict())
	# otherwise, there exists an OCR result for the current area of the
	# document, so we should append our existing line
	else:
		# unpack the existing OCR result and append the line to the
		# existing text
		(existingText, loc) = r
		text = "{}\n{}".format(existingText, line)
		# update our results dictionary
		results[loc["id"]] = (text, loc)


# loop over the results
for (locID, result) in results.items():
	# unpack the result tuple
	(text, loc) = result
	# display the OCR result to our terminal
	print(loc["id"])
	print("=" * len(loc["id"]))
	print("{}\n\n".format(text))
	# extract the bounding box coordinates of the OCR location and
	# then strip out non-ASCII text so we can draw the text on the
	# output image using OpenCV
	(x, y, w, h) = loc["bbox"]
	clean = cleanup_text(text)
	# draw a bounding box around the text
	cv2.rectangle(aligned, (x, y), (x + w, y + h), (0, 255, 0), 2)
	# loop over all lines in the text
	for (i, line) in enumerate(text.split("\n")):
		# draw the line on the output image
		startY = y + (i * 70) + 40
		cv2.putText(aligned, line, (x, startY),
			cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 255), 5)


cv2.imshow("Input", imutils.resize(image, width=700))
cv2.imshow("Output", imutils.resize(aligned, width=700))
cv2.waitKey(0)