window.onload = function(){

  var socket = io.connect('http://' + document.domain + ':' + location.port);
  var term = '';
  var mainVolume = 1;

  var sampler = new Tone.Sampler({
    "Key" : "./static/samples/key.wav",
  }).toMaster();

  socket.on('connect', function() {
      console.log("DEBUG: Conected to server socket");
  });

  termForm = document.getElementById("termForm")
  termForm.onsubmit = function () {
    term = document.getElementsById("termData").value;
    console.log('DEBUG: Clicked connect button, emitting term: ' + term );
    socket.emit('term', {data: term});
  }

  socket.on('vector', function(data) {
    var sum = data.reduce(function(previousValue, currentValue, currentIndex, array) {
      return previousValue + currentValue;
    });
    if (sum >= 10) {
        sampler.triggerAttack("Key");
    }
    console.log('Received a vector: ' + data + ' ' + sum);
  });

  socket.on('error', function(data) {
    console.log(data);
  });

  // connect = document.getElementById("connect")
  // connect.onclick = function () {
  //   console.log('DEBUG: Clicked connect button, emitting term');
  //   socket.emit('term', {data: ''});
  // }

  // disconnect = document.getElementById("disconnect")
  // disconnect.onclick = function () {
  //   console.log('DEBUG: Clicked disconnect button');
  //   socket.disconnect();
  // }

  // Tone.Buffer.on('load', function () {
  //   console.log('Loaded samples')
  // })
  //
  // var monoSynth = new Tone.SimpleSynth().toMaster();
  // var mono = document.getElementById("monoTrigger");
  // mono.onclick = function(){
  //   monoSynth.triggerAttackRelease("C4", "4n");
  // };
  //
  // var polySynth = new Tone.PolySynth(6, Tone.MonoSynth).toMaster();
  // var poly = document.getElementById("polyTrigger");
  // poly.onclick = function(){
  //   polySynth.triggerAttackRelease(["C4", "E4", "G4"], "4n");
  // };
  //
  // var sampler = new Tone.Sampler({
  //   "Key" : "./static/samples/key.wav",
  // }).toMaster();
  // var test = document.getElementById("test");
  // test.onclick = function(){
  //   sampler.triggerAttack("Key");
  // };
};
