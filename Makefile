exe:
	make -C doc/manual qch
	cd esquipulaspy && python py2exe-setup.py py2exe
	cd installer && makensis esquipulas-installer.nsi
	

	