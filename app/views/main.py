import shutil
from pathlib import Path
from uuid import uuid4

from flask import render_template, current_app, send_from_directory, abort, request, flash, redirect
from werkzeug.utils import secure_filename

from app.functions.Integrate_DEG import integrate_DEG_cluster_wise
from app.functions.integrate_excel_files import integrate_excel
from app.main import main
from app.views.helpers import allowed_file, save_file, zip_files


@main.route('/')
def homepage():
    # severe_healthy_path = 'assets/Severe_vs_Healthy'
    # integrate_DEG_cluster_wise(severe_healthy_path, adj_p=0.05, logFC_cutoff=0.2, fill_zeros=True)
    # config = current_app.config
    # from_file = Path.joinpath(config['ASSETS_PATH'], 'from_file1_path.xlsx')
    # to_file = Path.joinpath(config['ASSETS_PATH'], 'past_to.xlsx')
    #
    # integrate_excel(from_file, to_file, columns_of_interest_from_file1=[3, 5], key_from_file1=1, key_to_file2=1,
    #                 starting_column_file2=3, new_column_name='Test', add_annotation="Gene location", add_report=True)

    return render_template('main/index.html')


@main.route('/applications', methods=('GET',))
def applications():
    return render_template('main/applications.html')


@main.route('/inegrate_deg', methods=('POST',))
def integrate_deg():
    req = request.form
    print(req)
    config = current_app.config

    if 'deg_files' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('deg_files')
    folder_name = str(uuid4())
    folder_path = Path.joinpath(config['UPLOAD_FOLDER'], folder_name)
    if files:
        # Create a directory to store the files

        if not Path.is_dir(folder_path): Path.mkdir(folder_path)

        for file in files:
            if file.filename == '':
                flash('No selected file', 'error')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(Path.joinpath(folder_path, filename))
            else:
                flash(f"Please upload the correct excel file - {file.filename}")

    try:
        adj_p = float(req.get('adj_p'))
    except ValueError:
        adj_p = 0.05
    try:
        logFC_cutoff = float(req.get('logFC_cutoff'))
    except ValueError:
        logFC_cutoff = 0.2
    fill_zeros = req.get('fill_zeros') == '1'

    # file_name = integrate_DEG_cluster_wise(str(folder_path), adj_p=0.05, logFC_cutoff=0.2, fill_zeros=True)
    file_name = integrate_DEG_cluster_wise(str(folder_path), adj_p=adj_p, logFC_cutoff=logFC_cutoff,
                                           fill_zeros=fill_zeros)
    try:
        shutil.rmtree(folder_path)
        return send_from_directory(config['OUTPUT_PATH'], filename=file_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@main.route('/integrate_excel_files', methods=('POST',))
def integrate_excel_files():
    data = request.form
    if 'from_file1_path' not in request.files or 'to_file2_path' not in request.files:
        flash('Please add all the files')
        return redirect(request.url)
    config = current_app.config

    saved_file_1_path = save_file(request.files.get('from_file1_path'))
    saved_file_2_path = save_file(request.files.get('to_file2_path'))

    file_name = integrate_excel(saved_file_1_path, saved_file_2_path, columns_of_interest_from_file1=[3, 5],
                                key_from_file1=1, key_to_file2=1,
                                starting_column_file2=3, new_column_name='Test', add_annotation="Gene location",
                                add_report=True)
    files = [str(Path.joinpath(config['OUTPUT_PATH'], file_name + '.xlsx'))]

    report_name = str(Path.joinpath(config['OUTPUT_PATH'], 'reports', file_name + '.txt'))
    files.append(report_name)

    zipped_filename = zip_files(files)
    try:
        return send_from_directory(config['OUTPUT_PATH'], filename=zipped_filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)
