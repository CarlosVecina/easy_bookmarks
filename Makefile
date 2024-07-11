run_images_folder:
	@echo "Running images folder"
	poetry run python image_extraction.py --input images
start_telegram_bot:
	@echo "Starting telegram bot"
	poetry run python pic2bookmark/telegram_bot.py