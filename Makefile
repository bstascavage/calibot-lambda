TARGET = lambda-calibot

all: build sync deploy

build: 
	rm -f $(TARGET).zip; pip install -r requirements.txt -t .; zip -r $(TARGET).zip *

sync:
	aws s3 sync data/ s3://$(TARGET)/data 

deploy:
	aws lambda update-function-code --function-name lambda-test --zip-file fileb://$(TARGET).zip

clean:
	rm -f $(TARGET).zip; rm -rf twitter*
