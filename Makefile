.PHONY: cloud-cli

cloud-cli:
	@echo "Building cloud-cli"
	poetry run pyinstaller --onefile clouds/cli/cli.py
	sudo mv dist/cli /usr/local/bin/cloud-cli
	rmdir dist
