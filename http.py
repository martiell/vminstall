#!/usr/bin/env python
from os import getcwd, sep, unlink
from os.path import abspath, exists
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from subprocess import Popen, PIPE, call, check_call
from xml.dom.minidom import parseString
from threading import Thread

class InstallRequestHandler(BaseHTTPRequestHandler):

  def do_GET(s):
    """Respond to a GET request."""
    if (s.path).startswith('/shutdown'):
      s.send_response(200)
      Thread(target=s.server.shutdown).start()
      return
    p = abspath(getcwd() + s.path)
    if p.startswith(getcwd()) and exists(p):
      s.send_response(200)
      s.end_headers()
      f = open(p)
      content = f.read()
      if (s.path == '/./preseed.cfg'):
        content += "\nd-i mirror/http/proxy string http://192.168.101.1:3142/"
      s.wfile.write(content)
      f.close()
    else:
      s.send_response(404)

def bindAddress():
  p = Popen(['virsh', '-cqemu:///system', 'net-dumpxml', 'default'], stdout=PIPE)
  (out, err) = p.communicate()
  xml = parseString(out)
  ip = xml.documentElement.getElementsByTagName('ip')[0].attributes['address'].value
  return ip.encode('utf-8')

def main():
  try:
    address=bindAddress()
    port=8001
    server = HTTPServer((address, port), InstallRequestHandler)
    srvThread = Thread(target=server.serve_forever)
    srvThread.setDaemon(True)
    srvThread.start()
    hostname="test"
    url=address + ":" + str(port) + "/./preseed.cfg"
    call(["virsh", "-c", "qemu:///system", "destroy", hostname])
    call(["virsh", "-c", "qemu:///system", "undefine", hostname])
    try:
      unlink("disk")
    except OSError:
      pass
    check_call(["virt-install",
      "--noreboot",
      "--connect=qemu:///system",
      "-n", hostname,
      "-r", "128",
      "--video=vga",
      "--disk", "path=disk,bus=scsi,size=1",
      "-l", "installer-amd64",
      "-x", "auto=true hostname=" + hostname + " domain= url=http://" + url +
        " DEBCONF_DEBUG=5 quiet hw-detect/start_pcmcia=false"])
  except KeyboardInterrupt:
    server.socket.close()

if __name__ == '__main__':
  main()
