#! /usr/bin/env python
#
# See README for usage instructions.
import glob
import os
import subprocess
import sys
import platform
import shutil

protoc = "./protoc.exe"
target = "../src/pb2"

def generate_proto(source, require = True):

  if not require and not os.path.exists(source):
    return

  if protoc is None:
    sys.stderr.write(
      "protoc is not installed nor found in ../src.  Please compile it "
      "or install the binary package.\n")
    sys.exit(-1)

  protoc_command = [ protoc, "-I.", "-I.", "--python_out=.", source ]
  if subprocess.call(protoc_command) != 0:
    sys.exit(-1)

  output = source.replace(".proto", "_pb2.py")
  shutil.move(output, target)

subprocess.call([ protoc, "--version"])

# clear target dir
if os.path.exists(target):
  shutil.rmtree(target)
os.mkdir(target)

generate_proto("login.proto")
generate_proto("position.proto")
