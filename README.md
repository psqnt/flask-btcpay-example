# Flask BTCPayServer Example
This repo will show the bare bones of getting a website built with flask to integrate bitcoin/lightning using BTCPayServer.

If you want to learn flask, you only need to do two things:
1. Go through this tutorial all the way, every step
https://flask.palletsprojects.com/en/1.1.x/tutorial/#tutorial

2. Go through this tutorial all the way, every step
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

If you have python experience and do both of these things you can built a lightning app.

```
Note: This project is based on source code from the first tutorial, as I originally wrote 
a lot of this code 2 years ago. However, The second tutorial (Flask Mega Tutorial), is 
very good and goes very in depth and you should probably based projects on that.
```

## Pre-requisites
Before you can built the webserver in flask, you need the other software systems up and running. There's lots out there to do this. 

I personally recommend ketan's / ministry of nodes tutorials on youtube (nodebox). you can view these here:

https://www.youtube.com/watch?v=BIrL1lNsnJQ&list=PLCRbH-IWlcW17JxQ4mdv9DwSMJZlvUOle

OR you can use a mynodebtc or getumbrel raspberrypi nodes, which is basically a pre-built version of ministry of nodes tutorials but works right out of the box.

MyNode: https://github.com/mynodebtc/mynode
Umbrel: https://github.com/getumbrel/umbrel

I did the nodebox tutorial on my desktop and developed there, then I deployed to my mynodebtc over tor to expose it to the internet.

^ Make sure all that is setup first before starting this

## Virtual Environment
When using python or flask always use a virtual environment to keep imports and dependencies consistent.

```
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Setup Environment Variables
You can put all your environment vars in a `.env` file or source them in the command line
```
export FLASK_APP=start_flask_server.py
export FLASK_ENV=development
export FLASK_TOR=True
export SECRET_KEY=super-secret-key
export DEBUG=True
export ADMIN_EMAIL_ADDRESS_LIST=an-email-if-being-used
export TIP_CURRENCY=BTC
export TIP_AMOUNT=0.0000010
```

## Initialize the database
This will create a sqlite database in the `instance` folder
The code for this is in `db.py` it uses `click` to create a cli command
```
flask init-db
```


## BTCPayServer Python Client Instructions
You need to make a connection to your btcpayserver instance and store the client
in the database, you only need create the client once. Don't try to create a 
connection twice it will give you errors.

Follow the instructions in the readme here
https://github.com/btcpayserver/btcpay-python

I built a flask command in this repo that can be used as well.
```
flask btcpay-client <token> <url>
```

## btcpay.js
This code is provided in your btcpayserver instance here:
```
your.btcpay.url/modal/btcpay.js
```
So if you need just go to that url and copy it.

I provide it in this library because we need it in our frontend and we need to 
make an edit here.

I learned to this from the official docs here:
https://docs.btcpayserver.org/CustomIntegration/#modal-checkout

We need to manually set the origin of the btcpayserver instance in btcpay.js
file:
```
var origin = 'http://chat.btcpayserver.org join us there, and initialize this with your origin url through setApiUrlPrefix';
```
If you are running over tor, you need to get the hostname of your btcpay instance.

Do this to get it:
```
sudo cat /var/lib/tor/btcpayserver/hostname
```
^ may differ if you named it something else

if you are using mynodebtc
```
sudo cat /var/lib/tor/mynode_btcpay/hostname
```
or just look in the admin at `mynode.local/tor`

If you are not using tor just set this to the URL that your btcpay server is running on

In my case for local testing my variable is this:
```
var origin = 'http://localhost:23001';
```
Be aware:
```
NOTE: Do not using a trailing slash it wont work
```

## How to use btcpay.js
So the btcpay.js is important because it allows us (the webserver) to know when
an action has taken place .. like getting paid.

In lightning.html you can see this small script:
```javascript
function show_invoice(id) {
    window.btcpay.showInvoice(id);
}
window.btcpay.onModalReceiveMessage((event) => {
    if (typeof event.data == "object") {
        window.location.replace("{{redirect}}");
    }
});
```
the function `show_invoice` calls the btcpay.js function `showInvoice`,
which we inject into the html as a model.

when the invoice is paid we will receive a call back notifying us. To capture this
event we define a call back function. thats this:
```
window.btcpay.onModalReceiveMessage((event) => {
    if (typeof event.data == "object") {
        window.location.replace("{{redirect}}");
    }
```
This is saying when we receive a message, check the event data, if the event 
data is of type "object" then redirect.

The reason I chose object here is because all the other events that occur..
open, close, expired, etc

are just a string, however when the invoice is paid its an object, if you want 
a more robust way of checking this just print the event to console and inspect 
the data to get some insight

So thats how we can interact with lightning network and make our website do 
stuff when an invoice is paid, theres lots more to play around with but this
is enough to get started.

## Starting the server
if running over tor. if you want to learn more about starting the server over tor
read this:
https://stem.torproject.org/tutorials/over_the_river.html
```
python start_flask_server.py
```
If you are in development the server starts up twice so always use the last onion created,
all others are overwritten

Also note, if you want to keep the same tor in production then create a folder 
called: `.tor` and use production, it will store the key to reuse the same 
tor url there

if testing locally or not over tor
```
flask run
```

## Deployment
You can deploy this anywhere you can run a website basically, you can learn some here:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux

Personally right now I am deploying mine on my raspberrypi mynodebtc.

1. SSH into mynode
2. clone your git repository to your mynode or copy the files over
3. Follow the steps above the start up the webserver
    a. remember the different changes that need to be made like btcpay url, btcpay client etc
4. Turn FLASK_TOR on using environment variables and set FLASK_ENV to production
5. run `python start_flask_server.py` and your hidden service will start up,

Disclaimer: Technically you should use a WSGI server for production, I'll add how 
to do that soon but here is a link that looks helpful:
https://iotbytes.wordpress.com/python-flask-web-application-on-raspberry-pi-with-nginx-and-uwsgi/


Now you have a soveriegn and actually decentralized financial tool, congrats
Long Bitcoin

#### CSS Note
I dress up the html a little bit using `skeleton.css`
https://github.com/dhg/Skeleton

But use whatever you want, bootstrap is nice and easy too