window.onload = function(){

  var socket = io.connect('http://' + document.domain + ':' + location.port);

  socket.on('connect', function() {
      console.log("DEBUG: Conected to server socket");
  });

  connect = document.getElementById("connect")
  connect.onclick = function () {
    console.log('DEBUG: Clicked connect button, emitting term');
    socket.emit('term', {data: ''});
  }

  disconnect = document.getElementById("disconnect")
  disconnect.onclick = function () {
    console.log('DEBUG: Clicked disconnect button');
    socket.disconnect();
  }

  socket.on('vector', function(data) {
    console.log('Received a vector: ' + data);
  });

  socket.on('error', function(data) {
    console.log(data);
  });

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
