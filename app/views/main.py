import shutil
from pathlib import Path
from uuid import uuid4

from flask import render_template, current_app, send_from_directory, abort, request, flash, redirect
from werkzeug.utils import secure_filename

from app.forms.front.main.ApplicationForms import ExcelToListForm
from app.functions.Convert_excel_to_list import file_to_network
from app.functions.Integrate_DEG import integrate_DEG_cluster_wise
from app.functions.integrate_excel_files import integrate_excel
from app.main import main
from app.views.helpers import allowed_file, save_file, zip_files


@main.route('/')
def homepage():
    return render_template('front/main/index.html')


@main.route('/applications', methods=('GET',))
def applications():
    return render_template('front/main/applications.html')


@main.route('/inegrate_deg', methods=('POST', 'GET'))
def integrate_deg():
    if request.method == 'GET':
        return render_template('front/main/integrate_GED.html')
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


@main.route('/integrate_excel_files', methods=('POST', 'GET'))
def integrate_excel_files():
    if request.method == 'GET':
        return render_template('front/main/integrate_excel.html')
    data = request.form.to_dict()

    if 'csv_file_1' not in request.files or 'csv_file_2' not in request.files:
        flash('Please modify_access all the files', 'error')
        return redirect(request.url)
    config = current_app.config

    # print(request.files.get('csv_file_1'))
    # print(data)
    # key_from_file2 = int(request.form.get('key_from_file_2'))
    # key_from_file1 = int(request.form.get('key_from_file_1'))
    # columns_of_interest_from_file1 = request.form.get('columns_of_interest_from_file1').split(',')
    # starting_column_file2 = int(request.form.get('starting_column_file_2'))

    try:
        saved_file_1_path = save_file(request.files.get('csv_file_1'))
        saved_file_2_path = save_file(request.files.get('csv_file_2'))
    except Exception:
        flash(' Make sure to modify_access the correct files', 'error')
        return redirect(request.url)
    try:
        columns_of_interest_from_file1 = list(int(x) for x in data.get('columns_of_interest_from_file1').split(','))
    except:
        flash('Column of interest is invalid. Please separate the columns by a comma(,)', 'error')
        return redirect(request.url)
    try:
        starting_column_file2 = int(data.get('starting_column_file_2'))
    except:
        flash('Starting column from file 2 must be an integer', 'error')
        return redirect(request.url)
    try:
        key_from_file1 = int(data.get('key_column_from_file_1'))
    except:
        flash('Key column from file 1 is invalid. make sure it is a number', 'error')
        return redirect(request.url)
    try:
        key_from_file2 = int(data.get('key_column_from_file_2'))
    except:
        flash('Key column from file 2 is invalid. make sure it is a number', 'error')
        return redirect(request.url)

    file_name = integrate_excel(saved_file_1_path, saved_file_2_path,
                                columns_of_interest_from_file1=columns_of_interest_from_file1,
                                key_from_file1=key_from_file1, key_to_file2=key_from_file2,
                                starting_column_file2=starting_column_file2, new_column_name='Test',
                                add_annotation="Gene location",
                                add_report=True)
    if not file_name:
        flash('An error occurred while integrating the files. Please check the input and try again', 'error')
        return redirect(request.url)
    files = [str(Path.joinpath(config['OUTPUT_PATH'], file_name + '.xlsx'))]

    report_name = str(Path.joinpath(config['OUTPUT_PATH'], 'reports', file_name + '.txt'))
    files.append(report_name)

    zipped_filename = zip_files(files)
    try:
        return send_from_directory(config['OUTPUT_PATH'], filename=zipped_filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@main.route('/excel_to_list', methods=('POST', 'GET'))
def excel_to_list():
    form = ExcelToListForm()
    if form.validate_on_submit():
        if 'file' not in request.files:
            flash('Excel file not uploaded', 'error')
            return redirect(request.url)
        config = current_app.config

        try:
            excel_file = save_file(request.files.get('file'))
        except Exception:
            flash('Make sure to modify_access the correct files', 'error')
            return redirect(request.url)
        file_name = file_to_network(excel_file, form.key_column.data, form.target_column.data, form.delimiter.data)
        if not file_name:
            flash('An error occurred while integrating the files. Please check the input and try again', 'error')
            return redirect(request.url)
        # file_path = str(Path.joinpath(config['OUTPUT_PATH'], file_name + '.xlsx'))
        try:
            return send_from_directory(config['OUTPUT_PATH'], filename=file_name, as_attachment=True)
        except FileNotFoundError:
            abort(404)

    return render_template('front/main/excel_to_list.html',form=form)


