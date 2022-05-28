#include <Servo.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,16,2); 

Servo myservo;
int spin=D8;
int irpin=D7;
int oldvalue;
int newvalue;
int state1;
int count=0;

void setup() {
  // put your setup code here, to run once:
lcd.init();                      // initialize the lcd 
lcd.init();
  // Print a message to the LCD.
lcd.backlight();
Serial.begin(9600);
myservo.attach(spin);
pinMode(irpin,INPUT);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Total");
  lcd.setCursor(0,1);
  lcd.print("Parking slots:8");
}

void loop() {
  // put your main code here, to run repeatedly:
newvalue=digitalRead(irpin);
//Serial.println("newvalue");
//Serial.println(newvalue);
if(Serial.available()>0){
  state1=Serial.parseInt();
}
if(state1<9 && state1>0){
  
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Available");
      lcd.setCursor(0,1);
      lcd.print("Parking slots:");
      lcd.setCursor(15,1);
      lcd.print(state1);
}
//if(state1==70)
//{
//    if(count==7){
//      lcd.clear();
//      lcd.setCursor(0,0);
//      lcd.print("No slots");
//      lcd.setCursor(0,1);
//      lcd.print("available");
//  }
//  else{
//      count++;
//      lcd.clear();
//      lcd.setCursor(0,0);
//      lcd.print("Available");
//      lcd.setCursor(0,1);
//      lcd.print("Parking slots:");
//      lcd.setCursor(15,1);
//      lcd.print(8-count);
//  }

  
//}
//if(state1==80)
//{
//  if(count==0){
//    lcd.clear();
//    lcd.setCursor(0,0);
//    lcd.print("All slots");
//    lcd.setCursor(0,1);
//    lcd.print("available");
//  }
//  else{
//      count--;
//      lcd.clear();
//      lcd.setCursor(0,0);
//      lcd.print("Available");
//      lcd.setCursor(0,1);
//      lcd.print("Parking slots:");
//      lcd.setCursor(15,1);
//      lcd.print(8-count);
//  }
  

//}
Serial.println("count");
Serial.println(count);
if(oldvalue==0 && newvalue==1)
{
//  count++;
//  lcd.clear();
//  lcd.setCursor(0,0);
//  lcd.print("Available");
//  lcd.setCursor(0,1);
//  lcd.print("Parking slots:");
//  lcd.setCursor(15,1);
//  lcd.print(8-count);
  myservo.write(110);
  Serial.println("Servo closed");
  
}
if(state1==50)
{
  myservo.write(0);
  Serial.println("Servo opened");
}
Serial.println("state");
Serial.println(state1);
oldvalue=newvalue;
delay(1000);
//Serial.println("oldvalue");
//Serial.println(oldvalue);


}
