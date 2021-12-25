#include "dht.h"
#define dht_apin A0 // Analog Pin sensor is connected to
#include <Wire.h>
#include <Adafruit_BMP085.h>
#define seaLevelPressure_hPa 1013.25

//including libraries for our sensors
Adafruit_BMP085 bmp;
dht DHT;
//defining arduino pins on which our input would be received
const int ldr_pin = 8;
const int capteur_D = 4;

void setup(){
  //binding pins to either output or input
  pinMode(ldr_pin,INPUT);
  pinMode(capteur_D, INPUT);
  Serial.begin(9600);
  
  //dont start if the sensor isnt connected properly
  if (!bmp.begin()) 
  {
    Serial.println("Could not find a valid BMP085 sensor, check wiring!");
    while (1) 
    {
    }
  }
  
}//end "setup()"
 
void loop(){
  //Start of Program 
    //read input 
    DHT.read22(dht_apin);
    
    
    Serial.print("Current humidity=");
    Serial.print(DHT.humidity);
   
    Serial.print(", temperature=");
    Serial.print(DHT.temperature); 
    
    
    Serial.print(", pressure=");
    Serial.print(bmp.readPressure());
    Serial.println();
    
    delay(3000);//Wait 5 seconds before accessing sensor again.
 
  //Fastest should be once every two seconds.
 
}// end loop() 
