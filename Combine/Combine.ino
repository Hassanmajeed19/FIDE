//Incuding libraries for reading the sensors
#include "dht.h"
#include <Wire.h>
#include <Adafruit_BMP085.h>

//Analog Pin DHT22 is connected to
#define dht_apin A0 
//sea level reading to use in bmp 
#define seaLevelPressure_hPa 1013.25 

Adafruit_BMP085 bmp;
dht DHT;

const int ldr_dig = 8;
const int rain_dig = 4;

//for initializing
void setup()
{
  //initializing digital pin
  pinMode(ldr_pin,INPUT);
  pinMode(rain_dig, INPUT);
  
  //there are differnt baudrate for arduino. For this one its 9600
  Serial.begin(9600);
  
  //check if the bmp sensor is working properly
  if (!bmp.begin()) 
  {
    Serial.println("Could not find a valid BMP085 sensor, check wiring!");
    while (1) 
    {
    }
  }
}

//main loop  
void loop()
{
	//Start of Program 
	//printing ldr reading stored in bmp object
	//0 means light 1 means dark
    if (digitalRead(ldr_pin)==0)
    {
      Serial.println(" (Light)");
    }
    else
    {
      Serial.println(" (Dark)");
    }
    
	//reading the DHT22 sensor 
    DHT.read22(dht_apin);
	
	//printing humidity reading stored in dht object
    Serial.print("Current humidity = ");
    Serial.print(DHT.humidity);
    Serial.print("%  ");
    Serial.print("temperature = ");
    Serial.print(DHT.temperature); 
    Serial.println("C  ");
	
	//printing rain detector value
	//low means rain high means no rain
    if(digitalRead(rain_dig) == LOW) 
    {
      Serial.println("Digital value of rain detect : wet"); 
    }
    else
    {
      Serial.println("Digital value of rain detect : dry");
    }
	
	//commented this as pressure sensor also has read temperature option
    /*
    Serial.print("Temperature = ");
    Serial.print(bmp.readTemperature());
    Serial.println(" *C");
    */
	
	//printing pressure reading stored in bmp object
    Serial.print("Pressure = ");
    Serial.print(bmp.readPressure());
    Serial.println(" Pa");
	
	//printing altitude reading stored in bmp object
    Serial.print("Altitude = ");
    Serial.print(bmp.readAltitude());
    Serial.println(" meters");
	
	//printing sea level pressure stored in bmp object
	Serial.print("Pressure at sealevel (calculated) = ");
    Serial.print(bmp.readSealevelPressure());
    Serial.println(" Pa");
	
    Serial.print("Real altitude = ");
    Serial.print(bmp.readAltitude(seaLevelPressure_hPa * 100));
    Serial.println(" meters");
    
    Serial.println();
	//Wait 2 seconds before accessing sensor again.
    delay(2000);
}