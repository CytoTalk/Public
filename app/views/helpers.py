from pathlib import Path
from uuid import uuid4
from zipfile import ZipFile

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


def allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_file(file: FileStorage, folder_path: str = '') -> str:
    if not folder_path:
        folder_path = current_app.config['UPLOAD_FOLDER']
    if file.filename == '':
        raise Exception

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = Path.joinpath(folder_path, filename)
        file.save(file_path)
        return file_path
    else:
        raise Exception


def zip_files(file_paths=None, output_folder: str = '') -> str:
    if file_paths is None:
        file_paths = []
    if not output_folder:
        output_folder = current_app.config['OUTPUT_PATH']
    file_name = str(uuid4()) + '.zip'
    with ZipFile(Path.joinpath(output_folder, file_name), 'w') as zipfile:
        for file in file_paths:
            arcname = 'Generated.xlsx' if '.xlsx' in file else 'Report.txt'
            zipfile.write(file, arcname)
    return file_name
