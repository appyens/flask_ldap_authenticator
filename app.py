import os
import ldap
from configparser import ConfigParser
from flask import Flask, Response, render_template, request, redirect, url_for

app = Flask(__name__)
conf = ConfigParser()
conf.read(os.path.join(__file__, 'setup.conf'))

ad_server = conf.get('AD', 'server')
ad_domain = conf.get('AD', 'domain')


def authenticate(username, password, address=ad_server):
    conn = ldap.initialize('ldap://' + address)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    return conn.simple_bind_s(username + ad_domain, password)


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            check = authenticate(username=username, password=password)
            if not isinstance(check, ldap.INVALID_CREDENTIALS):
                return redirect(url_for('login_success'))
        return render_template('login.html')
    except Exception:
        return Response("Invalid Credentials", status=401)


@app.route('/login/success', methods=['GET'])
def login_success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(host='172.16.0.207')
