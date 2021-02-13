#include <WiFi.h>
#define ARR_SIZE(arr) ( sizeof((arr)) / sizeof((arr[0])) )

// WIFI/////////////////////////////
const char* ssid = "XXXX";
const char* password =  "XX";
const uint16_t port = 123456;
const char * host = "1XXX";

// TOUCH////////////////////////////
int button_a_threshold = 0;
int button_b_threshold = 0;
int button_c_threshold = 0;
int button_d_threshold = 0;
int button_e_threshold = 0;
int button_f_threshold = 0;
int button_g_threshold = 0;
int button_h_threshold = 0;

int a_stack[3] = {0, 0, 0}; 
int b_stack[3] = {0, 0, 0};  
int c_stack[3] = {0, 0, 0};  
int d_stack[3] = {0, 0, 0};  
int e_stack[3] = {0, 0, 0}; 
int f_stack[3] = {0, 0, 0};  
int g_stack[3] = {0, 0, 0};  
int h_stack[3] = {0, 0, 0};  

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


String client_name = "FUri";



// runned once
void setup()
{

  // declare output as output
  pinMode (DEBUG_LED_RED_PIN, OUTPUT);
  pinMode (DEBUG_LED_YELLOW_PIN, OUTPUT);
  pinMode (DEBUG_LED_GREEN_PIN, OUTPUT);
  pinMode (DEBUG_LED_BLUE_PIN, OUTPUT);
  pinMode (WHITE_LED_PIN, OUTPUT);

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

   if(a == 0 && b == 0 && c == 0 && d == 0 && e == 0 && f == 0 && g == 0 && h == 0){
        digitalWrite (DEBUG_LED_RED_PIN, HIGH);
   } else {
        digitalWrite (DEBUG_LED_RED_PIN, LOW);

   }

   // in the first 10 seconds the inputs are calibrated
   // then never again
   if(loopcounter < 11){
  
        calibrating();
        
        delay(1000);
        return; 
    }
    // update values
    if (loopcounter == 11){
        calibrating_again();
        return;
    }


    check_input();

    
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
      client.print("A:" + String(a) + "B:" + String(b) + "C:" + String(c) + "D:" + String(d) + "E:" + String(e) + "F:" + String(f) + "G:" + String(g) + "H:" + String(h) + "-");
      process_input(client);
    } else {
      if ((loopcounter % 100) == 0){
        client.print("im fine");
        process_input(client);
        Serial.println(ghost_a);
        Serial.println(ghost_b);

      }
      
    }

    
    

    // Serial.println("Disconnecting...");
    // client.stop();
 
    delay(10);
}


bool something_changed(){
  bool changed = false;

  if (ghost_a != a){
    changed = true;
    ghost_a = a;
  }
  
  if (ghost_b != b){
    changed = true;
    ghost_b = b;
  }
  if (ghost_c != c){
    changed = true;
    ghost_c = c;
  }
  if (ghost_d != d){
    changed = true;
    ghost_d = d;
  }
  if (ghost_e != e){
    changed = true;
    ghost_e = e;
  }
  if (ghost_f != f){
    changed = true;
    ghost_f = f;
  }  
  if (ghost_g != g){
    changed = true;
    ghost_g = g;
  }  
  if (ghost_h != h){
    changed = true;
    ghost_h = h;
  }
  return changed;
}

void update_touch(){
  a_stack[2] = a_stack[1];
  a_stack[1] = a_stack[0];
  a_stack[0] = touchRead(A_PIN);

  b_stack[2] = b_stack[1];
  b_stack[1] = b_stack[0];
  b_stack[0] = touchRead(B_PIN);

  c_stack[2] = c_stack[1];
  c_stack[1] = c_stack[0];
  c_stack[0] = touchRead(C_PIN);

  
  d_stack[2] = d_stack[1];
  d_stack[1] = d_stack[0];
  d_stack[0] = touchRead(D_PIN);

  e_stack[2] = e_stack[1];
  e_stack[1] = e_stack[0];
  e_stack[0] = touchRead(E_PIN);

  f_stack[2] = f_stack[1];
  f_stack[1] = f_stack[0];
  f_stack[0] = touchRead(F_PIN);

  g_stack[2] = g_stack[1];
  g_stack[1] = g_stack[0];
  g_stack[0] = touchRead(G_PIN);

  h_stack[2] = h_stack[1];
  h_stack[1] = h_stack[0];
  h_stack[0] = touchRead(H_PIN);

  a_value = max(max(a_stack[0], a_stack[1]), a_stack[2]);
  b_value = max(max(b_stack[0], b_stack[1]), b_stack[2]);
  c_value = max(max(c_stack[0], c_stack[1]), c_stack[2]);
  d_value = max(max(d_stack[0], d_stack[1]), d_stack[2]);

  e_value = max(max(e_stack[0], e_stack[1]), e_stack[2]);
  f_value = max(max(f_stack[0], f_stack[1]), f_stack[2]);
  g_value = max(max(g_stack[0], g_stack[1]), g_stack[2]);
  h_value = max(max(h_stack[0], h_stack[1]), h_stack[2]);
}

void calibrating(){
  Serial.println("Capacitiy value calibrating.....");
  button_a_threshold += a_value;
  button_b_threshold += b_value;
  button_c_threshold += c_value;
  button_d_threshold += d_value;
  button_e_threshold += a_value;
  button_f_threshold += f_value;
  button_g_threshold += g_value;
  button_h_threshold += h_value;
  
  Serial.println(button_a_threshold);
  Serial.println(button_b_threshold);
  Serial.println(button_c_threshold);
  Serial.println(button_d_threshold);
  Serial.println(button_e_threshold);
  Serial.println(button_f_threshold);
  Serial.println(button_g_threshold);
  Serial.println(button_h_threshold);
}

void calibrating_again(){
  button_a_threshold = (int)((button_a_threshold / 5) / 4);
  button_b_threshold = (int)((button_b_threshold / 5) / 4);
  button_c_threshold = (int)((button_c_threshold / 5) / 4);
  button_d_threshold = (int)((button_d_threshold / 5) / 4);
  button_e_threshold = (int)((button_e_threshold / 5) / 4);
  button_f_threshold = (int)((button_f_threshold / 5) / 4);
  button_g_threshold = (int)((button_g_threshold / 5) / 4);
  button_h_threshold = (int)((button_h_threshold / 5) / 4);

  Serial.println("Capacitiy value threshold set to:");
  Serial.println(button_a_threshold);
  Serial.println(button_b_threshold);
  Serial.println(button_c_threshold);
  Serial.println(button_d_threshold);
  Serial.println(button_e_threshold);
  Serial.println(button_f_threshold);
  Serial.println(button_g_threshold);
  Serial.println(button_h_threshold);

  Serial.println("wait a second...");

  delay(1000);
}

void check_input(){
    if((a_value < button_a_threshold) && (a_value != 0)){
      // code for touch a
      Serial.print("Button A pressed with capacity value: ");
      Serial.print(a_value);
      Serial.println();
      a = 1;
    } else{
      a = 0;
    }
    if((b_value < button_b_threshold) && (b_value != 0)){
      // code for touch b
      Serial.print("Button B pressed with capacity value: ");
      Serial.print(b_value);
      Serial.println();
      b = 1;
    } else {
      b = 0;
    }

    if((c_value < button_c_threshold) && (c_value != 0)){
      // code for touch c
      Serial.print("Button C pressed with capacity value: ");
      Serial.print(c_value);
      Serial.println();  
      c = 1;
    } else {
      c = 0;
    }
    if((d_value < button_d_threshold) && (d_value != 0)){
      // code for touch d
      Serial.print("Button D pressed with capacity value: ");
      Serial.print(d_value); 
      Serial.println();    
      d = 1;
    } else {
      d = 0;
    }

    if((e_value < button_e_threshold) && (e_value != 0)){
      // code for touch e
      Serial.print("Button E pressed with capacity value: ");
      Serial.print(e_value); 
      Serial.println();  
      e = 1;
    } else {
      e = 0;
    }

    if((f_value < button_f_threshold) && (f_value != 0)){
      // code for touch f
      Serial.print("Button F pressed with capacity value: ");
      Serial.print(f_value); 
      Serial.println();  
      f = 1;
    } else {
      f = 0;
    }


   if((g_value < button_g_threshold) && (g_value != 0)){
      // code for touch g
      Serial.print("Button G pressed with capacity value: ");
      Serial.print(g_value); 
      Serial.println();
      g = 1;
    } else {
      g = 0;
    }

    if((h_value < button_h_threshold) && (h_value != 0)){
      // code for touch h
      Serial.print("Button H pressed with capacity value: ");
      Serial.print(h_value); 
      Serial.println();   
      h = 1;
    } else {
      h = 0;
    }
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
