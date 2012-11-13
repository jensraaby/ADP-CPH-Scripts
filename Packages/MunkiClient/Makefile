# Installs custom scripts and settings for Munki - it will set the appropriate permissions on the the scripts


include /usr/local/share/luggage/luggage.make


TITLE=Munki_Client
REVERSE_DOMAIN=com.adpcph.it
PAYLOAD=\
		pack-usr-local-munki-preflight \
     	pack-usr-local-munki-postflight \
		pack-usr-local-munki-failure \
        pack-Library-Preferences-ManagedInstalls.plist

PACKAGE_VERSION=1.2.1


l_usr_local_munki: l_usr_local
	@sudo mkdir -p ${WORK_D}/usr/local/munki
	@sudo chown root:wheel ${WORK_D}/usr/local/munki
	@sudo chmod 755 ${WORK_D}/usr/local/munki

pack-usr-local-munki-preflight: l_usr_local_munki
	@sudo ${INSTALL} -m 0755 -o root -g wheel dynamic-client ${WORK_D}/usr/local/munki/dynamic-client
	@sudo ${INSTALL} -m 0755 -o root -g wheel dynamic-config ${WORK_D}/usr/local/munki/dynamic-config
	@sudo ${INSTALL} -m 0755 -o root -g wheel munki_preflight ${WORK_D}/usr/local/munki/preflight

pack-usr-local-munki-postflight: l_usr_local_munki
	@sudo ${INSTALL} -m 0755 -o root -g wheel munki_postflight ${WORK_D}/usr/local/munki/postflight

pack-usr-local-munki-failure: l_usr_local_munki
	@sudo ${INSTALL} -m 0755 -o root -g wheel report_broken_client ${WORK_D}/usr/local/munki/report_broken_client
