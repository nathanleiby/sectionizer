'use strict';

// Create an instance
var wavesurfer2 = Object.create(WaveSurfer);

// Init & load mp3
document.addEventListener('DOMContentLoaded', function () {
    var options = {
        container     : document.querySelector('#waveform2'),
        waveColor     : "rgba(0, 125, 125, 0.3)",
        progressColor : "rgba(0, 125, 125, 0.2)",
        // waveColor     : 'violet',
        // progressColor : 'purple',
        loaderColor   : 'purple',
        cursorColor   : 'navy',
        markerWidth   : 2,
        skipLength    : 5
    };

    if (location.search.match('scroll')) {
        options.minPxPerSec = 100;
        options.scrollParent = true;
    }

    if (location.search.match('canvas')) {
        options.renderer = 'Canvas';
    }

    if (location.search.match('svg')) {
        options.renderer = 'SVG';
    }

    /* Progress bar */
    var progressDiv = document.querySelector('#progress-bar');
    var progressBar = progressDiv.querySelector('.progress-bar');
    progressBar.style.width = '100%';
    wavesurfer2.on('ready', function () {
        progressDiv.style.display = 'none';
    });

    // Init
    wavesurfer2.init(options);
    // Load audio from URL
    wavesurfer2.load('example/media/demo.mp3');

    // Start listening to marks being reached by cursor
    wavesurfer2.bindMarks();
    // Start listening to drag'n'drop on document
    wavesurfer2.bindDragNDrop();
});

// Play at once when ready
// Won't work on iOS until you touch the page
wavesurfer2.on('ready', function () {
    wavesurfer2.play();
    wavesurfer2.toggleMute();
});

// Bind buttons and keypresses
wavesurfer2.on('ready', function () {
    var eventHandlers = {
        'play': function () {
            wavesurfer2.playPause();
        },

        'green-mark': function () {
            wavesurfer2.mark({
                id: 'up',
                color: 'rgba(0, 255, 0, 0.5)'
            });
        },

        'red-mark': function () {
            wavesurfer2.mark({
                id: 'down',
                color: 'rgba(255, 0, 0, 0.5)'
            });
        },

        'back': function () {
            wavesurfer2.skipBackward();
        },

        'forth': function () {
            wavesurfer2.skipForward();
        },

        'toggle-mute': function () {
            wavesurfer2.toggleMute();
        }
    };

    document.addEventListener('keydown', function (e) {
        var map = {
            32: 'play',       // space
            38: 'green-mark', // up
            40: 'red-mark',   // down
            37: 'back',       // left
            39: 'forth'       // right
        };
        if (e.keyCode in map) {
            var handler = eventHandlers[map[e.keyCode]];
            e.preventDefault();
            handler && handler(e);
        }
    });

    document.addEventListener('click', function (e) {
        var action = e.target.dataset && e.target.dataset.action;
        if (action && action in eventHandlers) {
            eventHandlers[action](e);
        }
    });
});

// Flash when reaching a mark
wavesurfer2.on('mark', function (marker) {
    var markerColor = marker.color;

    setTimeout(function () {
        marker.update({ color: 'yellow' });
    }, 100);

    setTimeout(function () {
        marker.update({ color: markerColor });
    }, 300);
});
