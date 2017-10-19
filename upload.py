from flask import Blueprint, request, Response
import os
import json


IMAGE_UPLOAD_DIR = 'static/img/ImageUploads/'
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), IMAGE_UPLOAD_DIR)
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


upload_blueprint = Blueprint('upload', __name__)


@upload_blueprint.route('/upload_img', methods=['POST'])
def upload_img():
    f = request.files.get('blog_img')
    if f:
        filename = f.filename
        file_dir = os.path.join(os.path.dirname(__file__), UPLOAD_FOLDER)
        print(file_dir)
        if not os.path.exists(file_dir): os.makedirs(file_dir)
        f.save(os.path.join(file_dir, filename))
        imgUrl = request.url_root + IMAGE_UPLOAD_DIR + filename
        return json.dumps({'url': imgUrl})
    else:
        result = r"error|未成功获取文件，上传失败"
        res = Response(result)
        res.headers["ContentType"] = "text/html"
        res.headers["Charset"] = "utf-8"
        return res
