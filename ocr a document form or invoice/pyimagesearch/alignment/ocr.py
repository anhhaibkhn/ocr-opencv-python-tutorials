from tesserocr import PyTessBaseAPI, PSM, RIL
from PIL import ImageOps, Image
import numpy as np


def get_text(cropped_pil_im):

    # 文字ギリギリなので、まわりを広げる
    # im = ImageOps.expand(cropped_pil_im, border = 20, fill = 50)

    # NOTE: SetImage が内部で jpeg で Image.save しようとするが
    # alpha channel が含まれているとエラーになる
    # RGB に変換してから SetImage する
    
    im_org = Image.fromarray(np.uint8(cropped_pil_im)) 
    im = ImageOps.expand(im_org, border = 10, fill = "white")
    if im.mode != "RGB":
        rgb_im = im.convert('RGB')
    else:
        rgb_im = im.copy()

    with PyTessBaseAPI(lang="eng", psm=PSM.SINGLE_BLOCK) as api:
        api.SetImage(rgb_im)
        txt = api.GetUTF8Text()

    if txt == '':
        with PyTessBaseAPI(lang="eng", psm=PSM.SINGLE_LINE) as api:
            api.SetImage(rgb_im)
            txt = api.GetUTF8Text()

    if txt == '':
        with PyTessBaseAPI(lang="eng", psm=PSM.SINGLE_WORD) as api:
            api.SetImage(rgb_im)
            txt = api.GetUTF8Text()

    return txt


def get_full_text_box(cropped_pil_im):
    print("############################ CHECK FULL TEXT ##################################")
    # image = Image.fromarray(np.uint8(cropped_pil_im), mode='RGB')
    im_org = Image.fromarray(np.uint8(cropped_pil_im))
    image = ImageOps.expand(im_org, border = 10, fill = "white")
    with PyTessBaseAPI() as api:
        api.SetImage(image)
        boxes = api.GetComponentImages(RIL.TEXTLINE, True)
        print('Found {} textline image components.'.format(len(boxes)))
        for i, (im, box, _, _) in enumerate(boxes):
            # im is a PIL image object
            # box is a dict with x, y, w and h keys
            api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
            ocrResult = api.GetUTF8Text()
            conf = api.MeanTextConf()
            print(u"Box[{0}]: x={x}, y={y}, w={w}, h={h}, "
                "confidence: {1}, text: {2}".format(i, conf, ocrResult, **box))

    print(" ############################END FULL TEXT################################## ")