.PHONY: help
help: ## Display help message
	@grep -E '^[0-9a-zA-Z_-]+\.*[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

########################################################
# Campus 1
########################################################



.PHONY: build
build: ## Build Configs
	ansible-playbook playbooks/build_fabric.yml -i inventory.yml

.PHONY: deploy
deploy: ## Deploy Configs via CloudVision
	ansible-playbook playbooks/deploy_cv.yml -i inventory.yml

.PHONY: validate
validate: ## Validate network state
	ansible-playbook playbooks/validate_fabric.yml -i inventory.yml

########################################################
# ANTA TRAFFIC PROTOCOL TESTING PIPELINE
########################################################

# --- LAB CONFIGURATION VARIABLES ---
ANTA_INVENTORY := testing/anta_hosts.yml
ANTA_CATALOG   := testing/catalog.yml
ANTA_REPORT_DIR:= testing/reports
ANTA_USER      := arista
ANTA_PASSWORD  := Arista123!

# --- CAMPUS SELECTION ---
# Usage: make test campus1 | make test campus2 | make test campus3 | make test all
# Each host in testing/anta_hosts.yml is tagged campus1/campus2/campus3, so
# passing a campus name restricts the run to that campus via `anta --tags`.
CAMPUSES  := campus1 campus2 campus3
CAMPUS_ARG:= $(filter $(CAMPUSES),$(MAKECMDGOALS))
ifneq ($(CAMPUS_ARG),)
ANTA_TAGS := --tags $(CAMPUS_ARG)
else
ANTA_TAGS :=
endif

# Swallow campus/all as plain arguments instead of make targets to build.
.PHONY: $(CAMPUSES) all
$(CAMPUSES) all:
	@:

# ANTA's table view sizes its Message(s)/Description columns to the detected
# terminal width, which falls back to a cramped 80 columns whenever stdout
# isn't a real tty (eg. running under make, piped, or redirected to a file) -
# squeezing failure reasons into unreadable wrapped fragments. Forcing a wide
# COLUMNS below keeps the full failure reason intact and readable.
.PHONY: test
test: ## Run ANTA NRFU tests (Terminal Grid Table view). Add campus1|campus2|campus3|all to scope the run
	@echo "Running parallel traffic verification matrix..."
	COLUMNS=250 PYTHONPATH=$(PWD) anta nrfu --inventory $(ANTA_INVENTORY) --catalog $(ANTA_CATALOG) --username $(ANTA_USER) --password $(ANTA_PASSWORD) --insecure $(ANTA_TAGS) table


.PHONY: text
text: ## Run ANTA NRFU tests (Raw Text Stream view). Add campus1|campus2|campus3|all to scope the run
	@echo "Streaming raw text testing matrix..."
	anta nrfu --inventory $(ANTA_INVENTORY) --catalog $(ANTA_CATALOG) --username $(ANTA_USER) --password $(ANTA_PASSWORD) --insecure $(ANTA_TAGS) text

.PHONY: report
report: ## Run ANTA NRFU tests and generate permanent Markdown logs. Add campus1|campus2|campus3|all to scope the run
	@echo "Generating permanent Markdown test records..."
	@mkdir -p $(ANTA_REPORT_DIR)
	PYTHONPATH=$(PWD) anta nrfu --inventory $(ANTA_INVENTORY) --catalog $(ANTA_CATALOG) --username $(ANTA_USER) --password $(ANTA_PASSWORD) --insecure $(ANTA_TAGS) md-report --md-output $(ANTA_REPORT_DIR)/anta_report.md
	@echo "Report saved successfully to $(ANTA_REPORT_DIR)/anta_report.md"

.PHONY: test-summary
test-summary: ## Run ANTA NRFU tests and print a department-to-department connectivity summary. Add campus1|campus2|campus3|all to scope the run
	@echo "Running parallel traffic verification matrix..."
	@mkdir -p $(ANTA_REPORT_DIR)
	@PYTHONPATH=$(PWD) anta nrfu --inventory $(ANTA_INVENTORY) --catalog $(ANTA_CATALOG) --username $(ANTA_USER) --password $(ANTA_PASSWORD) --insecure $(ANTA_TAGS) json -o $(ANTA_REPORT_DIR)/nrfu_results.json
	@python3 scripts/connectivity_summary.py $(ANTA_REPORT_DIR)/nrfu_results.json



.PHONY: l4-test
l4-test: ## Run active Layer 4 script-driven socket checks (TCP/UDP/Telnet)
	@echo "=========================================================="
	@echo " Testing Active L4 Transport Paths across Lab Infrastructure"
	@echo "=========================================================="
	@echo "1. Checking Secure SSH Delivery (TCP Port 22)..."
	anta debug run-cmd --inventory $(ANTA_INVENTORY) --username $(ANTA_USER) --password $(ANTA_PASSWORD) --insecure \
		--command "bash timeout 2 bash -c 'cat < /dev/tcp/172.16.21.10/22'"
	@echo "2. Checking Application Traffic Sockets (UDP Port 53)..."
	anta debug run-cmd --inventory $(ANTA_INVENTORY) --username $(ANTA_USER) --password $(ANTA_PASSWORD) --insecure \
		--command "bash nc -zuv -w 2 172.16.31.10 53"
	@echo "3. Testing Cross-Department Telnet Traffic (TCP Port 23)..."
	anta debug run-cmd --inventory $(ANTA_INVENTORY) --username $(ANTA_USER) --password $(ANTA_PASSWORD) --insecure \
		--command "bash nc -zv -w 2 172.16.41.10 23"

.PHONY: clean-reports
clean-reports: ## Remove generated ANTA test reports from the workspace
	@echo "Cleaning up report artifacts..."
	rm -rf $(ANTA_REPORT_DIR)/*

########################################################
# Hosts - Lab Prep
########################################################

.PHONY: preplab
preplab: ## Deploy Configs via eAPI
	ansible-playbook playbooks/preplab.yml -i host_configs/inventory.yml -e "target_hosts=LAB"

