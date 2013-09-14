icinga-status
=============

This application is simply integrated into apache using mod_wsgi.</br>
It parses icingastats output and returns queried perfdata values.</br>
URL for futher information about using icingastats: http://docs.icinga.org/latest/de/icingastats.html</br>

Example request:</br>
HTTP-GET http://hostname:9000/icinga-status?query=STATUSFILEAGETT,NUMHSTUPS

Response:</br>
{NUMHSTUP: '1', STATUSFILEAGETT: '4'}
