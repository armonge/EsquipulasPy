import sip
try:
    sip.getapi('QString')
except ValueError:
    sip.setapi('QString', 2)

import PyQt4.Qt
Qt = PyQt4.Qt
