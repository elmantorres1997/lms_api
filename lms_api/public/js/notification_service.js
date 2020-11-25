/* This is a Notification Service  */
let notificationMP3 = window.location.origin + "/assets/lms_api/mp3/notification.mp3";
let notificationOGG = window.location.origin + "/assets/lms_api/mp3/notification.ogg";
//
let notificationSound = new Howl({
  src: [notificationMP3, notificationOGG]
});

let notificationPermission = function() {
    return Notification.permission;
}

let askPermission = function() {
    if (notificationPermission() !== 'granted') {
        Notification.requestPermission();
    }
};

let isNotificationGranted = function () {
    if (notificationPermission() === "granted") {
        return true;
    } else {
        return false;
    }
}

let notify = function(message, title="New Notification",sound_only=false,link="", icon="") {
    if (isNotificationGranted() && message) {
        if (sound_only == false) {
            let notification = new Notification(title,{
                icon: icon,
                body: message
            });
        }

        try{
            notificationSound.play();
        } catch(e) {}
        notification.onclick = function(x) {
             try {
                if(link!==""){
                    window.open(link)
                } else{
                   window.focus();
                    this.cancel();
                }

             }
             catch (ex) {
             }
        };
    } else {
        askPermission();
    }

}
