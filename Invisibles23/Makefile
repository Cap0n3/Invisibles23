# === Migration commands === #
.PHONY: makemigrations
makemigrations:
	python manage.py makemigrations

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: makemigrations-dry-run
makemigrations-dry-run:
	python manage.py makemigrations --dry-run

.PHONY: migrate-all
migrate-all:
	@echo "Migrating all apps..."
	python manage.py makemigrations
	python manage.py migrate

# === Test commands === #
.PHONY: test-all
test-all:
	@echo "Running all tests..."
	python manage.py test -v 2

# Launch a specific test case by passing the test case name as an argument
# Example: make test-case case=EventParticipantsModelTest
.PHONY: test-case
test-case:
	python manage.py test website.tests.$(case) -v 2


