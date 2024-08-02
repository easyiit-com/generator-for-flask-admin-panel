import functools
import logging
import os

from flask import Blueprint, request, render_template

from flask import g
from flask import redirect
from flask import session
from flask import url_for

from sqlalchemy import MetaData

from app.core.base_response import Response
from app.core.db import get_db, get_db_engine
from sqlalchemy import inspect

from app.plugins.generator.admin.config import Config
from app.plugins.generator.admin.utils import Generator

bp = Blueprint("generator", __name__, url_prefix="/admin/generator", template_folder="templates",static_folder='static')

@bp.route("/")
def index():
    engine = get_db_engine()
    inspector = inspect(engine)
    tables_list = inspector.get_table_names()
    return render_template("index2.jinja2", tables_list=tables_list)


@bp.route("/all_table")
def logout():
    engine = get_db_engine()
    inspector = inspect(engine)
    all_table_names = inspector.get_table_names()
    return Response.success(all_table_names)


@bp.route("/code", methods=("GET", "POST"))
def code():
    table_name = request.form.get("table_name")
    fields = request.form.get("fields",'*')
    engine = get_db_engine()
    data = Generator(engine,table_name).code(fields=fields)
    return Response.success(data)


@bp.route("/create_file", methods=("GET", "POST"))
def create_file():
    base_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    table_name = request.form.get("table_name")
    security_module = Config.SECURITY_MODULE
    if table_name =="-1":
        return Response.error(msg=f"Error,Please Select A Table")
    if table_name in security_module:
        return Response.error(msg=f"Error,{table_name} is security module")
    else:
        try:
            model_code_checked = int(request.form.get("model_code_checked",0))
            template_index_code_checked = int(request.form.get("template_index_code_checked",0))
            template_add_code_checked = int(request.form.get("template_add_code_checked",0))
            template_edit_code_checked = int(request.form.get("template_edit_code_checked",0))
            views_code_checked = int(request.form.get("views_code_checked",0))
            api_code_checked = int(request.form.get("api_code_checked",0))
            js_code_checked = int(request.form.get("js_code_checked",0))
            
            logging.error(f"{model_code_checked},{template_index_code_checked},{template_add_code_checked},{template_edit_code_checked},{views_code_checked},{api_code_checked},{js_code_checked}")
            
            model_code = request.form.get("model_code")
            template_index_code = request.form.get("template_index_code")
            template_add_code = request.form.get("template_add_code")
            template_edit_code = request.form.get("template_edit_code")
            views_code = request.form.get("views_code")
            api_code = request.form.get("api_code")
            js_code = request.form.get("js_code")
    
            model_file = f"{table_name}.py"

            template_index_path = f'templates/admin/{table_name.replace("_", "/", 1)}'
            template_add_path = f'templates/admin/{table_name.replace("_", "/", 1)}'
            template_edit_path = f'templates/admin/{table_name.replace("_", "/", 1)}'

            views_file = f"{table_name}.py"
            api_file = f"{table_name}.py"
            js_file = f"{table_name}.js"

            model_path = os.path.abspath(os.path.join(base_dir, "models", model_file))

            os.makedirs(os.path.join(base_dir, template_index_path), exist_ok=True)

            template_index_path = os.path.abspath(
                os.path.join(base_dir, template_index_path, "index.jinja2")
            )

            template_add_path = os.path.abspath(
                os.path.join(base_dir, template_add_path, "add.jinja2")
            )

            template_edit_path = os.path.abspath(
                os.path.join(base_dir, template_edit_path, "edit.jinja2")
            )

            views_path = os.path.abspath(os.path.join(base_dir, "views/admin", views_file))
            
            api_path = os.path.abspath(os.path.join(base_dir, "api/v1", views_file))
            
            js_path = os.path.abspath(
                os.path.join(base_dir, "static/assets/js/backend", js_file)
            )
            

            if model_code_checked ==1:
                with open(model_path, "w") as new_file:
                    new_file.write(model_code)
                    
            if template_index_code_checked ==1:        
                with open(template_index_path, "w") as new_file:
                    new_file.write(template_index_code)
            
            if template_add_code_checked ==1:          
                with open(template_add_path, "w") as new_file:
                    new_file.write(template_add_code)
            
            if template_edit_code_checked ==1:      
                with open(template_edit_path, "w") as new_file:
                    new_file.write(template_edit_code)
            
            if views_code_checked ==1:     
                with open(views_path, "w") as new_file:
                    new_file.write(views_code)
            
            if api_code_checked ==1:      
                with open(api_path, "w") as new_file:
                    new_file.write(api_code)
            
            if js_code_checked ==1:      
                with open(js_path, "w") as new_file:
                    new_file.write(js_code)

        except ValueError as e:
            return Response.error(e)
        return Response.success()
