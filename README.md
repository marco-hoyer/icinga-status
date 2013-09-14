icinga-status
=============

This application is simply integrated into apache using mod_wsgi.
It parses icingastats output and returns queried perfdata values.

Example request:
HTTP-GET http://<hostname>:9000/icinga-status?query=STATUSFILEAGETT,NUMHSTUPS

Response:
{NUMHSTUP: '1', STATUSFILEAGETT: '4'}
