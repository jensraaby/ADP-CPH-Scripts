include /usr/local/share/luggage/luggage.make


TITLE=Munki_Client_Dyn
REVERSE_DOMAIN=com.adpcph.it
PAYLOAD=\
		pack-usr-local-munki-preflight \
     	pack-usr-local-munki-postflight \
        pack-Library-Preferences-ManagedInstalls.plist

PACKAGE_VERSION=1.0.3


l_usr_local_munki: l_usr_local
	@sudo mkdir -p ${WORK_D}/usr/local/munki
	@sudo chown root:wheel ${WORK_D}/usr/local/munki
	@sudo chmod 755 ${WORK_D}/usr/local/munki

pack-usr-local-munki-preflight: l_usr_local_munki
	@sudo ${INSTALL} -m 0755 -o root -g wheel DynamicPreflight ${WORK_D}/usr/local/munki/DynamicPreflight
	@sudo ${INSTALL} -m 0755 -o root -g wheel munki_preflight ${WORK_D}/usr/local/munki/preflight

pack-usr-local-munki-postflight: l_usr_local_munki
	@sudo ${INSTALL} -m 0755 -o root -g wheel munki_postflight ${WORK_D}/usr/local/munki/postflight
