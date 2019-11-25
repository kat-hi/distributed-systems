compile:
	@echo " >>> knock knock!"
	@sleep 1s
	@echo " >>> who is there?"
	@sleep 3s
	@echo " << ... >>"
	@sleep 3s
	@echo " << ... >>"
	@sleep 6s
	@echo "java!"	
	@sleep 3s
	@echo "----"
	@echo "note: this datatransfer works for txt. with png/jpeg/pdf there are still issues and unfortunatly it is too late for solving these problems tonight. see comments."
run_receiver:
	@python3 DslpFileReceiver.py $(user)

run_sender:
	@python3 DslpFileSender.py $(user) $(receiver) $(filename)
