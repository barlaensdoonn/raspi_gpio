#!/usr/bin/python3
# control relay via gpio and received sockets
# 8/5/17
# updated 11/26/17

# NOTE: must start pigpio as daemon before running script: sudo pigpiod

import logging
import gpio_util
import socketserver


class TCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the client.
    """

    def parse_msg(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024)
        self.decoded = self.data.decode().strip()
        logging.info("{} wrote: {}".format(self.client_address[0], self.decoded))

    def get_state(self):
        states = {'on': 1, 'off': 0}

        if self.decoded in states.keys():
            self.state = states[self.decoded]
            logging.debug('set self.state to {}'.format(states[self.decoded]))
        else:
            self.state = None

    def handle(self):
        # TODO: maybe send back state so client app can store it
        logging.debug('client {} connected'.format(self.client_address[0]))
        self.parse_msg()
        self.get_state()

        if self.state == 1 or self.state == 0:
            logging.info('writing {} to pin {}'.format(self.state, self.server.switch))
            self.server.pi.write(self.server.switch, self.state)
        else:
            logging.warning("invalid command '{}' received, ignoring...".format(self.decoded))

    def finish(self):
        '''finish method is always called by the base handler after handle method has completed'''
        logging.info('<> <> <> <> <> <> <> <> <> <> <> <>')


def initialize():
    switch = 4  # gpio pin controlling relay
    hostport = ('', 9999)

    logging.debug('initializing open server on port {}'.format(hostport[1]))
    server = socketserver.TCPServer(hostport, TCPHandler)
    server.switch = switch
    server.pi = gpio_util.initialize_pigpiod(server.switch)

    return server


if __name__ == '__main__':
    log_path = 'logs/gpio_socket.log'
    logging.basicConfig(filename=log_path, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level=logging.DEBUG)

    server = initialize()

    try:
        server.serve_forever()
    except Exception as e:
        logging.error('{}'.format(e))
    except KeyboardInterrupt:
        logging.info('...user exit received...')
        logging.info('<> <> <> <> <> <> <> <> <> <> <> <>')
