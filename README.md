# LaMetric app for Netatmo Weather Station

A simple client which turns LaMetric into Netamo display. This client polls [Netatmo API](https://github.com/philippelt/netatmo-api-python)  and shows the weather data on LaMetric display.

![screencast](screenshots/netatmo.gif)

## LaMetric Setup

Go to the [LaMetric Developper site](https://developer.lametric.com) signin with your credentials (or signup for an account if you haven't done so already). Now create your new app with with the following five frames:

1. "Name" frame for Outdoor temperature value
2. "Sparkline" frame for Outdoor temperature graph
3. "Name" frame for Outdoor humidity value
4. "Name" frame for Pressure trend (icon) and value
5. "Name" frame for Sunrise time
6. "Name" frame for Sunset time

*Note:* The text and icon on the each frame are optional. They will be overriden by the script anyway.

Make sure to set the app to use *Push Mode*. Publish your app as a private app.

![screencast](screenshots/lametric_app2.png)

Now make a note of both `app_id` and `access_token` as per screenshot above and put them into your `config.ini` within the `[lametric]` part.

## Netatmo Setup

Go to the [Netatmo Developer Site](https://dev.netatmo.com) again signin with your credentials (or signup for an account if you haven't done so already).

Again create an app. Leave Redirect URI / Webhook URI empty. Make sure to enable the app. 

![screencast](screenshots/netatmo_app.png)

Now make a note of `client_id`, `client_secret`, `username` which is your emaill and `password` as per screenshot above and put them into your `config.ini` within the `[netatmo]` part.

## The Script 

Once you have created both LaMetric and Netatmo apps you can use APIs to connect the two. As described above the credentials are stored in `config.ini` file in the same directory as the updateLaMetric.py script.

```
# Netatmo authentication
[netatmo]
client_id     = ...
client_secret = ...
username      = ...
password      = ...

# LaMetric authentication
[lametric]
access_token  = ...
app_id        = ...
```

Running `updateLaMetric.py` script should give you immediate feedback on how successful you are with the setup process. Once everything is OK the easiest way to keep the LaMetric display updated is via cron task:

```
*/10 * * * * /home/lametric/updateLaMetric.py
```

Enjoy!
