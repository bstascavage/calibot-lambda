TARGET = calibot

all: build sync deploy

build: 
	cd $(TARGET); rm -f $(TARGET).zip; pip install -r requirements.txt -t .; zip -r $(TARGET).zip *

sync:
	cd $(TARGET); aws s3 sync data/ s3://lambda-$(TARGET)/data 

deploy:
	cd $(TARGET); aws lambda update-function-code --function-name lambda-test --zip-file fileb://$(TARGET).zip

clean:
	cd $(TARGET); rm -f $(TARGET).zip; rm -rf twitter*
