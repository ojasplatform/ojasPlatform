import subprocess

subprocess.call(["mitmproxy", "-s /home/dsampath/temp/mitmproxy/examples/ojas/ojasProxy.py "])
output = subprocess.check_output(["ps -ef | grep '[p]ython /etc/speech/TTSserver.py' | awk '{ print $2 }'"])
print output

