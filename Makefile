TARGET = lambda-calibot

all: zip

zip: 
	rm -f $(TARGET).zip; zip -r $(TARGET).zip *

clean:
	rm -f $(TARGET).zip
