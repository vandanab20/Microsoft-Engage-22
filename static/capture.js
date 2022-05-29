const camera = document.getElementById('camera');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const captureButton = document.getElementById('capturebutton');
const imageUrlLabel = document.getElementById("imageurl");
const gpsLabel = document.getElementById("location");
const statusLabel = document.getElementById("status")

/* Message to display on blank canvas */
context.font = "20px Arial";
context.fillText("Please capture an image !", 45, 120)

const constraints = {
  video : true
};

navigator.mediaDevices.getUserMedia(constraints)
  .then((stream) => {
  camera.srcObject = stream;
});

captureButton.addEventListener('click', () => {
  /* Draw captured image on canvas */
  context.clearRect(0, 0, canvas.width, canvas.height);
  context.drawImage(camera, 0, 0, canvas.width, canvas.height)

  /* Get the image in Base64 encoding and skip header part */
  var imageBase64 = canvas.toDataURL().slice(22);

    /* Upload the image to imgur */
    $.ajax({
      url: "https://api.imgur.com/3/image",
      type: "POST",
      datatype: "json",
      headers: {
        "Authorization": "Client-ID f58da3baf47229c",
        "Authorization" : "Bearer 80dc58f5739f9a81270e0c460e3801a729b78d2b"
      },
      data: {
        "image": imageBase64
      }
    }).done( response => {

      url = "https://imgur.com/" + response.data.id
      //imageUrlLabel.innerHTML = url
      imageUrlLabel.setAttribute("href", url)

      console.log(response.data.id);

      /* Get location */
      navigator.geolocation.getCurrentPosition( position => {


        const latitude = position.coords.latitude
        const longitude = position.coords.longitude

        gpsLabel.innerHTML = latitude + ", " + longitude;

        /* Send image and its metadata to flask server */
        $.post("/Attendance",
        {
          imageID : response.data.id,
          latitude : latitude,
          longitude : longitude
        }).done( (res) => {
          console.log(res);
          imageUrlLabel.innerHTML = res;
          statusLabel.innerHTML = "Save successful for Image ID: "  + response.data.id;
        }).fail( () => {
          console.log('Could not send data to server');
          statusLabel.innerHTML = "Unable to send data to server for Image ID: "  + response.data.id;
        });

      }, error => {
        console.log('Unable to get the GPS Co-ordinates');
        gpsLabel.innerHTML = "Error";
        statusLabel.innerHTML = "Unable to get the GPS Co-ordinates";
      });

    }).fail( () => {
      console.log('Image upload to Imgur failed');
      imageUrlLabel.innerHTML = "Error";
      statusLabel.innerHTML = "Image upload to Imgur failed";
    });

});
