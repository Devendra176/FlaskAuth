import moviepy.editor as mp
import wifi_qrcode_generator as qr
import random
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import easyocr
import matplotlib.pyplot as plt
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

current_path = os.getcwd()


def add_video_file(filename, Out_path, new_file_name):
    status = {}
    try:
        file, extension = os.path.splitext(new_file_name)
        out_filename = os.path.join(Out_path, file + ".mp3")
        my_clip = mp.VideoFileClip(os.path.join(current_path, filename))
        audio_filename = my_clip.audio.write_audiofile(
            os.path.join(current_path, out_filename))
        status = {
            'status': True,
            'output': out_filename.split('login_project')[1]
        }
    except Exception as e:
        print(e)
        status = {'status': False, 'output': None}
    return status


def wifi_qr(wifi_name, hidden, password, encryption, destination):
    status = {}
    try:
        qr_code = qr.wifi_qrcode(wifi_name, hidden, encryption, password)
        final_dest = os.path.join(current_path, destination)
        file_name = wifi_name + '_' + str(random.randint(0, 100000)) + '_.png'
        file_path = os.path.join(final_dest, file_name)
        qr_code.save(file_path)
        status = {
            'status': True,
            'output': os.path.join(destination, file_name),
            'file_name': file_name
        }
    except Exception as e:
        print(e)
        status = {'status': False}

    return status


class ExtractText(object):
    def pre_proccesing(self, image):
        image = cv2.imread(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        invert = cv2.bitwise_not(gray)
        # cv2.imwrite('firstinvert.jpg',invert)
        kernel = np.ones((1, 1), np.uint8)
        image = cv2.dilate(invert, kernel, iterations=1)
        kernel = np.ones((1, 1), np.uint8)
        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        # print(image)
        # image = cv2.medianBlur(image,3)
        # image = cv2.bitwise_not(image)
        # cv2.imwrite('secondinvert.jpg',image)
        return image

    def recognize_text(self, image):
        '''loads an image and recognizes text.'''
        image = self.pre_proccesing(image)
        reader = easyocr.Reader(['en'])
        for_draw = reader.readtext(image)
        for_show = reader.readtext(image, detail=0, paragraph=True)
        return (for_draw, for_show)

    def output_file(self, output_path, file_name):
        output_path = os.path.join(current_path, output_path)
        out_filename = os.path.join(output_path, file_name)
        return out_filename

    def draw(self, image_data, result, out_filename, color='yellow', width=2):
        make = ImageDraw.Draw(image_data)
        for res in range(len(result)):
            p0, p1, p2, p3 = result[res][0]
            make.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
            image_data.save(out_filename)
        return out_filename

    def get_image(self, image_path, output_path, file_name):
        status = {}
        try:
            out_filename = self.output_file(output_path, file_name)
            image_path = os.path.join(current_path, image_path)
            image_data = Image.open(image_path)
            result, for_show = self.recognize_text(image_path)
            self.draw(image_data, result, out_filename)
            status = {
                'status': True,
                'output': ' '.join(for_show),
                'out_filename': os.path.join(output_path, file_name)
            }
        except Exception as e:
            print(e)
            status = {'status': False}
        return status