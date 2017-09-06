---
title: Setting up a Python Virtualenv for SpiNNaker
---

These instructions will install the required packages only in a virtualenv.  This can help when you don't have root access or are on a shared machine.  Additionally, it will help when you have several packages with conflicting dependencies, or those that occupy the same namespace (such as pyNN.spiNNaker if you have an older version of the toolchain).

The installation of a virtualenv and the linking to the external libraries is platform-dependent.

* [Ubuntu Virtualenv Installation](#UbuntuVirtualenv)
* [32-bit Fedora Virtualenv Installation](#Fedora32Virtualenv)
* [64-bit Fedora Virtualenv Installation](#Fedora64Virtualenv)
* [Mac OS X Virtualenv Installation](#MacOSXVirtualenv)
* [Windows Virtualenv Installation](#WindowsVirtualenv)

## <a name="UbuntuVirtualenv"></a> Ubuntu Virtualenv Installation
1. Install virtualenv
```sudo pip install virtualenv```
1. Create a virtualenv; ```<name>``` in the following can be replaced by the name of your choice
```virtualenv <name>```
1. Activate the virtualenv
```source <name>/bin/activate```
1. Link numpy to the virtualenv
```ln -s /usr/lib/python2.7/dist-packages/numpy* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. Link scipy to the virtualenv
```ln -s /usr/lib/python2.7/dist-packages/scipy* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. Link lxml to the virtualenv
```ln -s /usr/lib/python2.7/dist-packages/lxml* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. *Optional:* link matplotlib to the virtualenv and install dependencies (only if you chose to install matplotlib)
```pip install python-dateutil```
```pip install pyparsing```
```pip install six```
```ln -s /usr/lib/pymodules/python2.7/matplotlib $VIRTUAL_ENV/lib/python2.7/site-packages/```
```ln -s /usr/lib/pymodules/python2.7/pylab.py $VIRTUAL_ENV/lib/python2.7/site-packages/```

## <a name="Fedora32Virtualenv"></a> 32-bit Fedora Virtualenv Installation
1. Install virtualenv
```sudo pip install virtualenv```
1. Create a virtualenv; ```<name>``` in the following can be replaced by the name of your choice
```virtualenv <name>```
1. Activate the virtualenv
```source <name>/bin/activate```
1. Link numpy to the virtualenv
```ln -s /usr/lib/python2.7/site-packages/numpy* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. Link scipy to the virtualenv
```ln -s /usr/lib/python2.7/site-packages/scipy* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. Link lxml to the virtualenv
```ln -s /usr/lib/python2.7/site-packages/lxml* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. *Optional:* link matplotlib to the virtualenv and install dependencies (only if you chose to install matplotlib)
```pip install python-dateutil```
```pip install pyparsing```
```pip install six```
```ln -s /usr/lib/python2.7/site-packages/matplotlib $VIRTUAL_ENV/lib/python2.7/site-packages/```
```ln -s /usr/lib/python2.7/site-packages/pylab.py $VIRTUAL_ENV/lib/python2.7/site-packages/```

## <a name="Fedora64Virtualenv"></a> 64-bit Fedora Virtualenv Installation
1. Install virtualenv
```sudo pip install virtualenv```
1. Create a virtualenv; ```<name>``` in the following can be replaced by the name of your choice
```virtualenv <name>```
1. Activate the virtualenv
```source <name>/bin/activate```
1. Link numpy to the virtualenv
```ln -s /usr/lib64/python2.7/site-packages/numpy* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. Link scipy to the virtualenv
```ln -s /usr/lib64/python2.7/site-packages/scipy* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. Link lxml to the virtualenv
```ln -s /usr/lib64/python2.7/site-packages/lxml* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. *Optional:* link matplotlib to the virtualenv and install dependencies (only if you chose to install matplotlib)
```pip install python-dateutil```
```pip install pyparsing```
```pip install six```
```ln -s /usr/lib64/python2.7/site-packages/matplotlib $VIRTUAL_ENV/lib/python2.7/site-packages/```
```ln -s /usr/lib64/python2.7/site-packages/pylab.py $VIRTUAL_ENV/lib/python2.7/site-packages/```

## <a name="MacOSXVirtualenv"></a> Mac OS X Virtualenv Installation
1. Install virtualenv
```sudo pip install virtualenv```
1. Create a virtualenv; ```<name>``` in the following can be replaced by the name of your choice
```virtualenv <name>```
1. Activate the virtualenv
```source <name>/bin/activate```
1. Link numpy to the virtualenv
```ln -s /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/numpy* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. Link scipy to the virtualenv
```ln -s /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/scipy* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. Link lxml to the virtualenv
```ln -s /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/lxml* $VIRTUAL_ENV/lib/python2.7/site-packages/```
1. *Optional:* link matplotlib to the virtualenv and install dependencies (only if you chose to install matplotlib)
```pip install python-dateutil```
```pip install pyparsing```
```pip install six```
```ln -s /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/matplotlib $VIRTUAL_ENV/lib/python2.7/site-packages/```
```ln -s /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/pylab.py $VIRTUAL_ENV/lib/python2.7/site-packages/```

## <a name="WindowsVirtualenv"></a> Windows Virtualenv Installation
1. Open a console as administrator and cd to your home directory
```cd %HOMEPATH%```
1. Install virtualenv
```pip install virtualenv```
1. Create a virtualenv; ```<name>``` in the following can be replaced by the name of your choice
```virtualenv <name>```
1. Activate the virtualenv
```<name>\Scripts\activate.bat ```
1. Link numpy to the virtualenv
```mklink /D %VIRTUAL_ENV%\Lib\site-packages\numpy C:\Python27\Lib\site-packages\numpy```
```mklink %VIRTUAL_ENV%\Lib\site-packages\numpy-1.9.1-py2.7.egg-info C:\Python27\site-packages\numpy-1.9.1-py2.7.egg-info```
1. Link scipy to the virtualenv
```mklink /D %VIRTUAL_ENV%\Lib\site-packages\scipy C:\Python27\Lib\site-packages\scipy```
```mklink %VIRTUAL_ENV%\Lib\site-packages\scipy-0.14.1rc1-py2.7.egg-info C:\Python27\site-packages\scipy-0.14.1rc1-py2.7.egg-info```
1. Link lxml to the virtualenv
```mklink /D %VIRTUAL_ENV%\Lib\site-packages\lxml C:\Python27\Lib\site-packages\lxml```
```mklink /D %VIRTUAL_ENV%\Lib\site-packages\lxml-3.4.1-py2.7.egg-info C:\Python27\site-packages\lxml-3.4.1-py2.7.egg-info```
1. *Optional:* link matplotlib to the virtualenv and install dependencies (only if you chose to install matplotlib)
```pip install python-dateutil```
```pip install pyparsing```
```pip install six```
```mklink /D %VIRTUAL_ENV%\Lib\site-packages\matplotlib C:\Python27\Lib\site-packages\matplotlib```
```mklink %VIRTUAL_ENV%\Lib\site-packages\pylab.py C:\Python27\Lib\site-packages\pylab.py```
1. *Optional:* To make matplotlib work within a virtualenv, create the following environment variables:
```TCL_LIBRARY: C:\Python27\tcl\tcl8.5```
```TK_LIBRARY: C:\Python27\tcl\tk8.5```
