import numpy as np
import easyocr


class OCR:
    def __init__(self, image) -> None:
        self.image = image
        self.reader = easyocr.Reader(
            lang_list=['en'],
            gpu=False,
            model_storage_directory='EasyOCR\model',
            download_enabled=False,
            user_network_directory='EasyOCR\user_network'
        )

    def detection(self):
        img_arr = np.array(self.image, dtype=np.uint8)
        response = self.reader.readtext(image=img_arr)

        detected_text = ""
        for _, text, _ in response:
            detected_text += text + "\n"

        return detected_text


    