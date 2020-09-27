import codecs

from flask import Flask, jsonify, request, session , make_response
from flaskext.mysql import MySQL
#from flask_bcrypt import Bcrypt
import hashlib
import datetime
import base64
from Crypto.Cipher import AES
from Crypto import Random
from pprint import pprint
import cgi
import os
from flask import request
import socket



#import hashlib

app = Flask(__name__)
app1 = Flask(__name__)
#app.config['TESTING'] = True
#bcrypt = Bcrypt(app)
mysql = MySQL()
mysql1 = MySQL()
mysql = MySQL(app)
mysql1 = MySQL(app1)
secretkey = "encryptme"

#----------------------MySQL configurations

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'university_info_system'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'




app1.config['MYSQL_DATABASE_USER'] = 'mgu_elegibility'
app1.config['MYSQL_DATABASE_PASSWORD'] = 'mgu3l3@)!&'
app1.config['MYSQL_DATABASE_DB'] = 'eligibility_db'
app1.config['MYSQL_DATABASE_HOST'] = '10.33.1.23'


#con1 = mdb.connect (host='localhost', user='root', passwd='root', db1='university_info_system')


mysql.init_app(app)
#mysql1.init_app(app1)

#--------------------------------add user------------------------------#



@app.route('/home1', methods=['POST', 'GET'])
def home1():
    conn = mysql1.connect()
    cur = conn.cursor()
    sql = "select * from affi_college_details_ug"
    cur.execute(sql)
    r = cur.fetchall()
    return jsonify(r)

    #return "<h1>UNIVERSITY INFORMATION SYSTEM</h1><p>API system developed as per the order from Higher Education, Kerala State</p>"




@app.route('/univ_details',methods=['POST', 'GET'])#-------------Get all the departments
def univ_details():
    try:
        if request.is_json:
            data = request.json
            hashkey = data['hashkey']
            univ_id = data['univ_id']
            conn = mysql.connect()
            cur = conn.cursor()
            sql = "select univ_id,univ_name,univ_address,univ_email,univ_phone_no,univ_image from univ_details where univ_id=%s"
            cur.execute(sql,(univ_id))
            r = cur.fetchall()
            #numrows = cur.rowcount
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}



@app.route('/univ_label',methods=['POST', 'GET'])#-------------Get all the departments
def univ_label():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            univ_id = data['univ_id']
            validate_res = validate_private_key(private_key)
            r=''
            if validate_res == 1:
                conn = mysql.connect()
                cur = conn.cursor()
                sql = "select univ_id,univ_name,univ_image from univ_details where univ_id=%s"
                cur.execute(sql,(univ_id))
                r = cur.fetchall()
                #numrows = cur.rowcount
            else :
                r=-5
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}





@app.route('/univ_list',methods=['POST', 'GET'])#-------------Get all the departments
def univ_list():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            validate_res = validate_private_key(private_key)
            r=''
            if validate_res == 1:
                conn = mysql.connect()
                cur = conn.cursor()
                sql = "select univ_id,univ_name,univ_image from univ_details"
                cur.execute(sql,())
                r = cur.fetchall()
                #numrows = cur.rowcount
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}



@app.route('/univ_centers',methods=['POST', 'GET'])#------------------Get all the departments
def univ_centers():
    try:
        if request.is_json:
            data = request.json
            univ_id = data['univ_id']
            private_key = data['private_key']
            validate_res = validate_private_key(private_key)
            r=''
            if validate_res == 1:
                cur = mysql.connect().cursor()
                cur.execute('''select univ_center_name,univ_center_address,univ_center_email,univ_center_phone from univ_centers  where univ_id=%s''',(univ_id))
                r = cur.fetchall()
                #print(cur._last_executed)
                #print(r)
            else :
                r=-5
            return jsonify(r)

    except Exception as e:
        return {'error': str(e)}



@app.route('/univ_dept',methods=['POST', 'GET'])#------------------Get all the departments
def univ_dept():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            univ_id = data['univ_id']
            r = ''
            validate_res = validate_private_key(private_key)
            if validate_res == 1:
                cur = mysql.connect().cursor()
                cur.execute('''select dept_name,dept_code,dept_address,dept_phone_no,dept_hod_name,dept_contact_no from univ_departments where univ_id =%s''',(univ_id))
                r = cur.fetchall()
            else :
                r = -5
            return jsonify(r)

    except Exception as e:
        return {'error': str(e)}




@app.route('/univ_colleges',methods=['POST', 'GET'])#------------------Get all the departments
def univ_colleges():
    try:
        if request.is_json:
            data = request.json
            univ_id = data['univ_id']
            clg_type = data['clg_type']
            private_key = data['private_key']
            r = ''
            validate_res = validate_private_key(private_key)
            if validate_res == 1:
                cur = mysql.connect().cursor()
                if clg_type != '':
                    cur.execute('''select college_name,college_code,college_address,college_district,college_phone_no ,college_principal_name,college_contact_no,univ_colg_id,college_type  from univ_colleges where univ_id=%s and college_type=%s''',(univ_id,clg_type))
                else :
                    cur.execute('''select college_name,college_code,college_address,college_district,college_phone_no ,college_principal_name,college_contact_no,univ_colg_id,college_type  from univ_colleges where univ_id=%s ''',(univ_id))
                r = cur.fetchall()
            else :
                r = -5
            return jsonify(r)

    except Exception as e:
        return {'error': str(e)}











@app.route('/get_role',methods=['POST', 'GET'])#-------------Get all the departments
def get_role():
    try:
        if request.is_json:
            data = request.json
            hashkey = data['hashkey']
            comp_hash = compare_hashkey(hashkey)
            r = []
            if comp_hash == 1:
                cur = mysql.connect().cursor()
                cur.execute("""select * from role_details where status = 'active'""")
                r = cur.fetchall()
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}


@app.route('/getselected_functions',methods=['POST', 'GET'])#-------------Get all the departments
def getselected_functions():
    try:
        if request.is_json:
            data = request.json
            hashkey = data['hashkey']
            comp_hash = compare_hashkey(hashkey)
            r = []
            if comp_hash == 1:
                conn = mysql.connect()
                cur = conn.cursor()
                sql = "select category_id,category_details from role_categories order by  category_details  asc"
                cur.execute(sql)
                r = cur.fetchall()
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}




@app.route('/assign_permission_action',methods=['POST', 'GET'])#-------------Get all the departments
def assign_permission_action():
    try:
        if request.is_json:
            data = request.json
            hashkey = data['hashkey']
            comp_hash = compare_hashkey(hashkey)
            retlast = 0
            if comp_hash == 1:
                roleid = data['roleid']
                func = data['sel_fun_array']
                prmsn = []
                ext = []
                conn = mysql.connect()
                cur = conn.cursor()
                sql = "select permission_id from role_permission_mapping where role_id= %s "
                cur.execute(sql,(roleid))
                r1 = cur.fetchall()
                if r1:
                    for valnew1 in r1:
                        ext.append(valnew1[0])
                else:
                    ret = 3  # second result null
                if len(func) == "" or len(func) == "":
                    sql = "delete from role_permission_mapping where role_id = %s"
                    cur.execute(sql, (roleid))
                    #$log_entry = "All access controll of '".$u_name. "' has removed by";
                else:
                    for val in func:
                        sql = "select a.category_id, a.function_id, b.dependency_id from role_permissions a, role_function_dependency b where a.permission_id = %s and b.func_id = a.function_id"
                        cur.execute(sql, (val))
                        r2 = cur.fetchall()

                        if r2:
                            for val2 in r2:
                                sql = "select permission_id from role_permissions where category_id = %s and function_id = %s"
                                cur.execute(sql, (val2[0],val2[2]))
                                r3 = cur.fetchall()

                                if r3:
                                    for val3 in r3:
                                        if val3[0] not in prmsn:
                                            prmsn.append(val3[0])
                                        diff1 = arraydifference(prmsn,ext)
                                        diff2 = arraydifference(ext,prmsn)
                                        diff = list(set(diff1+diff2))
                #print()


                for val4 in diff:

                    sql = "delete from role_permission_mapping where permission_id = %s and role_id= %s"
                    cur.execute(sql, (val4, roleid))
                    conn.commit()



                for val5 in prmsn:

                    sql = "select id from role_permission_mapping where permission_id= %s and role_id= %s"
                    cur.execute(sql, (val5, roleid))
                    r5 = cur.fetchall()
                    if r5:
                        print("hii")
                        #print(r5[0])
                        #print(val5)
                    elif val5 != "" :
                        sql = "insert into role_permission_mapping(permission_id,role_id,status)values(%s,%s,%s)"
                        cur.execute(sql, (val5, roleid, 'active'))
                        conn.commit()
                        print(cur._last_executed)
                        n = cur.lastrowid
                    #else r5 == "" and val5 != "":
                        #sql = "insert into role_permission_mapping(permission_id,role_id,status)values(%s,%s,%s)"
                        #cur.execute(sql, (val5, roleid, 'active'))
                        #conn.commit()
                        #print(cur._last_executed)
                        #n = cur.lastrowid

                return jsonify("1")
            else:
                return jsonify("2")

    except Exception as e:
        return {'error': str(e)}




@app.route('/remove_all_permissions',methods=['POST', 'GET'])#-------------Get all the departments
def remove_all_permissions():
    try:
        if request.is_json:
            data = request.json
            hashkey = data['hashkey']
            comp_hash = compare_hashkey(hashkey)
            #r = []
            if comp_hash == 1:
                roleid = data['roleid']
                conn = mysql.connect()
                cur = conn.cursor()
                sql = "delete from role_permission_mapping where role_id= %s"
                cur.execute(sql, (roleid))
                conn.commit()
                res = 1
            else:
                res = 2
        return jsonify(res)
    except Exception as e:
        return {'error': str(e)}



@app.route('/getcategory_details',methods=['POST', 'GET'])#-------------Get all the school
def getcategory_details():
    try:
        if request.is_json:
            data = request.json
            hashkey = data['hashkey']
            comp_hash = compare_hashkey(hashkey)
            r = []
            if comp_hash == 1:
                cur = mysql.connect().cursor()
                cur.execute("""select category_id,category_details from role_categories order by category_details  asc """)
                r = cur.fetchall()
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}



@app.route('/getcat_permission',methods=['POST', 'GET'])#-------------Get all the school
def getcat_permission():
    try:
        if request.is_json:
            data = request.json
            hashkey = data['hashkey']
            comp_hash = compare_hashkey(hashkey)
            r = []
            if comp_hash == 1:
                cur = mysql.connect().cursor()
                cur.execute("""select category_id,permission_id from role_permissions where function_id=1""")
                r = cur.fetchall()
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}




@app.route('/get_permission_mapping',methods=['POST', 'GET'])#-------------Get all the school
def get_permission_mapping():
    try:
        if request.is_json:
            data = request.json
            hashkey = data['hashkey']
            comp_hash = compare_hashkey(hashkey)
            r = []
            if comp_hash == 1:
                cur = mysql.connect().cursor()
                cur.execute("""select permission_id from role_permissions where function_id!=1""")
                r = cur.fetchall()
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}



@app.route('/getrole_permission_mapping',methods=['POST', 'GET'])#-------------Get all the departments
def getrole_permission_mapping():
    try:
        if request.is_json:
            data = request.json
            hashkey = data['hashkey']
            comp_hash = compare_hashkey(hashkey)
            r = []
            if comp_hash == 1:
                roleid = data['roleid']
                conn = mysql.connect()
                cur = conn.cursor()
                sql = "select permission_id from role_permission_mapping where role_id = %s order by id asc"
                cur.execute(sql,(roleid))
                r = cur.fetchall()
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}




@app.route('/getrole_permission_details',methods=['POST', 'GET'])#-------------Get all the departments
def getrole_permission_details():
    try:
        if request.is_json:
            data = request.json
            hashkey = data['hashkey']
            comp_hash = compare_hashkey(hashkey)
            r = []
            if comp_hash == 1:
                category_id = data['category_id']
                conn = mysql.connect()
                cur = conn.cursor()
                sql = "select  description,permission_id,category_id from role_permissions where category_id = %s order by  function_id asc"
                cur.execute(sql,(category_id))
                r = cur.fetchall()
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}




@app.route('/getrole_permission_dependency',methods=['POST', 'GET'])#-------------Get all the departments
def getrole_permission_dependency():
    try:
        if request.is_json:
            data = request.json
            hashkey = data['hashkey']
            comp_hash = compare_hashkey(hashkey)
            prmsn = []
            if comp_hash == 1:
                permission_id = data['permission_id']
                #prmsn = []
                conn = mysql.connect()
                cur = conn.cursor()
                sql = "select a.category_id,a.function_id,b.dependency_id from role_permissions a,role_function_dependency b where a.permission_id= %s and b.func_id=a.function_id"
                cur.execute(sql,(permission_id))
                r = cur.fetchall()
                if r:
                    for val in r:
                        sql = "select permission_id from role_permissions where category_id= %s and function_id= %s"
                        cur.execute(sql, (val[0],val[2]))
                        r1 = cur.fetchall()

                        if r1:
                            for val1 in r1:
                                if val1[0] not in prmsn and permission_id != val1[0]:
                                    prmsn.append(val1[0])
                        #else:
                            #r1 = "5"
                #else:
                    #r = "3"


            return jsonify(prmsn)
    except Exception as e:
        return {'error': str(e)}




@app.route('/getfunction_permission_details',methods=['POST', 'GET'])#-------------Get all the departments
def getfunction_permission_details():
    try:
        if request.is_json:
            data = request.json
            hashkey = data['hashkey']
            comp_hash = compare_hashkey(hashkey)
            prmsn = []
            if comp_hash == 1:
                permission_id = data['permission_id']
                category_id = data['category_id']
                conn = mysql.connect()
                cur = conn.cursor()
                sql = "select b.func_id from role_permissions a,role_function_dependency b where a.permission_id= %s and b.dependency_id=a.function_id"
                cur.execute(sql,(permission_id))
                r = cur.fetchall()
                if r:
                    for val in r:
                        sql = "select permission_id from role_permissions where category_id= %s and function_id= %s"
                        cur.execute(sql, (category_id,val[0]))
                        r1 = cur.fetchall()
                        if r1:
                            for val1 in r1:
                                if permission_id != val1[0]:
                                    prmsn.append(val1[0])
                        #else:
                            #r1 = "5"
                #else:
                    #r = "3"
            return jsonify(prmsn)
    except Exception as e:
        return {'error': str(e)}




def compare_hashkey(passhashkey):
    try:
        id = 1
        return id
    except Exception as e:
        return {'error': str(e)}





@app.route('/select_private_key',methods=['POST', 'GET'])#-------------Get all the departments
def select_private_key():
    try:
        private_key = '123456789'
        conn = mysql.connect()
        cur = conn.cursor()
        sql = "select ciphertext,tag,nonce,nonce2 from privatekey_generation where private_key= %s "
        cur.execute(sql, (private_key))
        r = cur.fetchall()
        if r:
            for val in r:
                ciphertext = val[0]
                tag = val[1]
                nonce = val[2]
                nonce2n = val[3]
        else :
            print('nothing')
        print(ciphertext)
        print(tag)
        print(nonce)

        nonce1 = b'e\xccE`\x89\xb3"!9\xdb\xa1\x87s\xd2\xb5D'
        print('answerrrrrrrrrrrr===============')

        print(nonce2n)
        print(nonce)
        encodednn = base64.b64encode(nonce2n)
        print('encodeddddd')
        print(encodednn)
        print('-------------+++++++++++')

        print(nonce2n)
        print(encodednn)
        encodednn = base64.b64decode(encodednn)
        #decoded1 = base64.b64decode(encoded)
        print('decodeddddddddd')
        #print(decoded)
        #print(decoded1)

        nonce2 = b'e\xccE`\x89\xb3"!9\xdb\xa1\x87s\xd2\xb5D'
        tag1 = b'\x9c\x14\xf9\x14/\xe2\x8f\xe51};<k\xa81\xfa'
        ciphertext1 = b'\xe5\xed\xb3\x05\xd3\xd1\x9f\xb2\x895x\xfd\xe9\xea\x06\x85L\xc6#z\x05\xc7N\xc3\xdd\x0c'

        print('same or nottttt')

        if nonce2 == nonce2n:
            print('sameeeeeeeeeeee')
        else:
            print('noooooooooo')





        print(ciphertext)
        print(tag)
        print(nonce)



        key = b'Sixteen byte key'
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce2)
        plaintext = cipher.decrypt(ciphertext1)
        try:
            cipher.verify(tag1)
            print("The message is authentic:", plaintext)
        except ValueError:
            print("Key incorrect or message corrupted")


        return jsonify('r')
    except Exception as e:
        return {'error': str('e')}


def referral():
    url = request.referrer
    print("enterrrr")
    print(url)
    # if domain is not mine, save it in the session
    if url and url_parse(url).host != "example.com":
        session["url"] = url
    return session.get("url")


def proxied_request_info(proxy_url):
    """Returns information about the target (proxied) URL given a URL sent to
    the proxy itself. For example, if given:
        http://localhost:5000/p/google.com/search?q=foo
    then the result is:
        ("google.com", "search?q=foo")"""
    parts = urlparse(proxy_url)
    if not parts.path:
        return None
    elif not parts.path.startswith('/p/'):
        return None
    matches = re.match('^/p/([^/]+)/?(.*)', parts.path)
    proxied_host = matches.group(1)
    proxied_path = matches.group(2) or '/'
    proxied_tail = urlunparse(parts._replace(scheme="", netloc="", path=proxied_path))
    #LOG.debug("Referred by proxy host, uri: %s, %s", proxied_host, proxied_tail)
    return [proxied_host, proxied_tail]


@app.route('/check_login',methods=['POST', 'GET'])#------------------Get all the departments
def check_login():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            username = data['username']
            password = data['password']
            #validate_res = validate_private_key(private_key)
            validate_res = 1
            res = 2
            if validate_res ==1:
                conn = mysql.connect()
                cur = conn.cursor()
                sql = "select userid,name,user_type from user_details where username=%s and password = %s and status = 'active'"
                cur.execute(sql,(username,password))
                r = cur.fetchall()
                numrows = cur.rowcount
                if numrows < 1:
                    r = -1
                #else:
                    #r = -1
            else:
                r = -2
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}



@app.route('/user_log_insert',methods=['POST', 'GET'])#---------------Save course
def user_log_insert():
    try:
        if request.is_json:
            data = request.json
            hashkey = data['hashkey']
            password = data['password']
            captcha =''
            actual_captcha = ''
            username = ''
            user_ip = data['user_ip']
            time=data['time']
            conn = mysql.connect()
            cur = conn.cursor()
            sql = "insert into login_attempts(username,password,captcha_entered,actual_captcha,user_ip)values(%s,%s,%s,%s,%s)"
            cur.execute(sql,(username,password,captcha,actual_captcha,user_ip))
            conn.commit()
            n = cur.lastrowid
            if n is not None:
                a = "Saved Successfully"
            else:
                a = "Can't Save the Data"
            return jsonify(a)
    except Exception as e:
        return {'error': str(e)}



@app.route('/add_login_attempt',methods=['POST', 'GET'])#---------------Save course
def add_login_attempt():
    try:
        if request.is_json:
            data = request.json
            username = data['username']
            password = data['password']
            #captcha = data['captcha']
            #actual_captcha = data['actual_captcha']
            captcha =''
            actual_captcha = ''
            user_ip = data['user_ip']
            time=data['time']

            conn = mysql.connect()
            cur = conn.cursor()
            sql = "insert into login_attempts(username,password,captcha_entered,actual_captcha,user_ip)values(%s,%s,%s,%s,%s)"
            cur.execute(sql,(username,password,captcha,actual_captcha,user_ip))
            conn.commit()
            n = cur.lastrowid
            if n is not None:
                a = "Saved Successfully"
            else:
                a = "Can't Save the Data"
            return jsonify(a)
    except Exception as e:
        return {'error': str(e)}




@app.route('/validate_login',methods=['POST', 'GET'])#------------------Get all the departments
def validate_login():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            validate_res = validate_private_key(private_key)
            s = 0
            if validate_res == 1:
                username = data['username']
                userid = data['userid']
                conn = mysql.connect()
                cur = conn.cursor()
                sql = "select userid from user_details where username=%s and  userid = %s and status = 'active'"
                cur.execute(sql,(username,userid))
                r = cur.fetchall()
                if r:
                    s = 1
                else:
                    s = 0
            return jsonify(s)
    except Exception as e:
        return {'error': str(e)}


@app.route('/univ_history', methods=['POST', 'GET'])  # ------------------Get universities_briefhistory
def univ_history():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            univ_id = data['univ_id']
            r=''
            validate_res = validate_private_key(private_key)
            if validate_res == 1:
                cur = mysql.connect().cursor()
                cur.execute('''select univ_id,univ_name,univ_history,univ_image from univ_details where univ_id =%s''',(univ_id))
                r = cur.fetchall()
            else :
                r=-5
            return jsonify(r)
    except Exception as e:
            return {'error': str(e)}







@app.route('/univ_juris', methods=['POST', 'GET'])  # ------------------Get universities_briefhistory
def univ_juris():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            univ_id = data['univ_id']
            r=''
            validate_res = validate_private_key(private_key)
            if validate_res == 1:
                cur = mysql.connect().cursor()
                cur.execute('''select univ_name,univ_jurisdiction,univ_land_area from univ_details where univ_id =%s''',(univ_id))
                r = cur.fetchall()
            else :
                r = -5
            return jsonify(r)
    except Exception as e:
            return {'error': str(e)}



@app.route('/univ_act_statutes',methods=['POST', 'GET'])#------------------Get all the departments
def univ_act_statutes():
    try:
        if request.is_json:
            data = request.json
            univ_id = data['univ_id']
            type = data['type']
            private_key = data['private_key']
            r=''
            validate_res = validate_private_key(private_key)
            if validate_res == 1:
                cur = mysql.connect().cursor()
                if type != '':
                    cur.execute('''select c.act_or_statute,c.act_stat_url from univ_details u inner join univ_acts_and_statutes c  on u.univ_id =c.univ_id and u.univ_id=%s and c.act_or_statute=%s''',(univ_id,type))
                else :
                    cur.execute('''select c.act_or_statute,c.act_stat_url from univ_details u inner join univ_acts_and_statutes c  on u.univ_id =c.univ_id and u.univ_id=%s''',(univ_id))
                r = cur.fetchall()
            else :
                r = -5
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}




@app.route('/univ_dept_faculty',methods=['POST', 'GET'])#------------------Get all the departments
def univ_dept_faculty():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            univ_id = data['univ_id']
            faculty_code = data['faculty_code']
            r=''
            validate_res = validate_private_key(private_key)
            if validate_res == 1:
                cur = mysql.connect().cursor()
                if faculty_code!= '' :
                    cur.execute('''select f.faculty_name,f.faculty_address,f.faculty_phone_no,f.faculty_contact_no,f.email,f.Designation,ud.dept_name from univ_dept_faculties f left join univ_departments ud on f.dept_id=ud.dept_id where ud.univ_id=%s and f.faculty_code Like %s''',(univ_id,"%" + faculty_code + "%"))
                else :
                    cur.execute('''select f.faculty_name,f.faculty_address,f.faculty_phone_no,f.faculty_contact_no,f.email,f.Designation,ud.dept_name from univ_dept_faculties f left join univ_departments ud on f.dept_id=ud.dept_id where ud.univ_id=%s''',(univ_id))
                r = cur.fetchall()
            else :
                r=-5
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}



@app.route('/univ_dept_programmes', methods=['POST', 'GET'])  # ------------------Get all the departments
def univ_dept_programmes():
    try:
        if request.is_json:
                data = request.json
                private_key = data['private_key']
                univ_id = data['univ_id']
                dept_code = data['dept_code']
                r = ''
                validate_res = validate_private_key(private_key)
                if validate_res == 1:
                    cur = mysql.connect().cursor()
                    if dept_code!= '':
                        cur.execute('''select p.pgm_name,d.dept_code,p.pgm_code,p.no_of_seats from univ_department_programmes p left join univ_departments d on p.dept_id = d.dept_id where p.univ_id=%s and d.dept_code Like %s''',(univ_id,"%" + dept_code + "%"))
                    else :
                        cur.execute('''select p.pgm_name,d.dept_code,p.pgm_code,p.no_of_seats from univ_department_programmes p left join univ_departments d on p.dept_id = d.dept_id where p.univ_id=%s''',(univ_id))
                    r = cur.fetchall()
                else :
                    r = -5
                return jsonify(r)
    except Exception as e:
        return {'error': str(e)}


@app.route('/checklogin',methods=['POST', 'GET'])#------------------Get all the departments
def checklogin():
    try:
        if request.is_json:
            data = request.json
            userid = data['userid']
            username = data['username']
            hashkey = data['hashkey']
            conn = mysql.connect()
            cur = conn.cursor()
            sql = "select count(*) from user_details where userid=%s and username=%s and status = 'active'"
            cur.execute(sql,(userid,username))
            r = cur.fetchall()
            if r:
                s = 1
            else:
                s = 0
            return jsonify(s)
    except Exception as e:
        return {'error': str(e)}



@app.route('/select_private_key_working',methods=['POST', 'GET'])#-------------Get all the departments
def select_private_key_working():
    try:
        private_key = '123456789'
        conn = mysql.connect()
        cur = conn.cursor()
        sql = "select ciphertext,tag,nonce from privatekey_generation where private_key= %s "
        cur.execute(sql, (private_key))
        r = cur.fetchall()
        #print(r)
        if r:
            for val in r:
                ciphertext = val[0]
                tag = val[1]
                nonce = val[2]

        else :
            print('nothing')




        #------------------don't delete this is working code-------------------

        #hex_nonce=codecs.encode(noncenew, 'hex_codec')
        #hex_tag = codecs.encode(tagnew, 'hex_codec')
        #hex_ciphertext = codecs.encode(ciphertextnew, 'hex_codec')

        #------------------dint delete this is working code-------------------



        key = b'Sixteen byte key'
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        try:
            cipher.verify(tag)
            print("The message is authentic:", plaintext)
        except ValueError:
            print("Key incorrect or message corrupted")


        return jsonify('r')
    except Exception as e:
        return {'error': str('e')}







def validate_private_key(private_key):
    try:
        res = 1
        return res

    except Exception as e:
        return {'error': str(e)}




@app.route('/univ_syndicate',methods=['POST', 'GET'])#------------------Get all the syndicatemembers
def univ_syndicate():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            univ_id = data['univ_id']
            synd_year_from = data['synd_year_from']
            synd_year_to = data['synd_year_to']
            numb=data['numb']
            status = data['status']
            exact_year = data['exact_year']
            r = ''
            validate_res = validate_private_key(private_key)
            if validate_res == 1:
                cur = mysql.connect().cursor()
                syndyear_from_str = ''
                status_str = ''
                limit_str = ''
                exact_year_str = ''
                from_to_str = ''
                if (synd_year_from<=synd_year_to and synd_year_to!='') or synd_year_to=='':
                    if (synd_year_from != '' or synd_year_to != '' or status!='' or numb!='' or exact_year!=''):

                        if exact_year != '':
                            exact_year_str = ' and  synd_year_from<='+exact_year+' and synd_year_to>='+exact_year
                        if synd_year_from != '' and synd_year_to == '':
                            syndyear_from_str = ' and ( synd_year_from>='+synd_year_from+' or synd_year_to>='+synd_year_from+')'
                        if synd_year_to != '' and synd_year_from !='':
                            from_to_str = ' and (( synd_year_from<='+synd_year_from+' and synd_year_to>='+synd_year_from+') or ( synd_year_from<='+synd_year_to+' and synd_year_to>='+synd_year_to+') or  (synd_year_from between '+synd_year_from+' and '+synd_year_to+') or (synd_year_to between '+synd_year_from+' and '+synd_year_to+'))'
                        if status != '':
                            status_str = ' and status="' + status + '"'
                        if numb != '':
                            limit_str = '  limit ' + numb

                        cur.execute('''select synd_name,synd_address,synd_email,synd_mobile,synd_photograph,synd_year_from,synd_year_to from univ_syndicate_members where univ_id=%s '''+from_to_str+''+exact_year_str+''+status_str+''+syndyear_from_str+''+limit_str,(univ_id))
                    else:
                        cur.execute('''select synd_name,synd_address,synd_email,synd_mobile,synd_photograph,synd_year_from,synd_year_to from univ_syndicate_members where univ_id=%s ''',(univ_id))
                    r = cur.fetchall()
                    #print(cur._last_executed)
            else:
               r = -5
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}




@app.route('/univ_senate',methods=['POST', 'GET'])#------------------Get all the senatemembers
def univ_senate():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            univ_id = data['univ_id']
            senate_year_from = data['senate_year_from']
            senate_year_to = data['senate_year_to']
            numb=data['numb']
            status = data['status']
            exact_year = data['exact_year']
            r = ''
            validate_res = validate_private_key(private_key)
            if validate_res == 1:
                cur = mysql.connect().cursor()

                senateyear_from_str = ''
                status_str = ''
                limit_str = ''
                exact_year_str = ''
                from_to_str = ''
                if (senate_year_from<=senate_year_to and senate_year_to!='') or senate_year_to=='':
                    if (senate_year_from != '' or senate_year_to != '' or status!='' or numb!='' or exact_year!=''):
                        if exact_year != '':
                            exact_year_str = ' and  senate_year_from<='+exact_year+' and senate_year_to>='+exact_year
                        if senate_year_from != '' and senate_year_to == '':
                            senateyear_from_str = ' and ( senate_year_from>='+senate_year_from+' or senate_year_to>='+senate_year_from+')'
                        if senate_year_to != '' and senate_year_from !='':
                            from_to_str = ' and (( senate_year_from<='+senate_year_from+' and senate_year_to>='+senate_year_from+') or ( senate_year_from<='+senate_year_to+' and senate_year_to>='+senate_year_to+') or  (senate_year_from between '+senate_year_from+' and '+senate_year_to+') or (senate_year_to between '+senate_year_from+' and '+senate_year_to+'))'
                        if status != '':
                            status_str = ' and status="' + status + '"'
                        if numb != '':
                            limit_str = '  limit ' + numb
                    cur.execute('''select senate_name,senate_address,senate_email,senate_mobile,senate_photograph_url,senate_id,senate_year_from,senate_year_to from univ_senate_members where univ_id=%s'''+ from_to_str + '' + exact_year_str + '' + status_str + '' + senateyear_from_str + '' + limit_str,(univ_id))

                #else:
                    #cur.execute('''select senate_name,senate_address,senate_email,senate_mobile,senate_photograph_url,senate_id,senate_year_from,senate_year_to from univ_senate_members where univ_id=%s''',(univ_id))

                    r = cur.fetchall()
                #print(cur._last_executed)

            else:
               r = -5

            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}





@app.route('/univ_ac',methods=['POST', 'GET'])#------------------Get all the senatemembers
def univ_ac():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            univ_id = data['univ_id']
            council_year_from = data['council_year_from']
            council_year_to = data['council_year_to']
            numb = data['numb']
            status = data['status']
            exact_year = data['exact_year']
            r = ''
            validate_res = validate_private_key(private_key)
            #validate_res = 1
            if validate_res == 1:
                cur = mysql.connect().cursor()

                councilyear_from_str = ''
                status_str = ''
                limit_str = ''
                exact_year_str = ''
                from_to_str = ''

                if (council_year_from <= council_year_to and council_year_to != '') or council_year_to == '':
                    if (council_year_from != '' or council_year_to != '' or status != '' or numb != '' or exact_year != ''):
                        if exact_year != '':
                            exact_year_str = ' and  council_year_from<=' + exact_year + ' and council_year_to>=' + exact_year
                        if council_year_from != '' and council_year_to == '':
                            councilyear_from_str = ' and ( council_year_from>=' + council_year_from + ' or council_year_to>=' + council_year_from + ')'
                        if council_year_to != '' and council_year_from != '':
                            from_to_str = ' and (( council_year_from<=' + council_year_from + ' and council_year_to>=' + council_year_from + ') or ( council_year_from<=' + council_year_to + ' and council_year_to>=' + council_year_to + ') or  (council_year_from between ' + council_year_from + ' and ' + council_year_to + ') or (council_year_to between ' + council_year_from + ' and ' + council_year_to + '))'
                        if status != '':
                            status_str = ' and status="' + status + '"'
                        if numb != '':
                            limit_str = '  limit ' + numb


                    cur.execute('''select council_name,council_address,council_email,council_mobile,council_photograph_url,council_id,council_year_from,council_year_to from univ_accademic_council where univ_id=%s '''+ from_to_str + '' + exact_year_str + '' + status_str + '' + councilyear_from_str + '' + limit_str,(univ_id))
                #else:
                    #cur.execute('''select council_name,council_address,council_email,council_mobile,council_photograph_url,council_id,council_year_from,council_year_to from univ_accademic_council where univ_id=%s ''',(univ_id))
                    r = cur.fetchall()
                #print(cur._last_executed)
                #print(r)
            else:
               r = -5

            #print(r)
            return jsonify(r)

    except Exception as e:
        return {'error': str(e)}




@app.route('/univ_statu_officer',methods=['POST', 'GET'])#------------------Get all the senatemembers
def univ_statu_officer():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            univ_id = data['univ_id']
            stat_year_from  = data['stat_year_from']
            stat_year_to  = data['stat_year_to']
            numb = data['numb']
            status = data['status']
            exact_year = data['exact_year']

            r = ''
            validate_res = validate_private_key(private_key)

            if validate_res == 1:
                cur = mysql.connect().cursor()

                stat_year_from_str = ''
                status_str = ''
                limit_str = ''
                exact_year_str = ''
                from_to_str = ''
                if (stat_year_from <= stat_year_to and stat_year_to != '') or stat_year_to == '':
                    if (stat_year_from != '' or stat_year_to != '' or status != '' or numb != '' or exact_year != ''):
                        if exact_year != '':
                            exact_year_str = ' and  stat_year_from<=' + exact_year + ' and stat_year_to>=' + exact_year
                        if stat_year_from != '' and stat_year_to == '':
                            stat_year_from_str = ' and ( stat_year_from>=' + stat_year_from + ' or stat_year_to>=' + stat_year_from + ')'
                        if stat_year_to != '' and stat_year_from != '':
                            from_to_str = ' and (( stat_year_from<=' + stat_year_from + ' and stat_year_to>=' + stat_year_from + ') or ( stat_year_from<=' + stat_year_to + ' and stat_year_to>=' + stat_year_to + ') or  (stat_year_from between ' + stat_year_from + ' and ' + stat_year_to + ') or (stat_year_to between ' + stat_year_from + ' and ' + stat_year_to + '))'
                        if status != '':
                            status_str = ' and status="' + status + '"'
                        if numb != '':
                            limit_str = '  limit ' + numb
                    cur.execute('''select stat_member_name,stat_member_address,stat_member_email,stat_member_mobile,stat_member_photograph,statut_id,stat_year_from,stat_year_to from univ_statutory_officers where univ_id=%s '''+ from_to_str + '' + exact_year_str + '' + status_str + '' + stat_year_from_str + '' + limit_str,(univ_id))
                #else:
                    #cur.execute('''select stat_member_name,stat_member_address,stat_member_email,stat_member_mobile,stat_member_photograph,statut_id,stat_year_from,stat_year_to from univ_statutory_officers where univ_id=%s  ''',(univ_id))
                    r = cur.fetchall()
                #print(cur._last_executed)
                #print(r)
            else:
               r = -5

            #print(r)
            return jsonify(r)

    except Exception as e:
        return {'error': str(e)}



@app.route('/univ_programmes',methods=['POST', 'GET'])#------------------Get all the programmes
def univ_programmes():
    try:
        if request.is_json:
            data = request.json
            univ_id = data['univ_id']
            pgm_type = data['pgm_type']
            private_key = data['private_key']
            r = ''
            validate_res = validate_private_key(private_key)
            #validate_res = 1
            if validate_res == 1:
                cur = mysql.connect().cursor()
                if pgm_type != '':
                    cur.execute('''select pgm_name,pgm_code,eligibility_criteria,statutory_limit,sem_year,no_sem_year,pgm_id,pgm_type from univ_department_programmes where univ_id=%s and pgm_type =%s ''',(univ_id,pgm_type))
                else:
                    cur.execute('''select pgm_name,pgm_code,eligibility_criteria,statutory_limit,sem_year,no_sem_year,pgm_id,pgm_type from univ_department_programmes where univ_id=%s ''',(univ_id))
                r = cur.fetchall()
                #print(cur._last_executed)
                #print(r)
            else:
                r = -5

            #print(r)
            return jsonify(r)

    except Exception as e:
        return {'error': str(e)}




@app.route('/univ_bos', methods=['POST', 'GET'])  # ------------------Get all the departments
def univ_bos():
    try:
        if request.is_json:
                data = request.json
                private_key = data['private_key']
                univ_id = data['univ_id']
                pgm_type = data['pgm_type']

                pgm_code = data['pgm_code']

                r = ''
                validate_res = validate_private_key(private_key)
                if validate_res == 1:
                    cur = mysql.connect().cursor()
                    pgm_type_str =''
                    if pgm_type != '':
                        pgm_type_str = ' and udp.pgm_type="'+pgm_type+'"'
                    if pgm_code != '':
                       cur.execute('''select ubs.board_member,ubs.board_member_address,ubs.board_mob,udp.pgm_type,udp.pgm_code from univ_board_studies ubs left join univ_department_programmes udp on ubs.pgm_id=udp.pgm_id left join univ_departments ud on udp.dept_id=ud.dept_id where ud.univ_id=%s and udp.pgm_code Like %s '''+pgm_type_str,(univ_id,"%" + pgm_code + "%"))
                    else:
                        cur.execute('''select ubs.board_member,ubs.board_member_address,ubs.board_mob,udp.pgm_type,udp.pgm_code from univ_board_studies ubs left join univ_department_programmes udp on ubs.pgm_id=udp.pgm_id left join univ_departments ud on udp.dept_id=ud.dept_id where ud.univ_id=%s'''+pgm_type_str,(univ_id))
                    r = cur.fetchall()
                    #print(r)
                    #print(cur._last_executed)
                else:
                    r = -5
                return jsonify(r)
    except Exception as e:
        return {'error': str(e)}




@app.route('/college_dept',methods=['POST', 'GET'])#-------------Get all the departments of affiliated colleges
def college_dept():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            univ_id = data['univ_id']
            univ_colg_id = data['univ_colg_id']
            conn = mysql.connect()
            cur = conn.cursor()
            #if (pgm_type == ('UG' or 'PG')):
            sql = "select ad.dept_name,ad.dept_code,ad.dept_hod_name,ad.dept_phone_no from univ_affiliate_departments ad left join univ_colleges uc on ad.univ_colg_id=uc.univ_colg_id left join univ_details ud on uc.univ_id=ud.univ_id  where ud.univ_id=%s"
            cur.execute(sql,(univ_id))
            r = cur.fetchall()
            #numrows = cur.rowcount
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}


@app.route('/college_programmes', methods=['POST', 'GET'])  # -------------Get all the programmes of affiliated colleges
def college_programmes():
        try:
            if request.is_json:
                data = request.json
                private_key = data['private_key']
                univ_id = data['univ_id']
                dept_code = data['dept_code']
                conn = mysql.connect()
                cur = conn.cursor()

                dept_code_str =''
                if dept_code!='':
                    sql = "select uap.programme_name,uap.pgm_code,uad.dept_code,uap.no_of_seats from univ_affiliate_programmes uap left join univ_affiliate_departments uad on  uap.dept_id=uad.dept_id  left join univ_colleges uc on uad.univ_colg_id=uc.univ_colg_id  left join univ_details ud on  uc.univ_id=ud.univ_id  where ud.univ_id=%s and uad.dept_code Like %s"
                    cur.execute(sql, (univ_id, "%" + dept_code + "%"))
                else :
                    sql = "select uap.programme_name,uap.pgm_code,uad.dept_code,uap.no_of_seats from univ_affiliate_programmes uap left join univ_affiliate_departments uad on  uap.dept_id=uad.dept_id  left join univ_colleges uc on uad.univ_colg_id=uc.univ_colg_id  left join univ_details ud on  uc.univ_id=ud.univ_id  where ud.univ_id=%s"
                    cur.execute(sql, (univ_id))
                r = cur.fetchall()
                #print(cur._last_executed)
                # numrows = cur.rowcount
                return jsonify(r)
        except Exception as e:
            return {'error': str(e)}





@app.route('/college_faculties',methods=['POST', 'GET'])#-------------Get  the faculties of affiliated colleges
def college_faculties():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            univ_id = data['univ_id']
            dept_code = data['dept_code']
            conn = mysql.connect()
            cur = conn.cursor()
            if dept_code != '':
                sql = "select uaf.faculty_name,uaf.faculty_qualification,uaf.faculty_specialization,uaf.faculty_mobile,uad.dept_code,uc.college_code from univ_affiliate_faculties uaf inner join  univ_affiliate_departments uad on uaf.dept_id=uad.dept_id left join univ_colleges uc on uad.univ_colg_id=uc.univ_colg_id left join univ_details ud on uc.univ_id=ud.univ_id where ud.univ_id=%s and uad.dept_code Like %s"
                cur.execute(sql, (univ_id,"%" + dept_code + "%"))
                #print(cur._last_executed)
            else :
                sql = "select uaf.faculty_name,uaf.faculty_qualification,uaf.faculty_specialization,uaf.faculty_mobile,uad.dept_code,uc.college_code from univ_affiliate_faculties uaf inner join  univ_affiliate_departments uad on uaf.dept_id=uad.dept_id left join univ_colleges uc on uad.univ_colg_id=uc.univ_colg_id left join univ_details ud on uc.univ_id=ud.univ_id where ud.univ_id=%s"
                cur.execute(sql,(univ_id,))
            r = cur.fetchall()
            #numrows = cur.rowcount
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}





@app.route('/univ_dept_students',methods=['POST', 'GET'])#-------------Get  the students of university
def univ_dept_students():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            univ_id = data['univ_id']
            dept_code = data['dept_code']
            conn = mysql.connect()
            cur = conn.cursor()
            if dept_code != '':
                sql = "select usd.unique_id,usd.stud_name,usd.community,udp.pgm_type,udp.sem_year,usd.status,ud.dept_code,udp.pgm_code from univ_students_details usd left join univ_department_programmes udp on usd.pgm_id=udp.pgm_id  left join univ_departments ud on udp.dept_id=ud.dept_id left join univ_details und on ud.univ_id=und.univ_id where und.univ_id=%s and ud.dept_code Like %s"
                cur.execute(sql,(univ_id,"%" + dept_code + "%"))
            else :
                sql = "select usd.unique_id,usd.stud_name,usd.community,udp.pgm_type,udp.sem_year,usd.status,ud.dept_code,udp.pgm_code from univ_students_details usd left join univ_department_programmes udp on usd.pgm_id=udp.pgm_id  left join univ_departments ud on udp.dept_id=ud.dept_id left join univ_details und on ud.univ_id=und.univ_id where und.univ_id=%s"
                cur.execute(sql,(univ_id))
            r = cur.fetchall()
            #numrows = cur.rowcount
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}





@app.route('/college_students',methods=['POST', 'GET'])#-------------Get  the students of affiliated colleges
def college_students():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            univ_id = data['univ_id']
            dept_code = data['dept_code']
            clg_code = data['clg_code']
            conn = mysql.connect()
            cur = conn.cursor()
            if dept_code != '' and clg_code != '':
                sql = "select uasd.unique_id,uasd.stud_name,uasd.community,uap.pgm_type,uap.sem_year,uasd.status,uad.dept_code,uap.pgm_code,uc.college_code from univ_affiliate_students_details uasd inner join univ_affiliate_programmes uap on uasd.pgm_id=uap.pgm_id left join univ_affiliate_departments uad on uap.dept_id=uad.dept_id left join univ_colleges uc on uad.univ_colg_id=uc.univ_colg_id  left join  univ_details ud on uc.univ_id=ud.univ_id where ud.univ_id=%s and ( uad.dept_code Like %s or uc.college_code Like %s )"
                cur.execute(sql,(univ_id,"%" + dept_code + "%","%" + clg_code + "%"))
            elif dept_code!= '':
                sql = "select uasd.unique_id,uasd.stud_name,uasd.community,uap.pgm_type,uap.sem_year,uasd.status,uad.dept_code,uap.pgm_code,uc.college_code from univ_affiliate_students_details uasd inner join univ_affiliate_programmes uap on uasd.pgm_id=uap.pgm_id left join univ_affiliate_departments uad on uap.dept_id=uad.dept_id left join univ_colleges uc on uad.univ_colg_id=uc.univ_colg_id  left join  univ_details ud on uc.univ_id=ud.univ_id where ud.univ_id=%s and uad.dept_code Like %s"
                cur.execute(sql,(univ_id,"%" + dept_code + "%"))
            elif clg_code != '' :
                sql = "select uasd.unique_id,uasd.stud_name,uasd.community,uap.pgm_type,uap.sem_year,uasd.status,uad.dept_code,uap.pgm_code,uc.college_code from univ_affiliate_students_details uasd inner join univ_affiliate_programmes uap on uasd.pgm_id=uap.pgm_id left join univ_affiliate_departments uad on uap.dept_id=uad.dept_id left join univ_colleges uc on uad.univ_colg_id=uc.univ_colg_id  left join  univ_details ud on uc.univ_id=ud.univ_id where ud.univ_id=%s and uc.college_code Like %s"
                cur.execute(sql,(univ_id,"%" + clg_code + "%"))
            else :

                sql = "select uasd.unique_id,uasd.stud_name,uasd.community,uap.pgm_type,uap.sem_year,uasd.status,uad.dept_code,uap.pgm_code,uc.college_code from univ_affiliate_students_details uasd inner join univ_affiliate_programmes uap on uasd.pgm_id=uap.pgm_id left join univ_affiliate_departments uad on uap.dept_id=uad.dept_id left join univ_colleges uc on uad.univ_colg_id=uc.univ_colg_id  left join  univ_details ud on uc.univ_id=ud.univ_id where ud.univ_id=%s "
                cur.execute(sql,(univ_id))
            r = cur.fetchall()
            #numrows = cur.rowcount
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}


@app.route('/univ_calender',methods=['POST', 'GET'])#------------------Get all the departments
def univ_calender():
    try:
        if request.is_json:
            data = request.json
            univ_id = data['univ_id']
            calender_type = data['calender_type']
            private_key = data['private_key']
            r = ''
            validate_res = validate_private_key(private_key)
            #validate_res = 1
            if validate_res == 1:
                cur = mysql.connect().cursor()
                if calender_type != '':
                    cur.execute('''select calender_url,calender_type,cal_id from univ_calender where univ_id=%s and calender_type=%s''',(univ_id,calender_type))
                else:
                    cur.execute('''select calender_url,calender_type,cal_id from univ_calender where univ_id=%s''',(univ_id))
                r = cur.fetchall()
            else:
                r = -5
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}





@app.route('/univ_fund_agency',methods=['POST', 'GET'])#------------------Get all the FUND AGENCY
def univ_fund_agency():
    try:
        if request.is_json:
            data = request.json
            univ_id = data['univ_id']
            agency_type = data['agency_type']
            private_key = data['private_key']
            r = ''
            validate_res = validate_private_key(private_key)
            #validate_res = 1
            if validate_res == 1:
                cur = mysql.connect().cursor()
                if agency_type != '':
                    cur.execute('''select agency_name,agency_address,agency_code,agency_type from univ_fund_agency where univ_id=%s and agency_type =%s ''',(univ_id,agency_type))
                else:
                    cur.execute('''select agency_name,agency_address,agency_code,agency_type from univ_fund_agency where univ_id=%s ''',(univ_id))
                r = cur.fetchall()
                #print(cur._last_executed)
                #print(r)
            else:
                r = -5
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}



@app.route('/univ_FA_fund_det',methods=['POST', 'GET'])#-------------Get  the fund alocated
def univ_FA_fund_det():
    try:
        if request.is_json:
            data = request.json
            private_key = data['private_key']
            univ_id = data['univ_id']
            agency_id = data['agency_id']
            conn = mysql.connect()
            cur = conn.cursor()
            sql = "select a.agency_name,a.agency_address,a.agency_code,f.fund_alloted,f.duration from univ_fa_fund_details f left join univ_fund_agency a on f.agency_id=a.agency_id where f.univ_id=%s "
            cur.execute(sql,(univ_id))

            r = cur.fetchall()
            #numrows = cur.rowcount
            return jsonify(r)
    except Exception as e:
        return {'error': str(e)}


@app.route('/univ_research_facility', methods=['POST', 'GET'])  # ------------------Get all the departments
def univ_research_facility():
    try:
        if request.is_json:
                data = request.json
                private_key = data['private_key']
                univ_id = data['univ_id']
                institution_type = data['institution_type']
                r = ''
                validate_res = validate_private_key(private_key)
                if validate_res == 1:
                    cur = mysql.connect().cursor()
                    if institution_type == '1':
                        print('enterrrrrrrrrrrrrrrrrr')
                        cur.execute('''select r.facility_name,d.dept_code,'Nil',r.facility_cost,r.facility_manufacturer,r.faculty_member,r.brief_description,r.location,r.institution_type,'Nil' from univ_research_facility r left join univ_departments d on r.dept_id= d.dept_id where r.univ_id=%s and r.institution_type=%s''',(univ_id,institution_type))
                    elif institution_type == '2':
                        cur.execute('''select r.facility_name,'Nil',c.college_code,r.facility_cost,r.facility_manufacturer,r.faculty_member,r.brief_description,r.location,r.institution_type,'Nil' from univ_research_facility r left join univ_colleges c on r.univ_colg_id=c.univ_colg_id where c.univ_id=%s and r.institution_type=%s''',(univ_id,institution_type))
                    elif institution_type == '3' :
                        cur.execute('''select r.facility_name,'Nil','Nil',r.facility_cost,r.facility_manufacturer,r.faculty_member,r.brief_description,r.location,r.institution_type,ce.univ_center_name from univ_research_facility r left join univ_centers ce on r.univ_center_id=ce.univ_center_id where ce.univ_id=%s and r.institution_type=%s''',(univ_id,institution_type))
                    else:
                        cur.execute('''select r.facility_name,d.dept_code,'Nil',r.facility_cost,r.facility_manufacturer,r.faculty_member,r.brief_description,r.location,r.institution_type,'Nil' from univ_research_facility r left join univ_departments d on r.dept_id= d.dept_id where d.univ_id=%s and r.institution_type=%s union all select r.facility_name,'Nil',c.college_code,r.facility_cost,r.facility_manufacturer,r.faculty_member,r.brief_description,r.location,r.institution_type,'Nil' from univ_research_facility r left join univ_colleges c on r.univ_colg_id=c.univ_colg_id where c.univ_id=%s and r.institution_type=%s union all select r.facility_name,'Nil','Nil',r.facility_cost,r.facility_manufacturer,r.faculty_member,r.brief_description,r.location,r.institution_type,ce.univ_center_name from univ_research_facility r left join univ_centers ce on r.univ_center_id=ce.univ_center_id where ce.univ_id=%s and r.institution_type=%s ''',(univ_id,1,univ_id,2,univ_id,3))
                    #print(cur._last_executed)
                    r = cur.fetchall()
                    #print(r)
                else:
                    r = -5
                return jsonify(r)
    except Exception as e:
        return {'error': str(e)}




@app.route('/univ_patent', methods=['POST', 'GET'])  # ------------------Get all the departments
def univ_patent():
    try:
        if request.is_json:
                data = request.json
                private_key = data['private_key']
                univ_id = data['univ_id']
                institution_type = data['institution_type']
                r = ''
                #validate_res = validate_private_key(private_key)
                validate_res = 1
                if validate_res == 1:
                    cur = mysql.connect().cursor()
                    if institution_type == '1':
                        cur.execute('''select d.dept_code,'Nil','Nil',r.filled_patent,r.granted_patent,r.fund_generated,r.faculty_name,r.description,r.institution_type from univ_patent r left join univ_departments d on r.dept_id=d.dept_id where d.univ_id=%s and r.institution_type=%s''',(univ_id, institution_type))
                    elif institution_type == '2':
                        cur.execute('''select 'Nil',c.college_code,'Nil',r.filled_patent,r.granted_patent,r.fund_generated,r.faculty_name,r.description,r.institution_type from univ_patent r left join univ_colleges c on r.univ_colg_id=c.univ_colg_id where c.univ_id=%s and r.institution_type=%s''',(univ_id, institution_type))
                    elif institution_type == '3':
                        cur.execute('''select 'Nil','Nil',ce.univ_center_name,r.filled_patent,r.granted_patent,r.fund_generated,r.faculty_name,r.description,r.institution_type from univ_patent r left join univ_centers ce on r.univ_center_id=ce.univ_center_id where ce.univ_id=%s and r.institution_type=%s''',(univ_id, institution_type))
                    else:
                        cur.execute('''select d.dept_code,'Nil','Nil',r.filled_patent,r.granted_patent,r.fund_generated,r.faculty_name,r.description,r.institution_type from univ_patent r left join univ_departments d on r.dept_id= d.dept_id where d.univ_id=%s and r.institution_type=%s union all select 'Nil',c.college_code,'Nil',r.filled_patent,r.granted_patent,r.fund_generated,r.faculty_name,r.description,r.institution_type from univ_patent r left join univ_colleges c on r.univ_colg_id=c.univ_colg_id where c.univ_id=%s and r.institution_type=%s union all select 'Nil','Nil',ce.univ_center_name,r.filled_patent,r.granted_patent,r.fund_generated,r.faculty_name,r.description,r.institution_type from univ_patent r left join univ_centers ce on r.univ_center_id=ce.univ_center_id where ce.univ_id=%s and r.institution_type=%s''',(univ_id,1,univ_id,2,univ_id,3) )
                    r = cur.fetchall()
                else:
                    r = -5
                return jsonify(r)
    except Exception as e:
        return {'error': str(e)}




@app.route('/univ_publication', methods=['POST', 'GET'])  # ------------------Get all the departments
def univ_publication():
    try:
        if request.is_json:
                data = request.json
                private_key = data['private_key']
                univ_id = data['univ_id']
                institution_type = data['institution_type']
                r = ''
                validate_res = validate_private_key(private_key)

                if validate_res == 1:
                    cur = mysql.connect().cursor()
                    if institution_type == '1':
                        cur.execute(
                            '''select d.dept_code,'Nil','Nil',r.publication_type,r.journal_name,r.journal_details,r.citation,r.impact_index,r.type_of_journal,r.faculty_name,r.publication_brief,r.institution_type from univ_publications r left join univ_departments d on r.dept_id=d.dept_id where d.univ_id=%s and r.institution_type=%s''', (univ_id, institution_type))
                    elif institution_type == '2':
                        cur.execute(
                            '''select 'Nil',c.college_code,'Nil',r.publication_type,r.journal_name,r.journal_details,r.citation,r.impact_index,r.type_of_journal,r.faculty_name,r.publication_brief,r.institution_type from univ_publications r left join univ_colleges c on r.univ_colg_id=c.univ_colg_id where c.univ_id=%s and r.institution_type=%s''',(univ_id, institution_type))
                    elif institution_type == '3':
                        cur.execute(
                            '''select 'Nil','Nil',ce.univ_center_name,r.publication_type,r.journal_name,r.journal_details,r.citation,r.impact_index,r.type_of_journal,r.faculty_name,r.publication_brief,r.institution_type from univ_publications r left join univ_centers ce on r.univ_center_id=ce.univ_center_id where ce.univ_id=%s and r.institution_type=%s''',(univ_id, institution_type))
                    else:
                        cur.execute(
                            '''select d.dept_code,'Nil','Nil',r.publication_type,r.journal_name,r.journal_details,r.citation,r.impact_index,r.type_of_journal,r.faculty_name,r.publication_brief,r.institution_type from univ_publications r left join univ_departments d on r.dept_id= d.dept_id where d.univ_id=%s and r.institution_type=%s union all select 'Nil',c.college_code,'Nil',r.publication_type,r.journal_name,r.journal_details,r.citation,r.impact_index,r.type_of_journal,r.faculty_name,r.publication_brief,r.institution_type from univ_publications r left join univ_colleges c on r.univ_colg_id=c.univ_colg_id where c.univ_id=%s and r.institution_type=%s union all select 'Nil','Nil',ce.univ_center_name,r.publication_type,r.journal_name,r.journal_details,r.citation,r.impact_index,r.type_of_journal,r.faculty_name,r.publication_brief,r.institution_type from univ_publications r left join univ_centers ce on r.univ_center_id=ce.univ_center_id where ce.univ_id=%s and r.institution_type=%s''',(univ_id, 1, univ_id, 2, univ_id, 3))
                    r = cur.fetchall()
                    #print(cur._last_executed)
                    #print(r)
                else:
                    r = -5
                return jsonify(r)
    except Exception as e:
        return {'error': str(e)}



@app.route('/univ_conference', methods=['POST', 'GET'])  # ------------------Get all the departments
def univ_conference():
    try:
        if request.is_json:
                data = request.json
                private_key = data['private_key']
                univ_id = data['univ_id']
                institution_type = data['institution_type']
                r = ''
                validate_res = validate_private_key(private_key)
                #validate_res = 1
                if validate_res == 1:
                    cur = mysql.connect().cursor()
                    if institution_type == '1':
                        cur.execute(
                            '''select d.dept_code,'Nil','Nil',r.conference_name,r.conference_type,r.conference_year,r.brief_description,r.institution_type from univ_conference r left join univ_departments d on r.dept_id=d.dept_id where d.univ_id=%s and r.institution_type=%s''', (univ_id, institution_type))
                    elif institution_type == '2':
                        cur.execute(
                            '''select 'Nil',c.college_code,'Nil',r.conference_name,r.conference_type,r.conference_year,r.brief_description,r.institution_type from univ_conference r left join univ_colleges c on r.univ_colg_id=c.univ_colg_id where c.univ_id=%s and r.institution_type=%s''',(univ_id, institution_type))
                    elif institution_type == '3':
                        cur.execute(
                            '''select 'Nil','Nil',ce.univ_center_name,r.conference_name,r.conference_type,r.conference_year,r.brief_description,r.institution_type from univ_conference r left join univ_centers ce on r.univ_center_id=ce.univ_center_id where ce.univ_id=%s and r.institution_type=%s''',(univ_id, institution_type))
                    else:
                        cur.execute(
                            '''select d.dept_code,'Nil','Nil',r.conference_name,r.conference_type,r.conference_year,r.brief_description,r.institution_type from univ_conference r left join univ_departments d on r.dept_id= d.dept_id where d.univ_id=%s and r.institution_type=%s union all select 'Nil',c.college_code,'Nil',r.conference_name,r.conference_type,r.conference_year,r.brief_description,r.institution_type from univ_conference r left join univ_colleges c on r.univ_colg_id=c.univ_colg_id where c.univ_id=%s and r.institution_type=%s union all select 'Nil','Nil',ce.univ_center_name,r.conference_name,r.conference_type,r.conference_year,r.brief_description,r.institution_type from univ_conference r left join univ_centers ce on r.univ_center_id=ce.univ_center_id where ce.univ_id=%s and r.institution_type=%s''',(univ_id, 1, univ_id, 2, univ_id, 3))

                    r = cur.fetchall()
                    #print(r)
                else:
                    r = -5
                return jsonify(r)
    except Exception as e:
        return {'error': str(e)}


@app.route('/eminent_person_visit', methods=['POST', 'GET'])  # ------------------Get all the departments
def eminent_person_visit():
    try:
        if request.is_json:
                data = request.json
                private_key = data['private_key']
                univ_id = data['univ_id']
                institution_type = data['institution_type']
                r = ''
                validate_res = validate_private_key(private_key)

                if validate_res == 1:
                    cur = mysql.connect().cursor()
                    if institution_type == '1':
                        cur.execute(
                            '''select d.dept_code,'Nil','Nil',r.programme_name,r.eminent_person_name,r.programme_year,r.brief_description,r.institution_type from univ_eminent_person_visit r left join univ_departments d on r.dept_id=d.dept_id where d.univ_id=%s and r.institution_type=%s''',(univ_id, institution_type))
                    elif institution_type == '2':
                        cur.execute(
                            '''select '',c.college_code,'Nil',r.programme_name,r.eminent_person_name ,r.programme_year,r.brief_description,r.institution_type from univ_eminent_person_visit r left join univ_colleges c on r.univ_colg_id=c.univ_colg_id where c.univ_id=%s and r.institution_type=%s''',(univ_id, institution_type))
                    elif institution_type == '3':
                        cur.execute(
                            '''select 'Nil','Nil',ce.univ_center_name,r.programme_name,r.eminent_person_name ,r.programme_year,r.brief_description,r.institution_type from univ_eminent_person_visit r left join univ_centers ce on r.univ_center_id=ce.univ_center_id where ce.univ_id=%s and r.institution_type=%s''',(univ_id, institution_type))
                    else:
                        cur.execute(
                            '''select d.dept_code,'Nil','Nil',r.programme_name,r.eminent_person_name ,r.programme_year,r.brief_description,r.institution_type from univ_eminent_person_visit r left join univ_departments d on r.dept_id= d.dept_id where d.univ_id=%s and r.institution_type=%s union all select 'Nil',c.college_code,'Nil',r.programme_name,r.eminent_person_name ,r.programme_year,r.brief_description,r.institution_type from univ_eminent_person_visit r left join univ_colleges c on r.univ_colg_id=c.univ_colg_id where c.univ_id=%s and r.institution_type=%s union all select 'Nil','Nil',ce.univ_center_name,r.programme_name,r.eminent_person_name ,r.programme_year,r.brief_description,r.institution_type from univ_eminent_person_visit r left join univ_centers ce on r.univ_center_id=ce.univ_center_id where ce.univ_id=%s and r.institution_type=%s''',(univ_id, 1, univ_id, 2, univ_id, 3))
                    r = cur.fetchall()
                    #print(r)
                else:
                    r = -5
                return jsonify(r)
    except Exception as e:
        return {'error': str(e)}








@app.route('/univ_fee_structure',methods=['POST', 'GET'])#------------------Get all the syndicatemembers
def univ_fee_structure():
    try:
        if request.is_json:
            data = request.json
            univ_id = data['univ_id']
            purpose = data['purpose']
            print(purpose)
            #private_key = data['private_key']
            r = ''
            #validate_res = validate_private_key(private_key)
            validate_res = 1
            if validate_res == 1:
                cur = mysql.connect().cursor()
                print('kkkkk')
                if (purpose != ''):
                    cur.execute('''select univ_id,purpose,link from univ_fee_structure where univ_id=%s and purpose=%s ''',(univ_id,purpose))
                else:
                    print('else')
                    cur.execute('''select univ_id,purpose,link from univ_fee_structure where univ_id=%s ''',(univ_id))
                r = cur.fetchall()
                print(cur._last_executed)
                #print(r)
            else:
               r = -5

            print(r)
            return jsonify(r)

    except Exception as e:
        return {'error': str(e)}
































if __name__ == '__main__':
    app.run(debug=True,port=5001)

