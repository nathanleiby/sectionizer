'use strict';

WaveSurfer.Mixer = {
    init: function (params) {
        this.ac = params.AudioContext ||
            new (window.AudioContext || window.webkitAudioContext);

        this.createScriptNode();
        this.createVolumeNode();
    },

    setFilter: function (filterNode) {
        this.filterNode && this.filterNode.disconnect();
        this.gainNode.disconnect();
        if (filterNode) {
            filterNode.connect(this.ac.destination);
            this.gainNode.connect(filterNode);
        } else {
            this.gainNode.connect(this.ac.destination);
        }
        this.filterNode = filterNode;
    },

    createScriptNode: function () {
        var my = this;
        if (this.ac.createScriptProcessor) {
            this.scriptNode = this.ac.createScriptProcessor(256);
        } else {
            this.scriptNode = this.ac.createJavaScriptNode(256);
        }
        this.scriptNode.connect(this.ac.destination);
        this.scriptNode.onaudioprocess = function () {
            if (my.source && !my.isPaused()) {
                if (my.getCurrentTime() >= my.scheduledPause) {
                    my.pause();
                } else {
                    my.fireEvent('audioprocess');
                }
            }
        };
    },

    /**
     * Create the gain node needed to control the playback volume.
     */
    createVolumeNode: function () {
        // Create gain node using the AudioContext
        if (this.ac.createGain) {
            this.gainNode = this.ac.createGain();
        } else {
            this.gainNode = this.ac.createGainNode();
        }
        // Add the gain node to the graph
        this.gainNode.connect(this.ac.destination);
    },

    /**
     * Set the gain to a new value.
     *
     * @param newGain The new gain, a floating point value between -1
     * and 1. -1 being no gain and 1 being maxium gain.
     */
    setVolume: function (newGain) {
        this.gainNode.gain.value = newGain;
    },

    /**
     * Get the current gain
     *
     * @returns The current gain, a floating point value between -1
     * and 1. -1 being no gain and 1 being maxium gain.
     */
    getVolume: function () {
        return this.gainNode.gain.value;
    },

    refreshBufferSource: function () {
        this.source && this.source.disconnect();
        this.source = this.ac.createBufferSource();
        if (this.buffer) {
            this.source.buffer = this.buffer;
        }
        this.source.connect(this.gainNode);
    },

    setBuffer: function (buffer) {
        this.lastPause = 0;
        this.lastStart = 0;
        this.startTime = 0;
        this.paused = true;
        this.buffer = buffer;
    },

    /**
     * Decodes binary data and creates buffer source.
     *
     * @param {ArrayBuffer} arraybuffer Audio data.
     */
    loadBuffer: function (arraybuffer, cb, errb) {
        var my = this;

        if (this.source) {
            this.pause();
        }

        this.ac.decodeAudioData(
            arraybuffer,
            function (buffer) {
                my.setBuffer(buffer);
                cb && cb(buffer);
            },
            function () {
                console.error('Error decoding audio buffer');
                errb && errb();
            }
        );
    },

    loadEmpty: function () {
        this.pause();
        this.setBuffer(0);
    },

    isPaused: function () {
        return this.paused;
    },

    getDuration: function () {
        return this.buffer.duration;
    },

    /**
     * Plays the loaded audio region.
     *
     * @param {Number} start Start offset in seconds,
     * relative to the beginning of the track.
     *
     * @param {Number} end End offset in seconds,
     * relative to the beginning of the track.
     */
    play: function (start, end) {
        console.log('play', start, end);
        this.refreshBufferSource();

        if (null == start) { start = this.getCurrentTime(); }
        if (null == end) { end = this.getDuration(); }
        if (start > end) {
            start = 0;
        }

        this.lastStart = start;
        this.startTime = this.ac.currentTime;
        this.paused = false;
        this.scheduledPause = end;

        // this.source.playbackRate = 2;

        if (this.source.start) {
            this.source.start(0, start, end - start);
        } else {
            this.source.noteGrainOn(0, start, end - start);
        }
    },

    /**
     * Pauses the loaded audio.
     */
    pause: function () {
        this.lastPause = this.lastStart + (this.ac.currentTime - this.startTime);
        this.paused = true;
        if (this.source.stop) {
            this.source.stop(0);
        } else {
            this.source.noteOff(0);
        }
        this.source.disconnect();
        this.source = null;
    },

    /**
     * @returns {Float32Array} Array of peaks.
     */
    getPeaks: function (length, sampleStep) {
        sampleStep = sampleStep || 128;
        var buffer = this.buffer;
        var k = buffer.length / length;
        var peaks = new Float32Array(length);

        for (var c = 0; c < buffer.numberOfChannels; c++) {
            var chan = buffer.getChannelData(c);

            for (var i = 0; i < length; i++) {
                var peak = -Infinity;
                var start = ~~(i * k);
                var end = (i + 1) * k;
                for (var j = start; j < end; j += sampleStep) {
                    var val = chan[j];
                    if (val > peak) {
                        peak = val;
                    } else if (-val > peak) {
                        peak = -val;
                    }
                }

                if (c > 0) {
                    peaks[i] += peak;
                } else {
                    peaks[i] = peak;
                }
            }
        }

        return peaks;
    },

    getMaxPeak: function () {
        /* Peaks are sums of absolute peak values from each channel. */
        return this.buffer.numberOfChannels * 1.0;
    },

    getPlayedPercents: function () {
        var duration = this.getDuration();
        return duration > 0 ? this.getCurrentTime() / duration : 0;
    },

    getCurrentTime: function () {
        if (this.isPaused()) {
            return this.lastPause;
        }
        return this.lastStart + (this.ac.currentTime - this.startTime);
    }
};

WaveSurfer.util.extend(WaveSurfer.WebAudio, WaveSurfer.Observer);
