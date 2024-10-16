# === Migration commands === #
.PHONY: help, run, mkmigs, migrate, mkmigs-dry, migrate-all, test-all, test-case, proxy-test-case

help:
	@echo "Available commands:"
	@echo "  mkmigs \t\tCreate new migrations based on the changes detected in the models."
	@echo "  mkmigs-dry \t\tDisplay the changes that would be made in the database without actually applying them."
	@echo "  migrate \t\tApply the migrations to the database."
	@echo "  migrate-all \t\tCreate and apply migrations for all apps."
	@echo "  test-all \t\tRun all tests."
	@echo "  website-test-case \tRun a specific test case. Example: make website-test-case case=EventParticipantsModelTest"
	@echo "  proxy-test-case \tRun a specific test case for the proxy app. Example: make proxy-test-case case=ProxyModelTest"
run:
	python manage.py runserver

mkmigs:
	python manage.py makemigrations

migrate:
	python manage.py migrate

mkmigs-dry:
	python manage.py makemigrations --dry-run

migrate-all:
	@echo "Migrating all apps..."
	python manage.py makemigrations
	python manage.py migrate

# === Test commands === #
test-all:
	@echo "Running all tests..."
	python manage.py test -v 2

# Launch a specific test case by passing the test case name as an argument
# Example: make website-test-case case=EventParticipantsModelTest
website-test-case:
	python manage.py test website.tests.$(case) -v 2

proxy-test-case:
	python manage.py test proxy.tests.$(case) -v 2
