from pathlib import Path

from flask import render_template, current_app

from app.functions.integrate_excel_files import integrate_excel
from app.main import main


@main.route('/')
def homepage():
    # severe_healthy_path = 'assets/Severe_vs_Healthy'
    # integrate_DEG_cluster_wise(severe_healthy_path, adj_p=0.05, logFC_cutoff=0.2, fill_zeros=True)
    config = current_app.config
    from_file = Path.joinpath(config['ASSETS_PATH'], 'from_file1_path.xlsx')
    to_file = Path.joinpath(config['ASSETS_PATH'], 'past_to.xlsx')

    integrate_excel(from_file, to_file, columns_of_interest_from_file1=[3, 5], key_from_file1=1, key_to_file2=1,
                    starting_column_file2=3, new_column_name='Test', add_annotation="Gene location", add_report=True)

    return render_template('main/index.html')
