from flask import Flask, render_template, flash, redirect, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import FileField, SelectField
from wtforms.fields import ColorField
from werkzeug.utils import secure_filename
from PIL import Image
import os
import uuid
import requests, json
from pprint import pprint
from io import BytesIO
import random
from filters import negative_filter, grayscale_filter, sepia_filter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ott3r' 
app.config['UPLOAD_FOLDER'] = 'static/uploads'
bootstrap = Bootstrap5(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class HeaderForm(FlaskForm):
    header_text = StringField('Header Text', validators=[DataRequired()])

class FooterForm(FlaskForm):
    footer_text = StringField('Footer Text', validators=[DataRequired()])

class ImageUploadForm(FlaskForm):
    image = FileField('Upload an Image')

class SearchImageForm(FlaskForm):
    search_text = StringField('Search Image')
    header_text = StringField(
        'Header Text', validators=[DataRequired()]
    )

#updates 4/30:
class HeaderColorForm(FlaskForm):
    header_color = ColorField(
        'Header Text Color'
    )

class FooterColorForm(FlaskForm):
    footer_color = ColorField(
        'Footer Text Color'
    )

'''
class ImageFilterForm(FlaskForm):
    image_filter = StringField(
        'Image Filter'
    )
'''

class ImageFilterForm(FlaskForm):
    image_filter = SelectField('Image Filter', choices=[
        ('none', 'No Filter'),
        ('negative_filter', 'Negative'),
        ('grayscale_filter', 'Grayscale'),
        ('sepia_filter', 'Sepia')
    ])

current_settings = {
    'header_text': 'Header Text',
    'footer_text': 'Footer Text',
    'searched_image': None,
    'searched_image_url': None,
    #update
    'header_color': '#000000',
    'footer_color': '#000000',
    'user_image_filename': None,
    'image_filter': None
}

@app.route('/', methods=['GET', 'POST'])
def index():
    header_form = HeaderForm()
    footer_form = FooterForm()
    imageupload_form = ImageUploadForm()
    search_image_form = SearchImageForm()
    #update
    headercolor_form = HeaderColorForm()
    footercolor_form = FooterColorForm()
    image_filter_form = ImageFilterForm()

    if request.method == 'POST':
        if header_form.header_text.data:
            current_settings['header_text'] = header_form.header_text.data

        if footer_form.footer_text.data:
            current_settings['footer_text'] = footer_form.footer_text.data
        
        #update
        if headercolor_form.header_color.data:
            current_settings['header_color'] = headercolor_form.header_color.data

        if footercolor_form.footer_color.data:
            current_settings['footer_color'] = footercolor_form.footer_color.data


        if imageupload_form.image.data:
            image_file = imageupload_form.image.data
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_settings['user_image_filename'] = filename

        if search_image_form.search_text.data:
            page_num = random.randint(0, 10) * random.randint(0, 10)
            current_settings['searched_image'] = search_image_form.search_text.data
            url = f"https://api.unsplash.com/search/photos?page={page_num}&query={current_settings['searched_image']}"
            headers = {
                "Accept-Version": "v1",
                "Authorization": "Client-ID 9A5ot-o2F1PHh8ERLsxH09Fls1g8rQP9T2CH4bE3jFQ"
            }
            try:
                r = requests.get(url, headers=headers)
                data = r.json()
                image_url = data['results'][0]['urls']['regular']
                current_settings['searched_image_url'] = image_url

                image_response = requests.get(image_url)
                img = Image.open(BytesIO(image_response.content))
                img.save("static/uploads/img.jpg")
                
            except:
                print('please try again')

        if image_filter_form.image_filter.data:
            current_settings['image_filter'] = image_filter_form.image_filter.data
            img = Image.open('static/uploads/img.jpg')
            if current_settings['image_filter'] == "negative_filter":
                #img = Image.open('static/uploads/img.jpg')
                negative_filter(img)
            elif current_settings['image_filter'] == "grayscale_filter":
                #img = Image.open('static/uploads/img.jpg')
                grayscale_filter(img)
            elif current_settings['image_filter'] == "sepia_filter":
                #img = Image.open('static/uploads/img.jpg')
                sepia_filter(img)
            elif current_settings['image_filter'] == "No Filter":
                # After image upload or search
                current_settings['image_filter'] = None

            img.save('static/uploads/new.jpg')


    return render_template('index.html', 
                           header_form=header_form, 
                           footer_form=footer_form,
                           imageupload_form=imageupload_form,
                           search_image_form=search_image_form,
                           #update
                           headercolor_form=headercolor_form,
                           footercolor_form=footercolor_form,
                           image_filter_form=image_filter_form,
                           settings=current_settings)

if __name__ == '__main__':
    app.run(debug=True)