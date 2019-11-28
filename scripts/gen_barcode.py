import barcode
from io import StringIO
from barcode.writer import ImageWriter
import cv2
import csv
from fpdf import FPDF

class CsvEntry:
  def __init__(self, item_n, lot_n, fpg_input, barcode, qty, color):
    self.item_n = item_n
    self.lot_n = lot_n
    self.fpg_input = fpg_input
    self.barcode = barcode
    self.qty = qty
    self.color = color.lower()

## Create png barcode image from sn
def writeBaseBarcodeImage(sn):
  EAN = barcode.get_barcode_class('ean13')
  ean = EAN(sn, writer=ImageWriter())
  file_name = ean.save('ean13_barcode')
  return file_name

# read base png barcode image back in, opencv format
def loadBaseBarcodeImage(filename):
  return cv2.imread(filename)

def padImage(img):
  # pad image
  left_pad = 10
  right_pad = 10
  top_pad = 10
  bottom_pad = 10
  formatted_img = cv2.copyMakeBorder(
    img,
    top=top_pad,
    bottom=bottom_pad,
    left=left_pad,
    right=right_pad,
    borderType=cv2.BORDER_CONSTANT,
    value=[255,255,255]
  )
  return formatted_img

#format base barcode image w/ padding, text overlays etc... from input data
def overlayText(img, data):
  # add text
  rows,cols,_ = img.shape
  font = cv2.FONT_HERSHEY_SIMPLEX
  ll_corner = (0, rows)
  fontScale              = 1
  fontColor              = (0,0,0)
  lineType               = 2
  cv2.putText(img, data.item_n, 
      ll_corner, 
      font, 
      fontScale,
      fontColor,
      lineType)
  return img

ColorMap = {"red" : [0,0,255], "blue" : [255,0,0], "green" : [0,255,0], "yellow" : [0, 255, 255]}
def applyColor(img, data):
  width = 50
  rows,cols,_ = img.shape
  img[0:rows, cols-width : cols] = ColorMap[data.color]
  return img

def writeFormattedImage(file_name, img):
  out_dir = "./out/"
  path = out_dir + "formatted." + file_name + ".png"
  cv2.imwrite(path, img)
 
def add_image(image_path):
  pdf = FPDF()
  pdf.add_page()
  pdf.image(image_path, x=10, y=8, w=100)
  pdf.set_font("Arial", size=12)
  pdf.ln(85)  # move 85 down
  pdf.cell(200, 10, txt="{}".format(image_path), ln=1)
  pdf.output("add_image.pdf")

# run pipeline to generate png image for CsvEntry data
def processCsvEntry(data):
  base_image_path = writeBaseBarcodeImage(data.barcode)
  img = loadBaseBarcodeImage(base_image_path)
  img = padImage(img)
  img = overlayText(img, data)
  img = applyColor(img, data)
  writeFormattedImage(data.item_n, img) 

def loadCsv(file_path):
  csv_entries = []
  with open(file_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    first = True 
    for row in csv_reader:
      if first:
        first = False
        continue
      print(row)
      entry = CsvEntry(row[0], row[1], row[2], row[3], row[4], row[5])
      csv_entries.append(entry)
  return csv_entries

if __name__ == "__main__":
  csv_entries = loadCsv('data/example.csv')
  for csv_entry in csv_entries:
    processCsvEntry(csv_entry)
