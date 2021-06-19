#include <WiFi.h>
#define ARR_SIZE(arr) ( sizeof((arr)) / sizeof((arr[0])) )

// WIFI/////////////////////////////
const char* ssid = "XXXX";
const char* password =  "XX";
const uint16_t port = 123456;
const char * host = "1XXX";

// TOUCH////////////////////////////



const int A_PIN = 14;
const int B_PIN = 27;
const int C_PIN = 4;
const int D_PIN = 12;
const int E_PIN = 32;
const int F_PIN = 33;
const int G_PIN = 2;
const int H_PIN = 15;


int a_value = 0;
int b_value = 0;
int c_value = 0;
int d_value = 0;
int e_value = 0;
int f_value = 0;
int g_value = 0;
int h_value = 0;

int a = 0;
int b = 0;
int c = 0;
int d = 0;
int e = 0;
int f = 0;
int g = 0;
int h = 0;

int ghost_a = 0;
int ghost_b = 0;
int ghost_c = 0;
int ghost_d = 0;
int ghost_e = 0;
int ghost_f = 0;
int ghost_g = 0;
int ghost_h = 0;


// LEDS //////////////////////////////////
const int DEBUG_LED_RED_PIN = 5;
const int DEBUG_LED_YELLOW_PIN = 26;
const int DEBUG_LED_GREEN_PIN = 18;
const int DEBUG_LED_BLUE_PIN = 25;
const int WHITE_LED_PIN = 16;

// control vars
int loopcounter = 0;


WiFiClient client;


String client_name = "Nimas_kleiner_helfer";



// runned once
void setup()
{

  // declare output as output
  pinMode (DEBUG_LED_RED_PIN, OUTPUT);
  pinMode (DEBUG_LED_YELLOW_PIN, OUTPUT);
  pinMode (DEBUG_LED_GREEN_PIN, OUTPUT);
  pinMode (DEBUG_LED_BLUE_PIN, OUTPUT);
  pinMode (WHITE_LED_PIN, OUTPUT);

  // declare button pins as INPUT
  pinMode(A_PIN, INPUT);
  pinMode(B_PIN, INPUT);
  pinMode(C_PIN, INPUT);
  pinMode(D_PIN, INPUT);
  pinMode(E_PIN, INPUT);
  pinMode(F_PIN, INPUT);
  pinMode(G_PIN, INPUT);
  pinMode(H_PIN, INPUT);



  // turn red led on because system ist running
  digitalWrite (DEBUG_LED_RED_PIN, HIGH);  

  // enable USB debug
  Serial.begin(115200);

 // Try to gain wifi acces
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    
    // YELLOW blinks until we accesed wifi
    digitalWrite (DEBUG_LED_YELLOW_PIN, HIGH);  
    delay(250);
    digitalWrite (DEBUG_LED_YELLOW_PIN, LOW);  
    delay(250);
    digitalWrite (DEBUG_LED_YELLOW_PIN, HIGH);  

    // USB debug output
    Serial.println("trying to connect to wifi");
  }

  // connection to wifi succelfull
  action_wifi_connection_succesful();
   
}


// repeats forever
void loop()
{
    loopcounter +=1;

   update_touch();

   if(a_value == 0 && b_value == 0 && c_value == 0 && d_value == 0 && e_value == 0 && f_value == 0 && g_value == 0 && h_value == 0){
        digitalWrite (DEBUG_LED_RED_PIN, HIGH);
   } else {
        digitalWrite (DEBUG_LED_RED_PIN, LOW);

   }

    
    // trys to connect to server socket
    // if already connected just skip
    if (!client.connected()){
      if (!client.connect(host, port)) {
          action_initial_connection_failure();
          return;
      } else {
          action_initial_connection_succesful();
      }
    }


    // process_input(client);

    if (something_changed()){
      client.print("A:" + String(a_value) + "B:" + String(b_value) + "C:" + String(c_value) + "D:" + String(d_value) + "E:" + String(e_value) + "F:" + String(f_value) + "G:" + String(g_value) + "H:" + String(h_value) + "-");
      process_input(client);
    } else {
      if ((loopcounter % 100) == 0){
        client.print("im fine");
        process_input(client);

      }
      
    }

    
    

    // Serial.println("Disconnecting...");
    // client.stop();
 
    delay(10);
}


bool something_changed(){
  bool changed = false;

  if (ghost_a != a_value){
    changed = true;
    ghost_a = a_value;
  }
  
  if (ghost_b != b_value){
    changed = true;
    ghost_b = b_value;
  }
  if (ghost_c != c_value){
    changed = true;
    ghost_c = c_value;
  }
  if (ghost_d != d_value){
    changed = true;
    ghost_d = d_value;
  }
  if (ghost_e != e_value){
    changed = true;
    ghost_e = e_value;
  }
  if (ghost_f != f_value){
    changed = true;
    ghost_f = f_value;
  }  
  if (ghost_g != g_value){
    changed = true;
    ghost_g = g_value;
  }  
  if (ghost_h != h_value){
    changed = true;
    ghost_h = h_value;
  }
  return changed;
}

void update_touch(){
  a_value = digitalRead(A_PIN);
  b_value = digitalRead(B_PIN);
  c_value = digitalRead(C_PIN);
  d_value = digitalRead(D_PIN);
  e_value = digitalRead(E_PIN);
  f_value = digitalRead(F_PIN);
  g_value = digitalRead(G_PIN);
  h_value = digitalRead(H_PIN);
}



void action_wifi_connection_succesful(){
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
  digitalWrite (DEBUG_LED_YELLOW_PIN, HIGH);  

}


void action_initial_connection_failure(){
  Serial.println("Connection to host failed");
  digitalWrite (DEBUG_LED_GREEN_PIN, LOW);  

  delay(1000);

  
}
void action_initial_connection_succesful(){
  Serial.println("Connected to server successful!"); 
  // sending my name
  client.print("name:" + client_name + "-");
  digitalWrite (DEBUG_LED_GREEN_PIN, HIGH);  
  process_input(client);
}


void message_handler(String message){
  
  Serial.println(message);

  if(strstr(message.c_str(), "LEDON") != NULL) {
    digitalWrite (WHITE_LED_PIN, HIGH);  
  }
  if(strstr(message.c_str(), "LEDOFF") != NULL) {
    digitalWrite (WHITE_LED_PIN, LOW);  
  }

}

void process_input(WiFiClient client){
  String message = "";
  digitalWrite (DEBUG_LED_BLUE_PIN, HIGH);  

  while(true){
    if (client.available()) {    
      message += char(client.read());
          
    } else{      
      // no data available or all is already processed
      digitalWrite (DEBUG_LED_BLUE_PIN, LOW);  
      break;    
    }
  }
  if (ARR_SIZE(message) > 0) {
    // THIS IS THE MESSAGE RECIEVED FROM THE SERVER AS A STRING
    message_handler(message);
    
  }
}
