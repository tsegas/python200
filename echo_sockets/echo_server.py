import socket
import sys
import select


def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000)
    # TODO: Replace the following line with your code which will instantiate
    #       a TCP socket with IPv4 Addressing, call the socket you make 'sock'
    #sock = None
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Set a timeout option for the server socket so that it will close if the client doesn't response
    #  for a period of time
    sock.settimeout(10)

    # TODO: You may find that if you repeatedly run the server script it fails,
    #       claiming that the port is already used.  You can set an option on
    #       your socket that will fix this problem. We DID NOT talk about this
    #       in class. Find the correct option by reading the very end of the
    #       socket library documentation:
    #       http://docs.python.org/3/library/socket.html#example

    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # TODO: bind your new sock 'sock' to the address above and begin to listen
    #       for incoming connections
    sock.bind(address)
    sock.listen(1)

    # set the exception to use the timeout for the socket
    KeyboardInterrupt = socket.timeout

    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)

            # TODO: make a new socket when a client connects, call it 'conn',
            #       at the same time you should be able to get the address of
            #       the client so we can report it below.  Replace the
            #       following line with your code. It is only here to prevent
            #       syntax errors
            #addr = ('bar', 'baz')
            conn, addr = sock.accept()
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                while True:
                    # TODO: receive 16 bytes of data from the client. Store
                    #       the data you receive as 'data'.  Replace the
                    #       following line with your code.  It's only here as
                    #       a placeholder to prevent an error in string
                    #       formatting
                    #data = b''
                    data = conn.recv(16)
                    print('received........... "{0}"'.format(data.decode('utf8')))
                    # TODO: Send the data you received back to the client, log
                    # the fact using the print statement here.  It will help in
                    # debugging problems.
                    conn.sendall(data)
                    print('sent.......... "{0}"'.format(data.decode('utf8')))
                    # TODO: Check here to see if the message you've received is
                    # complete.  If it is, break out of this inner loop.
                    if not data: break
                    #from_server = conn.recv(16)
                    #if from_server == data :
                      #break
            finally:
                # TODO: When the inner loop exits, this 'finally' clause will
                #       be hit. Use that opportunity to close the socket you
                #       created above when a client connected.
                conn.close()
                print(
                    'echo complete, client connection closed', file=log_buffer
                )
    except KeyboardInterrupt:
        # TODO: Use the python KeyboardInterrupt exception as a signal to
        #       close the server socket and exit from the server function.
        #       Replace the call to `pass` below, which is only there to
        #       prevent syntax problems
        #pass
        if KeyboardInterrupt == socket.timeout :
            print('Timed out waiting for a connection', file=log_buffer)

        sock.close()
        print('quitting echo server', file=log_buffer)


if __name__ == '__main__':
    server()
    sys.exit(0)