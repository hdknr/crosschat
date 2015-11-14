console.log("Ok, AutobahnJS loaded", autobahn.version);

var user = "{{ request.user.username }}";
var key = "{{ request.user.socketuser.key }}";
var wsuri = "{{ wsuri }}";
var topic = "{{ room.uri }}";
var payload = [];
var option = {acknowledge: true};
var realm = 'realm1';

      
function onchallenge (session, method, extra) {
    if (method === "wampcra") {
        console.log("onchallenge: authenticating via '" + method + "' and challenge '" + extra.challenge + "'");
        return autobahn.auth_cra.sign(key, extra.challenge);
    } else {
        throw "don't know how to authenticate using '" + method + "'";
    }
}

var connection = new autobahn.Connection({
    url: wsuri, realm: realm,
    // the following attributes must be set of WAMP-CRA authentication
    authmethods: ["wampcra"], authid: user, onchallenge: onchallenge
});


var the_session = null;
var the_subscription = null;

connection.onopen = function (session, details) {
    the_session = session;

    console.log("connected session with ID " + session.id);
    console.log("authenticated using method '" + details.auuthmethod + "' and provider '" + details.authprovider + "'");
    console.log("authenticated with authid '" + details.authid + "' and authrole '" + details.authrole + "'");

    the_session.subscribe(topic, onMessage ).then(
      function(subscription) {
         console.log("subscriped", subscription);
         the_subscription = subscription;
      },  
      function(error) {
         console.log("subscription failed ", error);
      }   
   );  

}   // onopen

connection.onclose = function (reason, details) {
    console.log("disconnected", reason, details.reason, details);
}

connection.open();

function sendMessage(message) {
   console.log("send message");

   var payload = {}; 
   payload.message = message;
   payload.nick = user;
   opts = {exclude_me: false, acknowledge: true};

   // http://autobahn.ws/js/tutorial_pubsub.html#on-connect
   the_session.publish( topic, [payload], {}, opts).then( 
      function(publication){},
      function(error) {
         console.log("publication failed ", error);
      }   
   );       
};

