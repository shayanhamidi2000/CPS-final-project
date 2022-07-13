#include "BluetoothSerial.h"
#include "esp_bt_main.h"
#include "esp_bt_device.h"
#define STATE_IDLE 0
#define STATE_TRANSMIT 1
#define STATE_CONNECTED 2
#define END_SIGN "#"

BluetoothSerial SerialBT;
String sensor_buffer = "";
String master_buffer = "";
int state = STATE_IDLE;
    
void setup()
{
  SerialBT.begin("ECG");
  delay(1000);
  Serial.begin(9600);
  Serial.setTimeout(0);
  SerialBT.setTimeout(0);
}

String get_last_whole_data_from_master_buffer(){
  int delimeter_index = master_buffer.indexOf(END_SIGN);
  String last_whole_data = master_buffer.substring(0, delimeter_index);
  if(delimeter_index == (master_buffer.length() - 1))
    master_buffer = "";
  else
    master_buffer = master_buffer.substring(delimeter_index + 1);
  return last_whole_data;
}

void process_sensor_data(){
  SerialBT.print(sensor_buffer);
  sensor_buffer = "";
}

String get_device_address_message(){
  String message_address;
  const uint8_t* point = esp_bt_dev_get_address();
  for (int i = 0; i < 6; i++){
    char str[3];
    sprintf(str, "%02X", (int)point[i]);
    message_address += String(str);
    if (i < 5)
      message_address += ":";
  }
  return message_address;
}

void process_master_data(){
  String master_data = get_last_whole_data_from_master_buffer();
  if(master_data == "start"){
    SerialBT.print(get_device_address_message());
    state = STATE_CONNECTED;
  }  
}

void check_sensor_data(){
  String data = Serial.readString();
  if (data != ""){
    sensor_buffer += data;
    if(sensor_buffer.indexOf(END_SIGN) != -1)
      process_sensor_data();
  }
}

void check_master_data(){
  String data = SerialBT.readString();
  if (data != ""){
    master_buffer += data;
    if(master_buffer.indexOf(END_SIGN) != -1)
      process_master_data();
  }
}
  
void loop()
{
  if (SerialBT.available())
    check_master_data();
  if(Serial.available() && state != STATE_IDLE)
    check_sensor_data();
    
}
