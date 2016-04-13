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


def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    return uri


def resolve_uri(uri):
    """This method should return appropriate content and a mime type"""

    """ param uri: Provides information for looking up resources. specifies
                   the pathname for a file in the directory structure. 
        return value content: specifies the content of a file or directory.
        return value mime_type: specifies mime_type of file/directory content. """
   
    # Remove leading slash from uri
    uriPath = re.sub("^/|/$", "", uri)
    rootPath = 'webroot'
    inputPath = os.path.join(os.path.sep, rootPath, uriPath)

    # Remove leading slash from path
    inputPath = re.sub("^/|/$", "", inputPath)

    # When uri is the a directory, get the path to the root directory
    if uri == "/" :
        bytList = b''
        bytListAdd = b''
        dirList = os.listdir(inputPath)

        len_dirList = len(dirList)

        # Loop through list to get the content of the direcctory
        for i,j in enumerate(dirList):
            if (i <len_dirList-1):
                byte = j + ', '
            else :
                byte = j
            byteSumm = str.encode(byte)
            bytList += byteSumm

    # List of file extentions
    fileList = [".jpg", ".png", "a_web_page", ".py", ".txt"]
    
    # Get the file content for the files in the directory specified by uri
    for fileExt in fileList:
        if fileExt in uri :
            fileBytes = b''
            filename = path.relpath(inputPath)
            if os.path.isfile(filename) :
                #print("This is a valid file", filename)
                print("{0} is a valid file".format(filename))
            else :
                print("{0} is NOT a valid file".format(filename))
            f = open(filename, 'rb')
            txtCont = io.BytesIO(f.read())
            f.close()
            for i in txtCont :
                fileBytes += i

    # Assign the return values based on the type of argument in uri
    if "missing" in uri:
        raise NameError("Name error")
        content = b"content-type: text/html"
        mime_type = response_not_found()
    elif ".py" in uri:
        content = fileBytes
        mime_type = b"text/x-python"
    elif '.jpg' in uri:
        content = fileBytes
        mime_type = b'image/jpeg'
    elif '.png' in uri:
        content = fileBytes
        mime_type = b'image/png'
    elif ".txt" in uri:
        content = fileBytes
        mime_type = b'text/plain'
    elif "a_web_page" in uri:
        content = fileBytes
        mime_type = b'text/html'
    elif "/" in uri:
        content = bytList
        mime_type = b'text/plain'
    else :
        content = b"This is a pretty minimal response"
        mime_type = b"text/plain"
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
                    request += data.decode('utf8')
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
