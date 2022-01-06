## Steps to deploy:

### Create my-deployment-package.zip
`pip3 install --target ./package  virtualenv discord.py pytz python-dotenv beautifulsoup4 requests`
`cd package/`
`zip -r ../my-deployment-package.zip .`
`cd ..`
`zip -g my-deployment-package.zip dubai_iacad_scraper.py discord_bot.py .env lambda_function.py`

### Deploy zip package
`aws lambda update-function-code --function-name discord_bot --zip-file fileb://my-deployment-package.zip`