# api-client-python
Python libraries for convenient access to PYLOT cloud platform by its customers & partners.

Communication is done through HTTPS JSON REST protocols.

All requests are idempotent, which means you may resend the same request multiple times without bad consequences.

Short outages of API servers may occur. So when making a call to API (through methods of the library), it is preferable to
wrap the call into retry logic with exponential backoff and jitter (e.g. see https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter).     

## Sending measurements to PYLOT API
The client application should have a unique `adapter` name to identify itself in PYLOT cloud. Usually it is third-party application name
suffixed with the location name.

Each measurement:
* is associated with a `node` to which the measurement relates to. It is compartment/climate zone/valve/drain/set of devices of specific type etc.  
* have a metric id it represents. Preferably it is one of PYLOT's metrics  

_``=> adapter, node, metric ids should be agreed with PYLOT team beforehand.``_

* is supplemented with its `timestamp` - moment of time it was collected. The timestamp is always in the greenhouse
local time zone. 
* value is always of numeric type

### Security
For simplicity, your application may just use a login/password to be authenticated in PYLOT cloud. The credentials will be granted to you by PYLOT team. 

### Resending data
If you found a mistake in the measurements you have already sent to PYLOT cloud - not a problem. Just resend correct data with the same `timestamps` and 
your fresh version of data will overwrite the wrong one inside PYLOT databases.

### Ways of using the library
There are two ways of using the library.
See usage of both methods in `/tests/demo.py`
#### Direct API call
This way, a bit more lower level, implies that you yourself compose the list of MeasurementsRow objects that are to be sent to PYLOT API.
You should yourself collect measurements of different metrics in different `nodes` of different `timestamps`, so that  
one MeasurementsRow has all the measurements of the same `node` of the same `timestamp`.

   
Example of the request
```javascript
[{
    // app name + location 
    "adapter":"weight-system-dankov",
    // Compartment/climate zone/valve/drain inside third-party application
    "node": "Compartment 2 Zone 2",		
    "timestamp":"2017-04-05T14:30:25",	// Greenhouse time of measurements        
    "data": {                           // Measurements array
       "220": 57.56                     // Metric id and measured value
    }
},
{
    "adapter":"weight-system-dankov",		
    "node": "Compartment 3 Zone 1",			
    "timestamp":"2017-04-05T14:30:25",	
    "data" : {					
       "221": 30.56,				
       "222": 1.06e-2,				
       "223": 1,				
       //...
   }
}]
```

#### Using measurements accumulator
This is another way of sending data to PYLOT - using an accumulator.
You collect incoming measurements into accumulator's memory. They are automatically grouped into structures suitable for API call.
When you flush the accumulator they are send to PYLOT API and the accumulator is emptied.
This approach is more suitable when you collect measurements in realtime, 
rather than retrospectively from a persistent storage.


