#include "cam_server.h"
#include "esp_timer.h"
#include <WiFi.h>
#include "Arduino.h"
#include <SPIFFS.h>
#include <ESPAsyncWebServer.h>

#define PIN_7 13
#define PIN_8 14 
#define PIN_9 15 

const char *ssid = "AGV";
const char *password = "12345678";

AsyncWebServer server(80);
AsyncWebSocket ws("/ws");

void initSPIFFS()
{
  if (!SPIFFS.begin())
  {
    Serial.println("Cannot mount SPIFFS volume...");
  }
}

void initWebServer()
{
  server.serveStatic("/", SPIFFS, "/").setDefaultFile("index.html");
  server.begin();
}
void notifyClients (uint8_t *data) {
  ws.textAll ((char*) data);
}
void handleWebSocketMessage(void *arg, uint8_t *data, size_t len)
{
  AwsFrameInfo *info = (AwsFrameInfo *)arg; 
  if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT)
  {
    data[len] = 0;
    notifyClients (data);
    if (!strcmp((char *)data, "forward"))
    { 
      digitalWrite(PIN_7, 1);
      digitalWrite(PIN_8, 0);
      digitalWrite(PIN_9, 0);
    }
    if (!strcmp((char *)data, "backward"))
    {
      digitalWrite(PIN_7, 0);
      digitalWrite(PIN_8, 1);
      digitalWrite(PIN_9, 0);
    }
    if (!strcmp((char *)data, "left"))
    {
      digitalWrite(PIN_7, 1);
      digitalWrite(PIN_8, 1);
      digitalWrite(PIN_9, 0);
    }
    if (!strcmp((char *)data, "right"))
    {
      digitalWrite(PIN_7, 0);
      digitalWrite(PIN_8, 0);
      digitalWrite(PIN_9, 1);
    }
    if (!strcmp((char *)data, "stop"))
    {
      digitalWrite(PIN_7, 1);
      digitalWrite(PIN_8, 1);
      digitalWrite(PIN_9, 1);
    }
  }
}

// WebSocket initialization
void onEvent(AsyncWebSocket *server,       //
             AsyncWebSocketClient *client, //
             AwsEventType type,            // the signature of this function is defined
             void *arg,                    // by the `AwsEventHandler` interface
             uint8_t *data,                //
             size_t len)
{
  switch (type)
  {
  case WS_EVT_CONNECT:
    Serial.printf("WebSocket client #%u connected from %s\n", client->id(), client->remoteIP().toString().c_str());
    break;
  case WS_EVT_DISCONNECT:
    Serial.printf("WebSocket client #%u disconnected\n", client->id());
    break;
  case WS_EVT_DATA:
    handleWebSocketMessage(arg, data, len);
    break;
  case WS_EVT_PONG:
  case WS_EVT_ERROR:
    break;
  }
}

void initWebSocket()
{
  ws.onEvent(onEvent);
  server.addHandler(&ws);
}

void setup()
{
  // Wi-Fi connection
  WiFi.softAP(ssid, password);
  IPAddress miIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(miIP); // probar 192.168.4.1

  pinMode(PIN_7, OUTPUT);
  pinMode(PIN_8, OUTPUT);
  pinMode(PIN_9, OUTPUT);

  Serial.begin(115200);
  Serial.setDebugOutput(false);

  // Start cam server
  //setup_cam_server();
  // Start streaming web server
  initSPIFFS();
  initWebSocket();
  initWebServer();
}

void loop()
{
  ws.cleanupClients();
}