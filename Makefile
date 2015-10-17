package: clean
	@echo "Packaging... "
	@gsed -i 's/TestingConfig/ReleaseConfig/g' eSearch/entry.py
	tar -cf release.tar --exclude=tags --exclude=ENV *
	@gsed -i 's/ReleaseConfig/TestingConfig/g' eSearch/entry.py
	@echo "Package Success!"

.PHONY : clean
clean:
	@echo "Cleaning Workspace ... "
	@find ./eSearch/ |grep '\.pyc' |xargs rm -f
	@find ./config/ |grep '\.pyc' |xargs rm -f
	@rm -f ./log/* 
	@rm -f ./release.tar
	@echo "Done."


.PHONY : dockerize
dockerize : package
	docker build -t search_web_app .
