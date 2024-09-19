run_images_folder:
	@echo "Running images folder"
	poetry run python easy_bookmarks/integrations/pic2bookmark/image_extraction.py --input demo_images
start_telegram_bot:
	@echo "Starting telegram bot"
	poetry run python easy_bookmarks/integrations/pic2bookmark/telegram_bot.py

run:
	@echo "Running CLI"
	poetry run python -m easy_bookmarks.cli run --config config/integration_config.yaml
