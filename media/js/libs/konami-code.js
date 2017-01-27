/* global define, module */

/**
 * Create Konami Code Sequence recognition « Up Up Bottom Bottom Left Right Left Right B A » on specific HTMLElement or on global HTMLDocument. Usage of finger is also possible with « Up Up Bottom Bottom Left Right Left Right Tap Tap ».
 * @class KonamiCode
 * @version 0.8.0
 * @author {@link https://www.lesieur.name/|Bruno Lesieur}
 * @param {Object|Function} [options]             - Container for all options. If type of `options` is Function, it is executed after Konami Code Sequence has been recognize.
 * @param {Function}        [options.callback]    - If `options` is not a Function, `options.callback` is executed after Konami Code Sequence has been entered. The first parameter provided by the callback is current instance of KonamiCode.
 * @param {Node}            [options.listener]    - By default it is the HTMLDocument `window.document`. You can pass some HTMLElement like `<input>` (HTMLInputElement) to only recognize Konami Code Sequence from this element.
 * @param {boolean}         [options.debug]       - By default it is set to `false`. When you set this value to `true`, that allows you to see all debug message in the console.
 */
(function (root, factory) {
    var initialClass = root.KonamiCode,
        api = root.KonamiCode = factory;

    /**
     * If a previous `KonamiCode` variable exist into global environment, you could kept it by changing name of current KonamiCode.
     * You can also just use that function to change the name of Global « KonamiCode » variable.
     * @function noConflict
     * @memberOf KonamiCode.
     * @example <script src="other/konami-code.js"></script>
     * <script src="last/konami-code.js"></script>
     * <script>
     *      var MyKC = KonamiCode.noConflict();
     *      console.log(KonamiCode); // Return the other KonamiCode
     *      console.log(MyKC); // Return your KonamiCode
     * </script>
     */
    api.noConflict = function () {
        root.KonamiCode = initialClass;
        return api;
    };

    if (typeof define === "function" && define.amd) {
        define(function () {
            return factory;
        });
    }

    if (typeof module === "object" && module.exports) {
        module.exports = factory;
    }
}(this, function callee(options) {
    var publics = this,
        privates = {},
        statics = callee;

    /**
     * Return the number of time KonamiCode was instanciated.
     * @function getNumberOfInstance
     * @memberOf KonamiCode.
     * @return {number} - Number of KonamiCode instance create from begining.
     */
    statics.getNumberOfInstance = function () {
        return statics._numberOfInstance;
    };

    /**
     * Active the listening of Konami Code Sequence.
     * @function enable
     * @memberOf KonamiCode#
     * @return {KonamiCode} Current instance of KonamiCode
     */
    publics.enable = function () {
        privates.listenCodeCharSequence();
        privates.listenCodeGestureSequence();
        privates.debug && privates.debug("Listener enabled for all.");

        return publics;
    };

    /**
     * Active the listening of Konami Code Sequence for Keyboard Keys.
     * @function enableKeyboardKeys
     * @memberOf KonamiCode#
     * @return {KonamiCode} Current instance of KonamiCode
     */
    publics.enableKeyboardKeys = function () {
        privates.listenCodeCharSequence();
        privates.debug && privates.debug("Listener enabled for Keyboard Keys.");

        return publics;
    };

    /**
     * Active the listening of Konami Code Sequence for Touch Gesture.
     * @function enableTouchGesture
     * @memberOf KonamiCode#
     * @return {KonamiCode} Current instance of KonamiCode
     */
    publics.enableTouchGesture = function () {
        privates.listenCodeGestureSequence();
        privates.debug && privates.debug("Listener enabled for Touch Gesture.");

        return publics;
    };

    /**
     * Unactive the listening of Konami Code Sequence.
     * @function disable
     * @memberOf KonamiCode#
     * @return {KonamiCode} Current instance of KonamiCode
     */
    publics.disable = function () {
        privates.stopCodeCharSequence();
        privates.stopCodeGestureSequence();
        privates.debug && privates.debug("Listener disabled for all.");

        return publics;
    };

    /**
     * Unactive the listening of Konami Code Sequence for Keyboard Keys.
     * @function disabledKeyboardKeys
     * @memberOf KonamiCode#
     * @return {KonamiCode} Current instance of KonamiCode
     */
    publics.disableKeyboardKeys = function () {
        privates.stopCodeCharSequence();
        privates.debug && privates.debug("Listener disabled for Keyboard Keys.");

        return publics;
    };

    /**
     * Unactive the listening of Konami Code Sequence for Touch Gesture.
     * @function disabledTouchGesture
     * @memberOf KonamiCode#
     * @return {KonamiCode} Current instance of KonamiCode
     */
    publics.disableTouchGesture = function () {
        privates.stopCodeGestureSequence();
        privates.debug && privates.debug("Listener disabled for Touch Gesture.");

        return publics;
    };

    /**
     * Change the listener. The old listener will no longer work. Note: change the listener enable this instance if it is previously disabled.
     * @function setListener
     * @param {Node} listener - You can pass some HTMLElement like `<input>` (HTMLInputElement) to only recognize Konami Code Sequence from this element.
     * @memberOf KonamiCode#
     * @return {KonamiCode} Current instance of KonamiCode
     */
    publics.setListener = function (listener) {
        privates.stopCodeCharSequence();
        privates.stopCodeGestureSequence();
        privates.listener = listener || document;
        privates.listenCodeCharSequence();
        privates.listenCodeGestureSequence();
        privates.debug && privates.debug("Listener changed.", listener);

        return publics;
    };

    /**
     * Change the Function executed after Konami Code Sequence has been entered.
     * @function setCallback
     * @param {Function} callback - Function executed after Konami Code Sequence has been entered. The first parameter provided by the callback is current instance of KonamiCode.
     * @memberOf KonamiCode#
     * @return {KonamiCode} Current instance of KonamiCode
     * @example new KonamiCode().setCallback(function (konamiCode) {
     *     konamiCode.disable();
     *     // Do something here.
     * });
     */
    publics.setCallback = function (callback) {
        privates.afterCodeSequenceCallback = (typeof callback === "function" && callback) || privates.defaultCallback;
        privates.debug && privates.debug("Callback changed.", callback);

        return publics;
    };

    /**
     * Change options of instance currently existing.
     * @function setOptions
     * @param {Object}   [options]          - Container for all options.
     * @param {Function} [options.callback] - Function executed after Konami Code Sequence has been entered. The first parameter provided by the callback is current instance of KonamiCode.
     * @param {Node}     [options.listener] - By default it is the HTMLDocument `window.document`. You can pass some HTMLElement like `<input>` (HTMLInputElement) to only recognize Konami Code Sequence from this element.
     * @param {boolean}  [options.debug]    - By default it is set to `false`. When you set this value to `true`, that allows you to see all debug message in the console.
     * @memberOf KonamiCode#
     * @return {KonamiCode} Current instance of KonamiCode
     */
    publics.setOptions = function (options) {
        privates.initOptions(options);

        return publics;
    };

    privates.keptLastCodeChar = function () {
        if (privates.input.length > privates.konamiCodeChar.length) {
            privates.input = privates.input.substr((privates.input.length - privates.konamiCodeChar.length));
        }
    };

    privates.defaultCallback = function () {
        privates.debug && privates.debug("Konami Code Sequence Entered. There is no action defined.");
    };

    privates.checkIfCodeCharIsValid = function () {
        if (privates.input === privates.konamiCodeChar) {
            privates.afterCodeSequenceCallback(publics);
        }
    };

    privates.codeSequenceEventKeyDown = function (event) {
        privates.input += event.keyCode;
        privates.keptLastCodeChar();
        privates.checkIfCodeCharIsValid();
    };

    privates.codeSequenceEventTouchMove = function (event) {
        var touch;
        if (event.touches.length === 1 && privates.capture === true) {
            touch = event.touches[0];
            privates.stopX = touch.pageX;
            privates.stopY = touch.pageY;
            privates.tap = false;
            privates.capture = false;
            privates.checkIfCodeGestureIsValid();
        }
    };

    privates.codeSequenceEventTouchEnd = function () {
        if (privates.tap === true) {
            privates.checkIfCodeGestureIsValid();
        }
    };

    privates.codeSequenceEventTouchStart = function (event) {
        privates.startX = event.changedTouches[0].pageX;
        privates.startY = event.changedTouches[0].pageY;
        privates.tap = true;
        privates.capture = true;
    };

    privates.stopCodeCharSequence = function () {
        privates.listener.removeEventListener("keydown", privates.codeSequenceEventKeyDown);
    };

    privates.stopCodeGestureSequence = function () {
        privates.listener.removeEventListener("touchstart", privates.codeSequenceEventTouchStart);
        privates.listener.removeEventListener("touchmove", privates.codeSequenceEventTouchMove);
        privates.listener.removeEventListener("touchend", privates.codeSequenceEventTouchEnd);
    };

    privates.listenCodeCharSequence = function () {
        privates.stopCodeCharSequence();
        privates.listener.addEventListener("keydown", privates.codeSequenceEventKeyDown);
    };

    privates.listenCodeGestureSequence = function () {
        privates.originalCodeGesture = privates.konamiCodeGesture;
        privates.stopCodeGestureSequence();
        privates.listener.addEventListener("touchstart", privates.codeSequenceEventTouchStart);
        privates.listener.addEventListener("touchmove", privates.codeSequenceEventTouchMove);
        privates.listener.addEventListener("touchend", privates.codeSequenceEventTouchEnd, false);
    };

    privates.checkIfCodeGestureIsValid = function () {
        var xMagnitude = Math.abs(privates.startX - privates.stopX),
            yMagnitude = Math.abs(privates.startY - privates.stopY),
            x = (privates.startX - privates.stopX < 0) ? "rt" : "lt",
            y = (privates.startY - privates.stopY < 0) ? "dn" : "up",
            result = (xMagnitude > yMagnitude) ? x : y;

        result = (privates.tap === true) ? "tp" : result;

        if (result === privates.konamiCodeGesture.substr(0, 2)) {
            privates.konamiCodeGesture = privates.konamiCodeGesture.substr(2, privates.konamiCodeGesture.length - 2);
        } else {
            privates.konamiCodeGesture = privates.originalCodeGesture;
        }

        if (privates.konamiCodeGesture.length === 0) {
            privates.konamiCodeGesture = privates.originalCodeGesture;
            privates.afterCodeSequenceCallback(publics);
        }
    };

    privates.checkDebugMode = function (options) {
        if (options && options.debug === true) {
            privates.debug = function (message, obj) {
                if (obj !== undefined) {
                    console.log(message, obj);
                } else {
                    console.log(message);
                }
            };
            privates.debug && privates.debug("Debug Mode On.");
        } else {
            privates.debug = false;
        }
    };

    privates.initOptions = function (options) {
        privates.checkDebugMode(options);
        privates.listener = (options && options.listener) || document;
        privates.afterCodeSequenceCallback =
            (typeof options === "function" && options) ||
            (options && typeof options.callback === "function" && options.callback) ||
            privates.defaultCallback;
    };

    privates.init = function () {
        privates.input = "";
        privates.konamiCodeChar = "38384040373937396665";
        privates.konamiCodeGesture = "upupdndnltrtltrttptp";
        privates.startX = 0;
        privates.startY = 0;
        privates.stopX = 0;
        privates.stopY = 0;
        privates.tap = false;
        privates.capture = false;
        statics._numberOfInstance = (statics._numberOfInstance) ? statics._numberOfInstance + 1 : 1;

        privates.initOptions(options);

        privates.listenCodeCharSequence();
        privates.listenCodeGestureSequence();
    };

    privates.init();
}));
