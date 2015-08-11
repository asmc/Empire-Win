import os
from urllib import urlopen

ez_file_name = 'install_easy_setup.py'
m2_file_name = 'install_M2Crypto.py'

data = urlopen('http://peak.telecommunity.com/dist/ez_setup.py')
with open(ez_file_name, 'wb') as f:
    f.write(data.read())
os.system('python %s' % (os.path.join(os.getcwd(),ez_file_name)))

os.system('easy_install pip')
os.system('pip install pyreadline')
os.system('pip install iptools')
os.system('pip install pydispatcher')


data = urlopen('https://github.com/saltstack/salt-windows-install/blob/master/deps/win-amd64-py2.7/M2Crypto-0.21.1.win-amd64-py2.7.exe?raw=true')
with open(m2_file_name, 'wb') as f:
    f.write(data.read())
os.system( os.path.join(os.getcwd(),m2_file_name) )

os.unlink( os.path.join(os.getcwd(),ez_file_name) )
os.unlink( os.path.join(os.getcwd(),m2_file_name) )
