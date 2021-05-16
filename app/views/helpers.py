from pathlib import Path
import glob
import os
import time
from pathlib import Path
from uuid import uuid4
from zipfile import ZipFile

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


def allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def allowed_image_extensions(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_IMAGE_FILES']


def save_file(file: FileStorage, folder_path: str = '',return_filename:bool=False) -> str:
    if not folder_path:
        folder_path = current_app.config['UPLOAD_FOLDER']
    if file.filename == '':
        print("Wrong Filename")
        raise Exception

    if file and (allowed_file(file.filename) or allowed_image_extensions(file.filename)):
        filename = str(uuid4()) + '-' + secure_filename(file.filename)
        file_path = Path.joinpath(folder_path, filename)
        file.save(file_path)
        if return_filename:
            return filename
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


def delete_files(app):
    config = app.config
    now = time.time()

    folders = [config['OUTPUT_PATH'], config['UPLOAD_FOLDER'], str(Path.joinpath(config['OUTPUT_PATH'], 'reports'))]
    thirty = 60 * 30
    file_extensions = ('*.xlsx', '*.txt', '*.zip',)

    for folder in folders:
        print(folder)
        files = []
        for ext in file_extensions:

            try:
                print(glob.glob(str(Path.joinpath(folder, ext))))
                files.extend(glob.glob(str(Path.joinpath(folder, ext))))
            except AttributeError:
                pass
        print(files)
        for filename in files:
            if (now - os.stat(filename).st_mtime) > thirty:
                os.remove(filename)
                # command = f"rm {filename}"
                # subprocess.call(command, shell=True)
                print(f"removed {filename}")
