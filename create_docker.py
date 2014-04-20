#!/usr/bin/python3  
# Credit https://github.com/oskarhane/dockerpress Written by Oskar Hane <oh@oskarhane.com>
# Credit http://geraldkaszuba.com/quickly-ssh-into-a-docker-container/

import subprocess
import sys
import re
import shutil
import json

from optparse import OptionParser

def create_nginx_config(container_id):
    command = ["docker ps | grep " + container_id[:6]]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    d_str = output.decode("utf-8")
    p.stdout.close()
    domain = re.findall('\s([\S]+)\s*$', d_str)

    port = get_docker_port(container_id[:6],80)
    if not(port):
        return 'Port 80 not open'
    print ('{0} {1} {2}'.format(container_id[:6], domain[0], port))
    conf_test = write_and_test_nginx_config(container_id[:6], domain[0], port)
    if not(conf_test):
        return 'Error in Nginx config. Check file.'
    return True

#Expected response Testing nginx configuration: nginx.
def write_and_test_nginx_config(container_id, url, port):
    conf_dir = '/etc/nginx/sites-enabled/'
    fail_dir = '/etc/nginx/sites-available/'

    conf_str = get_nginx_conf(container_id, url, port)
    f = open(conf_dir + url, 'w+')
    f.write(conf_str)
    f.close()

    test_command = ["/etc/init.d/nginx configtest"]
    p_ok = subprocess.Popen(test_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    ok_output, err = p_ok.communicate()
    err_response = err.decode("utf-8")
    p_ok.stdout.close()
    p_ok.stderr.close()
    if not(re.search('(failed)', err_response)):
        return True
    else:
        shutil.move(conf_dir + url, fail_dir + url)
        return False

def get_port_from_address(address):
    port = re.search(':([0-9]+)\s*$', address).group(1)
    return port


def get_nginx_conf(container_id, url, http_port):
    listen_str = 'upstream ' + container_id + " {\n"
    listen_str += "\tserver 127.0.0.1:" + http_port + ";\n}\n"    
    listen_str += 'server {\n'
    listen_str += "\tlisten 80;\n"
    listen_str += "\tserver_name " + url + ";\n"
    listen_str += "\tlocation / {\n"
    listen_str += "\t\tproxy_pass http://" + container_id + ";\n"
    listen_str += "\t\tproxy_set_header X-Real-IP $remote_addr;\n"
    listen_str += "\t\tproxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n"
    listen_str += "\t\tproxy_set_header X-NginX-Proxy true;\n"
    listen_str += "\t\tproxy_set_header Host $host;\n"
    listen_str += "\t\tproxy_redirect off;\n"
    listen_str += "\t}\n"
    listen_str += "}"

    return listen_str

def create_docker_action(options):
    if not (options.url):
        parser.error("You must provide a URL to create a site for")
    if not (re.search('^([a-z0-9\.-]+\.[a-z]{2,4})$', options.url)):
        parser.error('The given url is not a valid domain')
    
    create_project_specifc_dockerfile(options.project_code,options.maintainer)
    image_tag = create_docker_project_image(options.project_code)
    container_id = create_docker_container(options.url, image_tag)
    print ("Container created: {0}".format(container_id))
    nginx_conf = create_nginx_config(container_id)

    if(nginx_conf == True):
        print('All ok, you can safetly reload nginx now. service nginx reload')
    else:
        print('Nginx config failed. Please check file /etc/nginx/sites-available/' + options.url)
        print (nginx_conf)

def get_docker_port(container_id,container_port):
    command = ['docker port {} {}'.format(container_id,container_port)]
    output = subprocess.check_output(command, shell=True).decode('utf-8')
    #subprocess.stdout.close()
    return get_port_from_address(output)

def create_project_specifc_dockerfile(project_code,maintainer):
    dockerfile_content = """
    FROM {image}
    MAINTAINER {maintainer}
    ENV PROJECT_CODE {project_code}

    ADD ./id_rsa_$PROJECT_CODE.pub /root/.ssh/
    RUN cat /root/.ssh/id_rsa_$PROJECT_CODE.pub  >> /root/.ssh/authorized_keys
    RUN chmod 600 /root/.ssh/authorized_keys

    RUN echo "$PROJECT_CODE" >>/home/index.html
    CMD  /usr/sbin/sshd -D
    CMD cd /home && python -m SimpleHTTPServer 80 &

    """.format(project_code=project_code,image="open-platform-hk/bootstrap:0.1", maintainer=maintainer)
    ##Docker don't support other file name while with context 
    target=open ("Dockerfile",'w')
    target.write(dockerfile_content)
    target.close

def create_docker_project_image(project_code):
    tag = project_code+":0.1"
    command = ["docker build -t {tag} .".format(tag=tag)]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    container_id = output.decode("utf-8")
    p.stdout.close()
    return tag

def create_docker_container(url,image_tag):
    image = image_tag
    command = "bin/bash"
    command = ["docker run -d -t -i -p 80 -p 22 --name '{url}' {image} {command}".format( url=url,image=image, command=command)]
    p = subprocess.Popen(command, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    container_id = output.decode("utf-8")

    ##TODO err handling
    p.stderr.close()
    p.stdout.close()
    return container_id

if __name__ == "__main__":
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    parser.add_option("--code", dest="project_code", help="Project Code to create a site for.")
    parser.add_option("--id", dest="container_id", help="Container id to ssh.")
    parser.add_option("--action", dest="action", help="Action")
    parser.add_option("--maintainer", dest="maintainer", help="Maintainer")

    options, args = parser.parse_args()
    options.url = '{project_code}.dev.code4.hk'.format(project_code=options.project_code) 

    if not (options.maintainer):
        options.maintainer=''

    if (options.action == 'ssh'):
        get_docker_port(options.container_id,22)
    else:
        create_docker_action(options)

