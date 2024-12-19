
    const schema = {
  "asyncapi": "2.6.0",
  "defaultContentType": "application/json",
  "info": {
    "title": "",
    "version": "",
    "description": ""
  },
  "servers": {
    "development": {
      "url": "nats://localhost:4222",
      "protocol": "nats",
      "protocolVersion": "custom"
    }
  },
  "channels": {
    "properties:OnProperties": {
      "description": "    Consumes messages from properties     topic and produces messages to changes topic",
      "servers": [
        "development"
      ],
      "bindings": {
        "nats": {
          "subject": "properties",
          "bindingVersion": "custom"
        }
      },
      "subscribe": {
        "message": {
          "title": "properties:OnProperties:Message",
          "correlationId": {
            "location": "$message.header#/correlation_id"
          },
          "payload": {
            "properties": {
              "identificativo_immobile": {
                "description": "Identificativo dell'immobile",
                "title": "Identificativo Immobile",
                "type": "integer",
                "x-parser-schema-id": "<anonymous-schema-1>"
              },
              "data_aggiornamento": {
                "description": "Data di aggiornamento",
                "format": "date-time",
                "title": "Data Aggiornamento",
                "type": "string",
                "x-parser-schema-id": "<anonymous-schema-2>"
              },
              "tipo_immobile": {
                "enum": [
                  "Terreni",
                  "Fabbricati"
                ],
                "title": "PropertyTypeEnum",
                "type": "string",
                "x-parser-schema-id": "PropertyTypeEnum"
              },
              "identificativo_operazione": {
                "enum": [
                  "FRAZIONAMENTO",
                  "ACCORPAMENTO"
                ],
                "title": "ChangeTypeEnum",
                "type": "string",
                "x-parser-schema-id": "ChangeTypeEnum"
              }
            },
            "required": [
              "identificativo_immobile",
              "data_aggiornamento",
              "tipo_immobile",
              "identificativo_operazione"
            ],
            "title": "Property",
            "type": "object",
            "x-parser-schema-id": "Property"
          },
          "x-parser-message-name": "properties:OnProperties:Message"
        }
      }
    },
    "changes:Publisher": {
      "description": "    Produces a message on changes     after receiving a message on properties",
      "servers": [
        "development"
      ],
      "bindings": {
        "nats": {
          "subject": "changes",
          "bindingVersion": "custom"
        }
      },
      "publish": {
        "message": {
          "title": "changes:Publisher:Message",
          "correlationId": {
            "location": "$message.header#/correlation_id"
          },
          "payload": {
            "x-parser-schema-id": "changes:PublisherPayload"
          },
          "x-parser-message-name": "changes:Publisher:Message"
        }
      }
    }
  },
  "components": {
    "messages": {
      "properties:OnProperties:Message": "$ref:$.channels.properties:OnProperties.subscribe.message",
      "changes:Publisher:Message": "$ref:$.channels.changes:Publisher.publish.message"
    },
    "schemas": {
      "ChangeTypeEnum": "$ref:$.channels.properties:OnProperties.subscribe.message.payload.properties.identificativo_operazione",
      "PropertyTypeEnum": "$ref:$.channels.properties:OnProperties.subscribe.message.payload.properties.tipo_immobile",
      "Property": "$ref:$.channels.properties:OnProperties.subscribe.message.payload",
      "changes:PublisherPayload": "$ref:$.channels.changes:Publisher.publish.message.payload"
    }
  },
  "x-parser-spec-parsed": true,
  "x-parser-api-version": 3,
  "x-parser-spec-stringified": true
};
    const config = {"show":{"sidebar":true},"sidebar":{"showOperations":"byDefault"}};
    const appRoot = document.getElementById('root');
    AsyncApiStandalone.render(
        { schema, config, }, appRoot
    );
  