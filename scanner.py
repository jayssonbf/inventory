"""database.py: Handles the functionality relating to the scanner"""
import cv2
from pyzbar import pyzbar
import imutils


# Thrown exception when barcode is found
class FoundBarcode(Exception):
    pass


def close_camera(camera):
    camera.release()
    cv2.destroyAllWindows()


# Reading barcode algorithm
def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        # Record the barcode into a file
        with open("barcode_result.txt", mode='w') as file:
            file.write(barcode_info)
        raise FoundBarcode
    return frame


def scan_for_barcode(device):
    # Camera feed connects to network camera on phone
    if device == "":
        # Use web cam (default)
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    else:
        url = f"{device}/video"
        camera = cv2.VideoCapture(url)



    # To use web cam (default web cam on device):
    #

    ret, frame = camera.read()
    try:
        # Loop searching for Barcode
        while ret:
            ret, frame = camera.read()
            frame = imutils.resize(frame, width=800, height=600)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, "Press ESC to exit", (250, 50), font, 1.0,
                         (255, 255, 255), 1)
            frame = read_barcodes(frame)
            cv2.imshow('Barcode/QR code reader', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        # Turn off video feed if user presses "Esc"
        close_camera(camera)

    except FoundBarcode:
        close_camera(camera)
        with open('barcode_result.txt') as f:
            lines = f.readlines()
        return int(lines[0])
