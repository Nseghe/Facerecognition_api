from flask import current_app as app, make_response, request, redirect, render_template, jsonify, flash
from flask_cors import CORS
from application.facerecog import calc_dist
import os
from PIL import Image
from io import BytesIO
import base64

CORS(app)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/compare', methods=['POST', 'OPTIONS'])
def compare():
	if request.method == 'OPTIONS':
		return _build_cors_prelight_response()
	if request.method == 'POST':
		print(request.method)
		images = request.get_json()
		# check if the post request has the files part
		if 'image1' not in images or 'image2' not in images:
			message = 'No images to compare'
		else:
			image1 = images['image1']
			image2 = images['image2']
			result = calc_dist(image1,image2) < 1
			message = result
		return _corsify_actual_response(jsonify({'result':message}))
  
def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response
def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
