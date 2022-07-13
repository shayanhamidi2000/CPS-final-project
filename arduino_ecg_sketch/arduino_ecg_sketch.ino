#define OUT_PIN_ECG A0
#define LOD_PLUS 9
#define LOD_MIN 10
#define STATE_IDLE 0
#define STATE_TRANSMIT 1
#define END_SIGN "#"

int last_ecg_value = -1;

void setup() {
  // initialize the serial communication:
  Serial.begin(9600);
  pinMode(LOD_PLUS, INPUT); // Setup for leads off detection LO +
  pinMode(LOD_MIN, INPUT); // Setup for leads off detection LO -
}

void check_bluetooth_data(){
  
}
 
void loop() {
  if((digitalRead(LOD_PLUS) == 1)||(digitalRead(LOD_MIN) == 1))
    last_ecg_value = -1;
  else
    last_ecg_value = analogRead(OUT_PIN_ECG);
  if(last_ecg_value != -1){
    String sensor_data = String(last_ecg_value)+END_SIGN;
    Serial.write(&sensor_data[0]);
  }
}
