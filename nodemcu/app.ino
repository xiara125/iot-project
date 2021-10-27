#include <Segment7.h>
#include <MqttCom.h>
#include <DHT.h>
#include <Analog.h>
#include <ArduinoJson.h>
#include <Led.h>
#include <Segment7.h>

const char *ssid = "SK_WiFiGIGAE247";
const char *password ="1707027087";
const char *mqtt_server ="192.168.35.129";

MqttCom com;
DHT dht11(D1, DHT11);
ShiftSegment segment(D5, D6, D7); // shift, latch, data
int preValue = 1;

void subscribe(char *topic, byte *payload, unsigned int length){
    char buf[128];
    memcpy(buf, payload, length);
    buf[length]='\0';


    // Json 역직렬화
    StaticJsonDocument<256> doc;
    auto error = deserializeJson(doc, buf);
    if (error){
        Serial.print("deserializeJson() failed with code");
        Serial.println(error.c_str());
        return;
    }
    
    // if (buf[0] == 's'){
    //     com.publish("iot/hong/floor/elevator",preValue);
    //     return;
    // }

    int value = buf[0] - '0';

    if (value == 0){
        Serial.println('성공');
        char msg[50];
        float fh, fc;
        fh = dht11.readHumidity(); // 습도 측정
        fc = dht11.readTemperature(); // 섭씨 온도 측정
        
        com.publish("iot/sensors/Room/temp", fc);
        com.publish("iot/sensors/Room/humi", fh);
        com.publish("iot/hong/floor/elevator",preValue);
        return;
    }

    if (preValue < value){
        for(int i=preValue;i<=value;i++){
            segment.display(i);
            com.publish("iot/hong/floor/elevator",i);
            delay(1000);
        }
        preValue = value;
    }
    else if(preValue>value){
        for(int i=preValue;i>=value;i--){
            segment.display(i);
            com.publish("iot/hong/floor/elevator",i);
            delay(1000);
        }
        preValue = value;
    }
    else if(preValue == value){
        com.publish("iot/hong/floor/elevator",value);
        segment.display(value);
    }
    
    
    if (value == 5){
        com.publish("iot/hong/arrive/elevator",1);
    }

    
    Serial.println(topic);
    Serial.println(buf[0]);

    
}

void publish() {
    char msg[50];
    float fh, fc;
    fh = dht11.readHumidity(); // 습도 측정
    fc = dht11.readTemperature(); // 섭씨 온도 측정
    
    com.publish("iot/sensors/Room/temp", fc);
    com.publish("iot/sensors/Room/humi", fh);
}

void pub_dht(char *topic, byte *payload, unsigned int length){
    char buf[128];
    memcpy(buf, payload, length);
    buf[length]='\0';

    Serial.println(buf);

    if (buf[0] == 'c'){
        Serial.println('성공');
        char msg[50];
        float fh, fc;
        fh = dht11.readHumidity(); // 습도 측정
        fc = dht11.readTemperature(); // 섭씨 온도 측정
        
        com.publish("iot/sensors/Room/temp", fc);
        com.publish("iot/sensors/Room/humi", fh);
    }
}


void setup() {
    Serial.begin(115200);
    com.init(ssid,password);
    com.setServer(mqtt_server,"iot/hong/control/elevator",subscribe);
    // com.setServer(mqtt_server,"iot/dht",pub_dht);
    com.setInterval(20000, publish);
    dht11.begin();
    segment.display(preValue);
}
void loop() {
    com.run();
}