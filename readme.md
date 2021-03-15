# installation

Needs an auth.json file in the following format:
```json
{
    "token":"bot token"
}
```

and a services.json dictating what it should be looking for, and where.

```json
[
    {
        "serviceName": "hordelings",
        "serviceType": "valheim",
        "host": "127.0.0.1",
        "statusPort": 2459,
        "startupCommand": "serviceControls\\startServer.bat",
        "shutdownCommand": "serviceControls\\stopServer.bat"
    },
    {
        "serviceName": "LaserScraper",
        "serviceType": "localApplication",
        "processName": "CmdMenus.py",
    }
]
```