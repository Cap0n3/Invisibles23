# === Migration commands === #
.PHONY: help, mkmigs, migrate, mkmigs-dry-run, migrate-all, test-all, test-case

help:
	@echo "Available commands:"
	@echo "  mkmigs \t\tCreate new migrations based on the changes detected in the models."
	@echo "  migrate \t\tApply the migrations to the database."
	@echo "  mkmigs-dry-run \tDisplay the changes that would be made in the database without actually applying them."
	@echo "  migrate-all \t\tCreate and apply migrations for all apps."
	@echo "  test-all \t\tRun all tests."
	@echo "  test-case \t\tRun a specific test case. Example: make test-case case=EventParticipantsModelTest"

mkmigs:
	python manage.py makemigrations

migrate:
	python manage.py migrate

mkmigs-dry-run:
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
# Example: make test-case case=EventParticipantsModelTest
test-case:
	python manage.py test website.tests.$(case) -v 2
