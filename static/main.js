window.onload = function(){

  var socket = io.connect('http://' + document.domain + ':' + location.port);
  var term = '';
  var mainVolume = 1;
  var vizData = {}
  var vizDataTest = [{'data': {
    'anger': 5,
    'anticipation': 5,
    'disgust': 5,
    'fear': 5,
    'joy': 5,
    'sadness': 5,
    'surprise': 5,
    'trust': 5,
  }}];

  var sampler = new Tone.Sampler({
    "Key" : "./static/samples/key.wav",
    "Beep" : "./static/samples/beep.wav",
    a : { // Acentuation
      1 : "./static/samples/reggae/a01.wav",
      2 : "./static/samples/reggae/a02.wav",
      3 : "./static/samples/reggae/a03.wav",
      4 : "./static/samples/reggae/a04.wav",
      5 : "./static/samples/reggae/a05.wav",
      6 : "./static/samples/reggae/a06.wav",
    },
    b : { // Bass
      1 : "./static/samples/reggae/b01.wav",
      2 : "./static/samples/reggae/b02.wav",
      3 : "./static/samples/reggae/b03.wav",
      4 : "./static/samples/reggae/b04.wav",
      5 : "./static/samples/reggae/b05.wav",
      6 : "./static/samples/reggae/b06.wav",
      7 : "./static/samples/reggae/b07.wav",
      8 : "./static/samples/reggae/b08.wav",
    },
    c : { // Winds
      1 : "./static/samples/reggae/c01.wav",
      2 : "./static/samples/reggae/c02.wav",
      3 : "./static/samples/reggae/c03.wav",
      4 : "./static/samples/reggae/c04.wav",
      5 : "./static/samples/reggae/c05.wav",
      6 : "./static/samples/reggae/c06.wav",
      7 : "./static/samples/reggae/c07.wav",
      8 : "./static/samples/reggae/c08.wav",
      9 : "./static/samples/reggae/c09.wav",
      10 : "./static/samples/reggae/c10.wav",
      11 : "./static/samples/reggae/c11.wav",
    },
    d : { // Guitar
      1 : "./static/samples/reggae/d01.wav",
      2 : "./static/samples/reggae/d02.wav",
      3 : "./static/samples/reggae/d03.wav",
      4 : "./static/samples/reggae/d04.wav",
      5 : "./static/samples/reggae/d05.wav",
    },
    // Natalia
    // "a" : "./static/samples/a.mp3",
    // "b" : "./static/samples/b.mp3",
    // "c" : "./static/samples/c.mp3",
    // "d" : "./static/samples/d.mp3",
    // "e" : "./static/samples/e.mp3",
    // "f" : "./static/samples/f.mp3",
    // "g" : "./static/samples/g.mp3",
  }).toMaster();

  socket.on('connect', function() {
      console.log("DEBUG: Conected to server socket");
  });

// Change term on enter insde text input
  document.getElementById("termData")
      .addEventListener("keyup", function(event) {
      event.preventDefault();
      if (event.keyCode == 13) {
        term = termData.value;
        socket.emit('term', {data: term});
      }
  });

  socket.on('vector', function(data) {
    var sum = data.reduce(function(previousValue, currentValue, currentIndex, array) {
      return previousValue + currentValue;
    });

    vizData = [{'data': {
      'joy': data[4],
      'trust': data[7],
      'fear': data[3],
      'surprise': data[6],
      'sadness': data[5],
      'disgust': data[2],
      'anger': data[0],
      'anticipation': data[1],
    }}];

    var chart = radialBarChart()
      .barHeight(250)
      .domain([0,5])
      .barColors(['#EBC527','#79BF2A','#007C37','#1781AA','#296CAB','#7D4CA1','#DB1245','#E66F11']);

    d3.select('#viz')
      .datum(vizData)
      .call(chart);

    // [ 'anger',
    if (document.getElementById("anger").checked){
      if (data[1] >= 4) { sampler.triggerAttack("a.1"); }
      else if (data[1] >= 3) { sampler.triggerAttack("c.3"); }
      else if (data[1] >= 2) { sampler.triggerAttack("b.1"); }
    }
    //   'anticipation',
    if (document.getElementById("anticipation").checked){
      if (data[2] >= 4) { sampler.triggerAttack("c.1"); }
      else if (data[2] >= 3) { sampler.triggerAttack("c.4"); }
      else if (data[2] >= 2) { sampler.triggerAttack("b.2"); }
    }
    //   'disgust',
    if (document.getElementById("disgust").checked){
      if (data[3] >= 4) { sampler.triggerAttack("a.2"); }
      else if (data[3] >= 3) { sampler.triggerAttack("c.5"); }
      else if (data[3] >= 2) { sampler.triggerAttack("b.3"); }
    }
    //   'fear',
    if (document.getElementById("fear").checked){
      if (data[4] >= 4) { sampler.triggerAttack("a.3"); }
      else if (data[4] >= 3) { sampler.triggerAttack("c.6"); }
      else if (data[4] >= 2) { sampler.triggerAttack("b.4"); }
    }
    //   'joy',
    if (document.getElementById("joy").checked){
      if (data[5] >= 4) { sampler.triggerAttack("a.4"); }
      else if (data[5] >= 3) { sampler.triggerAttack("c.7"); }
      else if (data[5] >= 2) { sampler.triggerAttack("b.5"); }
    }
    //   'negative',
    //   'positive',
    //   'sadness',
    if (document.getElementById("sadness").checked){
      if (data[8] >= 4) { sampler.triggerAttack("a.5"); }
      else if (data[8] >= 3) { sampler.triggerAttack("c.8"); }
      else if (data[8] >= 2) { sampler.triggerAttack("b.6"); }
    }
    //   'surprise',
    if (document.getElementById("surprise").checked){
      if (data[9] >= 4) { sampler.triggerAttack("c.2"); }
      else if (data[9] >= 3) { sampler.triggerAttack("c.9"); }
      else if (data[9] >= 2) { sampler.triggerAttack("b.7"); }
    }
    //   'trust']
    if (document.getElementById("trust").checked){
      if (data[10] >= 4) { sampler.triggerAttack("a.6"); }
      else if (data[10] >= 3) { sampler.triggerAttack("c.10"); }
      else if (data[10] >= 2) { sampler.triggerAttack("b.8"); }
    }

    // Intensity
    if (sum >= 20) { sampler.triggerAttack("Key"); }
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
