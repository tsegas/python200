import socket
import sys
import os
from pathlib import Path
import mimetypes
import pathlib
import re
from os import path
import struct
import io


def response_ok(body=b"this is a pretty minimal response", mimetype=b"content-type: text/plain"):
    """returns a basic HTTP response"""
    resp = []
    resp.append(b"HTTP/1.1 200 OK")
    #resp.append(b"Content-Type: text/plain")
    resp.append(mimetype)
    resp.append(b"")
    #resp.append(b"this is a pretty minimal response")
    resp.append(body)
    return b"\r\n".join(resp)


def response_method_not_allowed():
    """returns a 405 Method Not Allowed response"""
    resp = []
    resp.append("HTTP/1.1 405 Method Not Allowed")
    resp.append("")
    return "\r\n".join(resp).encode('utf8')


def response_not_found():
    """returns a 404 Not Found response"""
    resp = []
    resp.append("HTTP/1.1 404 Not Found")
    resp.append("")
    return "\r\n".join(resp).encode('utf8')
    #return b""


def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    print('first_line???...................',first_line)
    method, uri, protocol = first_line.split()
    print('method...................',method)
    print('uri...................',uri)
    print('protocol...................',protocol)
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    return uri


def resolve_uri(uri):
    """This method should return appropriate content and a mime type"""
    #uriPath = uri.replace('/', '')
    uriPath = re.sub("^/|/$", "", uri)
    print('uriPath........22222...........',uriPath)
    rootPath = 'webroot'
    print('rootPath........rrrrrr...........',rootPath)
    #inputPath = os.path.join("/webroot", uriPath)
    inputPath = os.path.join(os.path.sep, rootPath, uriPath)
    inputPath = re.sub("^/|/$", "", inputPath)
    #path = root + uri
    print('inputPath........pppppp...........',inputPath)
    #directory_uri = root.read_bytes()
    #directory_uri = "/{0}".format(directory[len(root):])
    #print('dir........ddddd...........',directory_uri)
    if uri == "/" :
        bytList = b''
        dirList = os.listdir(inputPath)
        print('dirList........dirList...........',dirList)
        for i in dirList :
            byt = str.encode(i)
            bytList += byt
        print('bytList........bytList...........',bytList)

   # if (".txt" or ".png" or ".jpg" or ".py" or "a_web_page") in uri :
    #fileList = [".ttt"]
    fileImg = [".jpg", ".png", "a_web_page", ".py", ".txt"]
   # fileInt = ["int"]
   # if any(substring in string ".txt", ".png", ".jpg", ".py", "a_web_page") in uri :
   # if any(substring in string for fileList in uri)
    # for sufix in fileList:
    #     if sufix in uri :
    #         fileBytes = b''
    #         filename = path.relpath(inputPath)
    #         if os.path.isfile(filename) :
    #             print("TRUE...........")
    #         else :
    #             print("WRONG FILE PATH...........")
    #         f = open(filename, 'rb+')
    #         print('filename........TXTfilename!!!!!!!!!...........',f.name)
    #         #open(filename, 'r')
    #         txtCont = f.read()
    #         f.close()
    #        # print('txtCont........txtCont!!!!!!!!!...........',txtCont)
    #         for i in txtCont :
    #             eachByte = str.encode(i)
    #             fileBytes += eachByte
           # print('fileBytes........fileBytes!!!!!!!!!!!!!!!!!!!...........',fileBytes)
    for sufix in fileImg:
        if sufix in uri :
            fileBytes = b''
            filename = path.relpath(inputPath)
            if os.path.isfile(filename) :
                print("TRUE...........")
            else :
                print("WRONG FILE PATH...........")
            f = open(filename, 'rb')
            txtCont = io.BytesIO(f.read())
            print('filename........IMGfilename!!!!!!!!!...........',f.name)
            #open(filename, 'r')
          #  txtCont = f.read()
            f.close()
           # print('txtCont........txtCont!!!!!!!!!...........',txtCont)
            for i in txtCont :
               # eachByte = str.encode(i)
                fileBytes += i
           # print('fileBytes........fileBytes!!!!!!!!!!!!!!!!!!!...........',fileBytes)
    # for sufix in fileInt:
    #     if sufix in uri :
    #         fileBytes = b''
    #         filename = path.relpath(inputPath)
    #         if os.path.isfile(filename) :
    #             print("TRUE...........")
    #         else :
    #             print("WRONG FILE PATH...........")
    #         f = open(filename, 'rb')
    #         txtCont = io.BytesIO(f.read())
    #         print('filename........INTfilename!!!!!!!!!...........',f.name)
    #         #open(filename, 'r')
    #         #txtCont = f.read()
    #         f.close()
    #        # print('txtCont........txtCont!!!!!!!!!...........',txtCont)
    #         for i in txtCont :
    #            # eachByte = bytes(i)
    #             fileBytes += i

    # if ".jpg" in uri :
    #     fileBytes = b''
    #     filename = path.relpath(inputPath)
    #     if os.path.isfile(filename) :
    #         print("TRUE...........")
    #     else :
    #         print("WRONG FILE PATH...........")
    #     #f = open(filename, 'rb+')
    #     f = open(filename, 'rb')
    #     txtCont = io.BytesIO(f.read())
    #     print('filename........filename!!!!!!!!!...........',f.name)
    #     #open(filename, 'r')
    #    # txtCont = f.read()
    #     f.close()
    #    # print('txtCont........txtCont!!!!!!!!!...........',txtCont)
    #     for i in txtCont :
    #        # eachByte = bytes(i)
    #         fileBytes += i
      #  print('fileBytes........fileBytes!!!!!!!!!!!!!!!!!!!...........',fileBytes)

    #dirList = os.listdir(inputPath)
    #print('dirList........dirList...........',dirList)

    if "missing" in uri:
        #mime_type = b'content-type: text/html'
        raise NameError("Name error")
        mime_type = response_not_found()
        content = b"content-type: text/html"
    elif ".py" in uri:
        mime_type = b"text/x-python"
        content = fileBytes
       # print('content........ccccc????...........',fileBytes)
        #content = b"content-type: image/jpeg" 
        #content = inputPath.read_bytes()
    elif '.jpg' in uri:
        mime_type = b'image/jpeg'
        content = fileBytes
      #  print('content........ccccc????...........',fileBytes)

     #   print('inputPath........file???????...........',inputPath)
      #  content = inputPath.read()
      #  print('content........ccccc????...........',content)
        #content = b'image/jpeg'
    elif '.png' in uri:
        mime_type = b'image/png'
        content = fileBytes
       # print('content........ccccc????...........',fileBytes)

        #print('inputPath........file???????...........',inputPath)
        #content = inputPath.read()
      #  print('content........ccccc????...........',content)
        #content = b'JPEG_example.jpg'
    elif "sample.txt" in uri:
        mime_type = b'text/plain'
        content = fileBytes
       # print('content........ccccc????...........',fileBytes)
        #content = b"a_web_page.html, images, make_time.py, sample.txt" 
    elif "a_web_page" in uri:
        mime_type = b'text/html'
        content = fileBytes
        print('content........ccccc????...........',fileBytes)
       # content = b"webroot/a_web_page.html"
       # content = b"a_web_page.html, images, make_time.py, sample.txt" 
    elif "/" in uri:
        mime_type = b'text/plain'
       # dirList = os.listdir(inputPath)
        print('bytList......../////...........',bytList)
        content = bytList
       # print('content........content...........',content)
        #content = b"a_web_page.html, images, make_time.py, sample.txt" 
    # elif ".html" in uri:
    #     mime_type = b'text/html'
    #     content = b"a_web_page.html" 
    else :
        mime_type = b"text/plain"
        content = b"This is a pretty minimal response"
     #   content = b"This is a pretty minimal response" text/x-python
    #return b"still broken", b"text/plain"
    #content = b"This is a pretty minimal response"
    return content, mime_type


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                request = ''
                while True:
                    data = conn.recv(1024)
                    print('data!!!!...................',data)
                    request += data.decode('utf8')
                    print('request...................',request)
                    if len(data) < 1024:
                        break

                try:
                    uri = parse_request(request)
                except NotImplementedError:
                    response = response_method_not_allowed()
                else:
                    try:
                        content, mime_type = resolve_uri(uri)
                    except NameError:
                        response = response_not_found()
                    else:
                        response = response_ok(content, mime_type)

                print('sending response', file=log_buffer)
                conn.sendall(response)
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
