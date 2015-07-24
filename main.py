import sys
import time
import threading

import subprocess
import BaseHTTPServer
from urlparse import urlparse


# Terraria Server controller
class Server:
    # Initializer
    def __init__(self):
        self.isOn = False
        self.port = 7777

    def handleCommands(self, command):
        if command[:6] == "start_":
            if self is not None:
                print self.getIsOn()
                if self.getIsOn():
                    self.stop()
            if command[6] != 'n' and command[6] != 'd':
                self.start(command[6:])
        else:
            self.console(command)

    # Reads from servers console then log it
    # Run in seperate thread
    def readline(self):
        while True:
            text = self.server.stdout.readline()
            sys.stdout.write(text)
            if text != "":
                if text[0] == "<":
                    name = text[1:text.index(">")]
                    print name + " command: " + text[text.index(">") + 2:]
                    if text[text.index(">") + 2] == "/":
                        players = ["A Bum", "The One"]
                        if any(name in s for s in players):
                            print "handled"
                            self.handleCommands(text[text.index(">") + 3:])
                else:
                    self.server.stdin.write("say " + text)
            time.sleep(0.01)

    # Writes to the console
    def console(self, command):
        if "exit" in command:
            self.isOn = False
        self.server.stdin.write(command + "\n")

    # Starts server
    def start(self, world):
        self.isOn = True
        self.server = subprocess.Popen(
            ["TerrariaServer"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        self.readerthread = threading.Thread(target=self.readline)
        self.readerthread.start()

        time.sleep(1)
        self.console(str(world) + "\n\n" + str(self.port) + "\n\n\n")

    def stop(self):
        if self.isOn:
            self.server.stdin.write("exit\n")
        self.isOn = False
        time.sleep(2)

    def getIsOn(self):
        return self.isOn


class HttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    serverTerraria = Server()

    def handleCommands(self, command):
        if command[:6] == "start_":
            if self.serverTerraria is not None:
                print self.serverTerraria.getIsOn()
                if self.serverTerraria.getIsOn():
                    self.serverTerraria.stop()
            if command[6] != 'n' and command[6] != 'd':
                self.serverTerraria.start(command[6:])
        else:
            self.serverTerraria.console(command)

    def isPassword(self, password):
        if password == "pass":
            return True
        return False

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self.url = urlparse(self.path)

        if self.isPassword(self.url.query):
            page = open("data.html", 'r')
            self.wfile.write(page.read())
            page.close()

            self.handleCommands(self.url.path[1:])
        else:
            self.wfile.write("Incorrect password")


class HttpServer:
    def start(self):
        self.serverHttp = BaseHTTPServer.HTTPServer(('', 9999), HttpHandler)
        try:
            self.serverHttp.serve_forever()
        except KeyboardInterrupt:
            pass
        self.serverHttp.server_close()


# server = Server()

if __name__ == "__main__":
    b = HttpServer()
    b.start()
