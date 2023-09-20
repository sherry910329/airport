# -*- coding: utf-8 -*-
from odoo import fields, models, api
import pytesseract
from PIL import Image
import io
import logging
import base64
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\odoo16\server\Tesseract-OCR\tesseract.exe'

class ImageCapture(models.TransientModel):
    _name = 'image.capture'
    _description = 'Image Captures'

    name = fields.Char(string='Name',help='Name of the image to capture')
    model_name = fields.Char(string='Model Name',  default='image.capture',  help="For getting the model name details")
    record_id = fields.Integer(string='Record ID', help="For getting the record ID details", default=1)
    field_name = fields.Char(string='Field Name', default='image_field', help="Field name for uploading the image")
    ocr_text_field = fields.Text(string='OCR Text', help='Recognized text from OCR')
    image_field = fields.Binary(string='Image Field', help='Binary field to store the image')

    @api.model
    def perform_ocr(self, image_path):
        try:
            _logger = logging.getLogger(__name__)

            _logger.info("Attempting OCR...")

            _logger.info("Performing OCR for image data")

            img = Image.open(image_path)
            img = img.convert("RGB")

            _logger.info("Image opened successfully")

            recognized_text = pytesseract.image_to_string(img, lang='chi_tra+eng')
            #_logger.info("OCR successful. Recognized text: %s", recognized_text)
      
            if recognized_text:
                _logger.info(u"OCR text recognized: %s", recognized_text)
                return recognized_text  # 返回识别的文本
            else:
                _logger.info(u"No text recognized by OCR")
                return None
        except Exception as e:
            _logger.error("Error during OCR: %s", e)
            recognized_text = ""
            _logger.error("OCR error: %s", e)
            return {'error': str(e)}  # 返回错误信息
        
    
    def ensure_base64_padding(self, data):
        data = data.replace(" ", "").replace("\n", "")
        padding_length = len(data) % 4
        if padding_length == 1:
            data += '=='
        elif padding_length == 2:
            data += '='
        return data

    def action_save_image(self, data, url):
        _logger = logging.getLogger(__name__)
        _logger.info("Received model_name: %s", data['model_name'])
        image = url.split(',')[1]  # 提取 Base64 部分
        image = self.ensure_base64_padding(image)  # 确保填充

        try:
            # 創建圖片檔案的檔名，使用遞增的 record_id
            record_id = int(data['record_id'])
            image_filename = f'image_{record_id}.png'
            temp_image_path = os.path.join('C:\\odoo16\\server\\odoo\\addons\\airport\\static\\img', image_filename)
            _logger.info("temp_image_path: %s", temp_image_path)

            # 創建目标文件夹，如果不存在
            os.makedirs(os.path.dirname(temp_image_path), exist_ok=True)

            with open(temp_image_path, 'wb') as temp_image_file:
                temp_image_file.write(base64.b64decode(image))  # 解码并保存图像

            recognized_text = self.perform_ocr(temp_image_path)  # 传递图像路径进行 OCR

            # 在這裡添加保存圖片的邏輯
            model = self.env[data['model_name']]
            field_name = data['field_name']
            model_record = model.browse(record_id)

            model_record.sudo().write({
                data['field_name']: image
            })

            #static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
            #img_folder = os.path.join(static_folder, 'img')
            image_path = temp_image_path

            original_image = Image.open(temp_image_path)
            original_image.save(image_path, 'PNG')
            _logger.info("Image saved and converted to PNG format")

            self.write({
                'ocr_text_field': recognized_text
            })

            with open(temp_image_path, 'rb') as temp_image_file:
                temp_image_data = base64.b64encode(temp_image_file.read()).decode('utf-8')

            return {'temp_image_data': temp_image_data}
        except Exception as e:
            _logger.error("Error while saving image and performing OCR: %s", e)
            _logger.exception(e)  # 记录完整的异常信息


    @api.model
    def action_get_temp_image_data(self, record_id):
        _logger = logging.getLogger(__name__)
        _logger.info("Calling action_get_temp_image_data function...")

        try:
            # 递增record_id以获取正确的图像文件
            record_id = int(record_id)
            image_filename = f'image_{record_id}.png'
            image_path = os.path.join('C:\\odoo16\\server\\odoo\\addons\\airport\\static\\img', image_filename)

            _logger.info("image_path: %s", image_path)
            with open(image_path, 'rb') as image_file:
                image_binary_data = image_file.read()

            # 将二进制数据编码为Base64字符串
            image_data_base64 = base64.b64encode(image_binary_data).decode('utf-8')

            _logger.info("Received temp_image_data for record: %s", record_id)
            return {'temp_image_data': image_data_base64}
        except Exception as e:
            _logger.error("Error while getting temp image data: %s", e)
            return {'error': str(e)}