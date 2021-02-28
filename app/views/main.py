from flask import render_template

from app.functions.Integrate_DEG import integrate_DEG_cluster_wise
from app.main import main


@main.route('/')
def homepage():
    severe_healthy_path = 'assets/Severe_vs_Healthy'
    integrate_DEG_cluster_wise(severe_healthy_path, adj_p=0.05, logFC_cutoff=0.2, fill_zeros=True)
    return render_template('main/index.html')
