start:
	uv run flask --app example --debug run --port 8000

start_bd:
	systemctl start postgresql

stop_bd:
	systemctl stop postgresql

build:
	./build.sh