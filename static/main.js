window.onload = function(){

  var socket = io.connect('http://' + document.domain + ':' + location.port);
  var term = '';
  var mainVolume = 1;

  var sampler = new Tone.Sampler({
    "Key" : "./static/samples/key.wav",
    "Beep" : "./static/samples/beep.wav",
    "a" : "./static/samples/a.mp3",
    "b" : "./static/samples/b.mp3",
    "c" : "./static/samples/c.mp3",
    "d" : "./static/samples/d.mp3",
    "e" : "./static/samples/e.mp3",
    "f" : "./static/samples/f.mp3",
    "g" : "./static/samples/g.mp3",
  }).toMaster();

  socket.on('connect', function() {
      console.log("DEBUG: Conected to server socket");
  });

  termTrigger = document.getElementById("termTrigger");
  termData = document.getElementById("termData");
  termTrigger.onclick = function () {
    term = termData.value;
    console.log('DEBUG: Clicked connect button, emitting term: ' + term );
    socket.emit('term', {data: term});
  }

  socket.on('vector', function(data) {
    var sum = data.reduce(function(previousValue, currentValue, currentIndex, array) {
      return previousValue + currentValue;
    });
    // ['anger',
    //   'anticipation',
    //   'disgust',
    //   'fear',
    //   'joy',
    //   'negative',
    //   'positive',
    //   'sadness',
    //   'surprise',
    //   'trust']
    if (sum >= 20) { sampler.triggerAttack("Key"); }
    if (data[1] >= 3) { sampler.triggerAttack("a"); }
    if (data[2] >= 3) { sampler.triggerAttack("b"); }
    if (data[3] >= 3) { sampler.triggerAttack("c"); }
    if (data[4] >= 3) { sampler.triggerAttack("d"); }
    if (data[5] >= 3) { sampler.triggerAttack("e"); }
    if (data[8] >= 3) { sampler.triggerAttack("f"); }
    if (data[9] >= 3) { sampler.triggerAttack("g"); }
    if (data[10] >= 1) { sampler.triggerAttack("Beep"); }
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
