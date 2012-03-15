var frameSize = 2048,
    bufferSize = frameSize / 2,
    sampleRate = 44100,
    signal = new Float32Array(bufferSize),
    fft = new FFT(bufferSize, sampleRate),
    bd = new BeatDetektor(60, 90),
    vu = new BeatDetektor.modules.vis.VU(),
    m_BeatCounter = 0,
    m_BeatTimer = 0,
    clearClr = [0,0,1],
    ftimer = 0,
    audio;

if (window.addEventListener) {
    window.addEventListener("load", function() {
            audio = document.getElementById("grappes");
            audio.addEventListener('MozAudioAvailable', audioAvailable, false);
    }, true);
}

function startProcessingAudio() {
        Processing.getInstanceById("audiocube").loop();
        audio.play();
}

function stopProcessingAudio() {
        Processing.getInstanceById("audiocube").noLoop();
        audio.pause();
}

function audioAvailable(event) {
    var frameBuffer = event.frameBuffer;
    timestamp = event.time;
    // de-interleave and mix down to mono
    signal = DSP.getChannel(DSP.MIX, frameBuffer);
    // perform forward transform
    fft.forward(signal);
    // beat detection
    bd.process( timestamp, fft.spectrum );
    ftimer += bd.last_update;
    if (ftimer > 1.0/24.0) {
        vu.process(bd,ftimer);
        ftimer = 0;
    }
}

