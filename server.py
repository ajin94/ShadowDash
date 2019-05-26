# import json, os, shutil
from flask import Flask, request
from flask import render_template
from flask_wtf.csrf import CsrfProtect
from connections import get_connection_to
# import traceback
# from PIL import Image

shadowdashapp = Flask(__name__)
shadowdashapp.secret_key = '6wfwef6AqwdwqdSDW67waedccscaQDWD6748wdFD'
shadowdashapp.config['SESSION_TYPE'] = 'filesystem'
shadowdashapp.config['WTF_CSRF_SECRET_KEY'] = 'asdaC34VERV6843CsC#$@d#$@%fewd#22342FWFQE'
csrf = CsrfProtect()
csrf.init_app(shadowdashapp)


@shadowdashapp.route('/')
def shadowdash():
    comment_count_query = "SELECT count(*) FROM user"
    try:
        cursor, conn = get_connection_to(db_name='sf')
        comment_count_obj = cursor.execute(comment_count_query)
        if comment_count_obj:
            ((signup_user_count,),) = cursor.fetchall()
    except Exception as e:
        pass

    template_dict = {
        "signup_count": signup_user_count
    }
    return render_template('dashpages/shadowfashion/index.html', template_data=template_dict)


@shadowdashapp.route('/shadowdashsignups')
def shadowdashsignups():
    user_data_dict = {}
    signups_query = """SELECT u.id, ac.type, u.fname, u.sname, u.gender, u.dob, 
    u.email, u.phone_number, u.house_apt, u.district, u.city, u.state, u.pin, 
    u.created_date FROM user u INNER JOIN account_types ac ON u.account_type_id=ac.id"""
    try:
        cursor, conn = get_connection_to(db_name='sf')
        user_data_obj = cursor.execute(signups_query)
        if user_data_obj:
            data = cursor.fetchall()
            if data:
                for (id, account, fname, sname, gender, dob, email,
                     phone, house, district, city, state, pin, date) in data:
                    address_line_1 = f"{house}, {district}"
                    address_line_2 = f"{city}, {state}, {pin}"
                    user_data_dict[id] = (account, fname, sname, gender, dob, email,
                                          phone, address_line_1, address_line_2, date)
    except Exception as e:
        user_data_dict = {}
    return render_template('dashpages/shadowfashion/signups.html', logins=user_data_dict)


# @dashapp.route('/nsdashquery')
# def nsdashquery():
#     query_dict = {}
#     comment_query = "SELECT id, name, email, query FROM query"
#     try:
#         cursor, conn = get_connection_to(db_name='sf')
#         comment_data_obj = cursor.execute(comment_query)
#         if comment_data_obj:
#             data = cursor.fetchall()
#             query_dict = {id: (name, email, query) for (id, name, email, query) in data}
#     except Exception as e:
#         query_dict = {}
#     return render_template('dashpages/shadowfashion/query.html', queries_received=query_dict)
#
#
# @dashapp.route('/nsdashimage')
# def nsdashimage():
#     template_return_dict = {}
#     image_info_dict = {}
#     category_info_dict = {}
#     image_path_info_query = "SELECT i.id, i.image_name, ic.image_for FROM image i INNER JOIN image_category ic on i.image_for=ic.id"
#     image_category_info_query = "SELECT id, image_for FROM image_category"
#     try:
#         cursor, conn = get_connection_to(db_name='sf')
#         # getting image paths
#         image_path_info_obj = cursor.execute(image_path_info_query)
#         if image_path_info_obj:
#             data = cursor.fetchall()
#             image_info_dict = {id: (path, image_for) for (id, path, image_for) in data}
#         # getting image categories
#         image_category_info_obj = cursor.execute(image_category_info_query)
#         if image_category_info_obj:
#             data = cursor.fetchall()
#             category_info_dict = {id: image_for for id, image_for in data}
#     except Exception as e:
#         image_info_dict = {}
#         category_info_dict = {}
#     template_return_dict['image_info'] = image_info_dict
#     template_return_dict['category_info'] = category_info_dict
#     return render_template('dashpages/shadowfashion/image.html', template_info=template_return_dict)
#
#
# @dashapp.route('/_upload_image', methods=["POST"])
# def upload_image():
#     file_to_upload = request.files.get('image_files', None)
#     image_for = request.form.get('image_category', None)
#     if file_to_upload:
#         filename = file_to_upload.filename.replace(" ", "")
#         try:
#             cursor, conn = get_connection_to('sf')
#             insert_query = "INSERT INTO image (image_name, image_for) VALUES (%s,%s)"
#             args = (filename, int(image_for))
#             cursor.execute(insert_query, args)
#             conn.commit()
#             dash_path_string = "/media/ajin/Drive/MX-Work/Dashboard/static/images"
#             ns_path_string = "/media/ajin/Drive/MX-Work/NSInterios/static/images"
#             # dash_path_string = "/home/mxp/projects/Dashboard/static/images"
#             # ns_path_string = "/home/mxp/projects/ShadowFashion/static/images"
#             try:
#                 # uploading files to server
#                 file_to_upload.save(os.path.join(dash_path_string, filename))
#                 file_name_string = "{0}/{1}".format(dash_path_string, filename)
#                 # resizing image with python
#                 image_obj = Image.open(file_name_string)
#                 quality_val = 90
#                 image_obj.save(file_name_string, 'JPEG', quality=quality_val)
#                 shutil.copy(file_name_string, ns_path_string)
#             except Exception as e:
#                 pass
#         except Exception as e:
#             pass
#     return json.dumps({"status": "OK"})
#
#
# @dashapp.route('/_delete_image', methods=["POST"])
# def delete_image():
#     image_name = request.form.get('image_name', None)
#     image_id = int(request.form.get('image_id', None))
#
#     if image_name and image_id:
#         try:
#             cursor, conn = get_connection_to('sf')
#             delete_query = "DELETE FROM image WHERE id=%s"
#             args = (image_id,)
#             cursor.execute(delete_query, args)
#             conn.commit()
#         except Exception as e:
#             return json.dumps({"status": str(traceback.format_exc())})
#         else:
#             dash_path_string = "/media/ajin/Drive/MX-Work/Dashboard/static/images"
#             ns_path_string = "/media/ajin/Drive/MX-Work/NSInterios/static/images"
#             # dash_path_string = "/home/mxp/projects/Dashboard/static/images"
#             # ns_path_string = "/home/mxp/projects/ShadowFashion/static/images"
#             try:
#                 os.remove("{0}/{1}".format(dash_path_string, image_name))
#                 os.remove("{0}/{1}".format(ns_path_string,image_name))
#             except Exception as e:
#                 return json.dumps({"status": str(traceback.format_exc())})
#
#     return json.dumps({"status": "OK"})


# if __name__ == "__main__":
#     shadowdashapp.run('0.0.0.0', '9879')
