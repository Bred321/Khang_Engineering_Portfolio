#include "cam_server.h"
#include "esp_timer.h"
#include <WiFi.h>
#include "Arduino.h"
#include <SPIFFS.h>
#include <ESPAsyncWebServer.h>

const char *ssid = "AGV2";
const char *password = "12345678";

AsyncWebServer server(80);
AsyncWebSocket ws("/ws");
int speedValue = 0;
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
void notifyClients(uint8_t *data)
{
  ws.textAll((char *)data);
}
void handleWebSocketMessage(void *arg, uint8_t *data, size_t len)
{
  AwsFrameInfo *info = (AwsFrameInfo *)arg;
  if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT)
  {
    data[len] = 0;
    notifyClients(data);
    if (!strcmp((char *)data, "forward"))
    {
      Serial.printf("l %d %d'\n", speedValue, speedValue);
    }
    if (!strcmp((char *)data, "backward"))
    {
      Serial.printf("l -%d -%d'\n", speedValue, speedValue);
    }
    if (!strcmp((char *)data, "left"))
    {
      Serial.printf("l -%d %d'\n", speedValue, speedValue);
    }
    if (!strcmp((char *)data, "right"))
    {
      Serial.printf("l %d -%d'\n", speedValue, speedValue);
    }
    else if (!strcmp((char *)data, "stop") || !strcmp((char *)data, "manual"))
    {
      Serial.println("l 0 0'");
    }
    if (!strcmp((char *)data, "automated"))
    {
      Serial.println("a'");
    }
    else if (String((char *)data).startsWith("setSpeed:"))
    {
      String speedValueStr = String((char *)data).substring(9); // Get the part after "setSpeed:"
      speedValue = speedValueStr.toInt();
      Serial.print("Speed updated to: ");
      Serial.println(speedValue);
    }
    if (strstr((char *)data, "Choose Plant") != nullptr)
    {
      int plantNumber = atoi((char *)data + strlen("Choose Plant "));
      Serial.print("m ");
      Serial.print(plantNumber);
      Serial.println("'");
    }
    else if (strstr((char *)data, "Unchoose Plant") != nullptr)
    {
      int plantNumber = atoi((char *)data + strlen("Unchoose Plant "));
      Serial.print("m ");
      Serial.print(plantNumber);
      Serial.println("'");
    }
    if (strstr((char *)data, "reset") != nullptr)
    {
      Serial.println("r'");
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

  Serial.begin(115200);
  Serial.setDebugOutput(false);

  // Start cam server
  setup_cam_server();
  // Start streaming web server
  initSPIFFS();
  initWebSocket();
  initWebServer();
}

void loop()
{
  ws.cleanupClients();
}