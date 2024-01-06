/*  IntelliTransit

    * This code handles the display and the alogorithm for the scheduling using the Arduino Uno
    * Pin connections
      * D0(RX) -> TX pin of the nodemcu
      * D1(TX) -> RX pin of the nodemcu
      * D2 -> RS pin of the lcd
      * D3 -> E pin of the lcd
      * D4 -> D4
      * D5 -> D5
      * D6 -> D6
      * D7 -> D7
*/

#define MIN_THRESHOLD  1
#define MAX_THRESHOLD  4

#define MIN_SPEED  10
#define MAX_SPEED  100
#define BASE_SPEED 30

#define CURRENT_PASSANGER_WEIGHT  0.1
#define LEAD_PASSANGER_WEIGHT  0.2

#define SPEED_GAP  9

#define FREQUENCY 5



# include <LiquidCrystal.h>

LiquidCrystal lcd(2,3,4,5,6,7);


int lead_passengers;
int current_passengers;

void setup() {

  lcd.begin(16,2);
  Serial.begin(115200);

  display_initialize();
}

void loop() {

 
  wait_for_serial();
  read_serial();
  display_speed();

  delay(FREQUENCY*1000);

}

// Initial Display
void display_initialize(){
  lcd.setCursor(2,0);
  lcd.print("Initializing");
  lcd.setCursor(1,1);
  lcd.print("IntelliTransit");
  delay(2000);
}

// Wait till the serial connection is established.
void wait_for_serial(){
  
  int count = 0;

  while(Serial.available() == 0){
    if (count == 10){
      lcd.clear();
      lcd.print("Connection Fault");
      lcd.setCursor(2,1);
      lcd.print("Retrying... ");
    }
    
    lcd.noDisplay();
    delay(500);
    lcd.display();
    delay(500);
    count = count + 1;
  }

  lcd.clear();
}


// Read the data from the serial connection
void read_serial(){
  
  int val;
  bool first = true;
  bool second = false;
  
  while(Serial.available()>0){
    val = Serial.parseInt();

    if(val == 200){
      first = false;
    }

    else if(val == 400){
      break;
    }

    else{
      if(first == true && second == false){
        lead_passengers = val;
        second = true;
      }
      else if(second == true && first == false){
        current_passengers = val;
      }
    }
  }
}


// Displays the minimim and maximum speeds in theled display
void display_speed(){
  lcd.print("MAX SPEED:");
  lcd.setCursor(11, 0);
  lcd.print(max_speed(new_speed(lead_passengers,current_passengers)));

  lcd.setCursor(0, 1);
  lcd.print("MIN SPEED:");
  lcd.setCursor(11, 1);
  lcd.print(min_speed(new_speed(lead_passengers,current_passengers)));
}



// Algorithm to calculate the new speed
float new_speed(int lead_passangers , int current_passengers){
  
  float new_speed = BASE_SPEED;


  if(lead_passengers > MAX_THRESHOLD){
    if(new_speed + LEAD_PASSANGER_WEIGHT * lead_passangers < MAX_SPEED ){
      new_speed = new_speed + LEAD_PASSANGER_WEIGHT * lead_passangers;
    }
    if(current_passengers > MAX_THRESHOLD){
      if(new_speed + LEAD_PASSANGER_WEIGHT * current_passengers < MAX_SPEED ){
        new_speed = new_speed + LEAD_PASSANGER_WEIGHT * current_passengers;
      }
    }
  }

  if(lead_passengers < MIN_THRESHOLD){
    if(new_speed - LEAD_PASSANGER_WEIGHT * (MIN_THRESHOLD - lead_passangers) > MIN_SPEED ){
      new_speed = new_speed - LEAD_PASSANGER_WEIGHT * (MIN_THRESHOLD - lead_passangers);
    }
  }

  if(current_passengers > MAX_THRESHOLD){
      if(new_speed + LEAD_PASSANGER_WEIGHT * (MIN_THRESHOLD - current_passengers) > MIN_SPEED ){
        new_speed = new_speed - LEAD_PASSANGER_WEIGHT * (MIN_THRESHOLD - current_passengers);
      }
    }

  return new_speed;
}



// Calculate the maximum speed 
float max_speed(float new_speed){
  if(new_speed + SPEED_GAP/2 < MAX_SPEED){
    return new_speed + SPEED_GAP/2;
  }
  else{
    return MAX_SPEED;
  }
}

// Calculate the minimim speed
float min_speed(float new_speed){
  if(new_speed - SPEED_GAP/2 > MIN_SPEED){
    return new_speed - SPEED_GAP/2;
  }
  else{
    return MIN_SPEED;
  }
}


