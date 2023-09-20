/** @odoo-module */

import { registry } from '@web/core/registry';
import { formView } from '@web/views/form/form_view';
import { FormController } from '@web/views/form/form_controller';
import { FormRenderer } from '@web/views/form/form_renderer';
import  rpc  from 'web.rpc';
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { web } from 'web.core';

patch(FormRenderer.prototype, 'FormRender', {
    requestId: 1, // 添加 requestId 属性，并初始化为 0
    setup() {
        this._super();
        this.notification = useService("notification");
        this.capturedImageUrl = "";
        this.props.record.data.record_id = 0; // 可以根據需求設置初始值
        this.requestId = Math.floor(Math.random() * 100000); // 创建唯一的请求 ID
        this.renderer = this; // 將 renderer 設置為 this
        this.ocrExecuted = false; // 添加一个标志变量，初始值为 false
    },

    reload() {
        // 实现重新加载视图的逻辑
        // 可以是重新渲染组件、重新请求数据等
    },

    async OnClickOpenCamera() {
        var player = document.getElementById('player');
        var captureButton = document.getElementById('capture');
        var camera = document.getElementById('camera');
        player.classList.remove('d-none');
        captureButton.classList.remove('d-none');
        camera.classList.add('d-none');

        await this.props.record.__focus;
       // console.log("Record ID in OnClickOpenCamera:", newRecordId);

       //console.log("Record ID in OnClickOpenCamera:", this.props.record.data.record_id);

        let stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        player.srcObject = stream;
    },

    async OnClickCaptureImage() {
            var context = snapshot.getContext('2d');
            var canvas = document.getElementById('snapshot');
            var save_image = document.getElementById('save_image');
            var image = document.getElementById('image');
            var video = document.getElementById('video');
            var camera = document.getElementById('camera');
            var scanButton = document.getElementById('scan');
            save_image.classList.remove('d-none');
            scanButton.classList.remove('d-none');
            context.drawImage(player, 0, 0, 320, 240);
            // 添加下面这行代码来检查图像数据的长度
            console.log("Captured image data length:", context.canvas.toDataURL("image/png").length);
            // 在捕获图像后
            console.log("Captured image data:", context.canvas.toDataURL("image/png"));


            image.value = context.canvas.toDataURL("image/png");
            canvas.classList.remove('d-none');
            this.url = context.canvas.toDataURL();
            this.capturedImageUrl = context.canvas.toDataURL();
            this.props.value = context.canvas.toDataURL();
           // console.log("Captured image data:", image.value);
           // console.log("Captured image:", this.props.value);
           // console.log("Record ID in OnClickCaptureImage:", this.props.record.data.record_id);
           // console.log("Image data saved successfully:", image.value);
            // Clear OCR text field
            this.props.record.data.ocr_text_field = "";
    },
    

    async OnClickScanImage() {
      // 添加条件检查，仅当 OCR 未执行时才执行
      if (!this.ocrExecuted) {
          // 执行 OCR 操作
          try {
              console.log("This context in OnClickScanImage:", this);
              // 生成唯一的请求 id
              const requestId = this.requestId;
  
              // 创建请求对象，并设置唯一的 "id" 值
              const request = {
                  jsonrpc: "2.0",
                  method: "call",
                  params: {
                      model: "image.capture",
                      method: "action_get_temp_image_data",
                      args: [this.props.record.data.record_id],
                      kwargs: {},
                  },
                  id: requestId,
              };
  
              // 输出请求信息到控制台，以进行调试
              console.log("Request URL:", "/web/dataset/call_kw/image.capture/action_get_temp_image_data");
              console.log("Request Method:", "POST");
              console.log("Request Headers:", {
                  "Content-Type": "application/json",
              });
              console.log("Request Body:", JSON.stringify(request));
  
              // 发送请求
              const response = await fetch("/web/dataset/call_kw/image.capture/action_get_temp_image_data", {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/json",
                  },
                  body: JSON.stringify(request),
              });
  
              if (response.ok) {
                  const imageDataResult = await response.json();
  
                  if (imageDataResult.id === requestId) {
                      console.log("Response data from server:", imageDataResult);
  
                      if (imageDataResult.result && imageDataResult.result.temp_image_data) {
                        // 解码 base64 编码的图像数据
                        const decodedImageData = atob(imageDataResult.result.temp_image_data);
        
                        const ocrTextFieldElement = document.querySelector('[name="ocr_text_field"]');
                        if (ocrTextFieldElement) {
                            ocrTextFieldElement.value = decodedImageData; // 设置文本值
                        }
        
                        // 调用 performOCR 函数，将解码后的图像数据传递给它
                        const ocrResponse = await performOCR(decodedImageData, requestId);
        
                        if (ocrResponse && typeof ocrResponse.result === 'string') {
                            // 更新 OCR 文本字段的值
                            const ocrTextFieldElement = document.querySelector('[name="ocr_text_field"]');
                            if (ocrTextFieldElement) {
                                ocrTextFieldElement.value = ocrResponse.result;
                            }
                            console.log("Handling temp_image_data...");
                        } else {
                            console.error("OCR failed to recognize text.");
                        }
                    } else {
                        console.error("temp_image_data not found in the response.");
                    }
                  } else {
                      console.error("Mismatched response id:", imageDataResult.id);
                  }
              } else {
                  console.error("Network request failed");
              }
          } catch (error) {
              console.error("Error in OnClickScanImage:", error);
              console.error("Error details:", error.message, error.stack);
          }
      }
  },
  
    
  async OnClickSaveImage() {
    try {
        const requestId = this.requestId; // 生成唯一的请求 id
        const imageData = this.props.value;

        if (!imageData) {
            console.error('Image data is empty or invalid.');
            return;
        }

        // 递增 record_id
        this.props.record.data.record_id++;

        const result = await fetch('/web/dataset/call_kw/image.capture/action_save_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                jsonrpc: '2.0',
                method: 'call',
                params: {
                    model: 'image.capture',
                    method: 'action_save_image',
                    args: [[], this.props.record.data, this.url], // 使用 this.url 作为图像数据
                    kwargs: {},
                },
                id: requestId, // 使用相同的请求 id
            }),
        });

        if (result.ok) {
            const responseData = await result.json();
            console.log('Response data from server:', responseData);

            if (responseData && responseData.error) {
                console.error('Error while saving image and performing OCR:', responseData.error);
            } else {
                console.log('Image saved successfully');

                // 检查是否已经执行过 performOCR
               // if (!this.props.record.data.ocr_text_field) {
                 //   await this.OnClickScanImage();
               // }
            }
        } else {
            console.error('Network request failed');
        }
    } catch (error) {
        console.error('Error while saving image and performing OCR:', error);
    }
}

});


async function performOCR(imageData, requestId) {
  try {
      console.log("performOCR called from:", new Error().stack);
      const response = await fetch('/web/dataset/call_kw/image.capture/perform_ocr', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              jsonrpc: '2.0',
              method: 'call',
              params: {
                  model: 'image.capture',
                  method: 'perform_ocr',
                  args: [imageData],
                  kwargs: {},
              },
              id: requestId,
          }),
      });

      if (response.ok) {
          const ocrResponse = await response.json();
          console.log("OCR Response:", ocrResponse);

          // 处理 OCR 结果中的空字符
          if (ocrResponse && ocrResponse.result && typeof ocrResponse.result === 'string') {
              const cleanedText = ocrResponse.result.replace(/\0/g, ''); // 去除空字符
              ocrResponse.result = cleanedText; // 更新 OCR 结果
          } else {
              ocrResponse.result = ""; // 如果不是字符串，将结果设置为空字符串
          }

          return ocrResponse;
      } else {
          console.error('Network request failed');
      }
  } catch (error) {
      console.error('OCR error:', error);
      throw error;
  }
}


