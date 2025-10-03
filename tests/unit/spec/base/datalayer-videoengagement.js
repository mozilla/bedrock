/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import VideoEngagement from '../../../../media/js/base/datalayer-videoengagement.es6.js';

describe('datalayer-videoengagement.es6.js', function () {
    const gaEventNames = ['video_start', 'video_progress', 'video_complete'];
    const videoTitle = 'Test';
    const videoUrl = 'https://assets.mozilla.net/video/test.webm';
    const videoProvider = 'self-hosted';
    const videoVisible = true;
    const videoDuration = 100;
    const percentage10 = 10;
    const percentage25 = 25;
    const percentage50 = 50;
    const percentage75 = 75;
    const percentage100 = 100;

    const expectedEventStart = {
        event: gaEventNames[0],
        visible: videoVisible,
        video_duration: videoDuration,
        video_title: videoTitle,
        video_url: videoUrl,
        video_provider: videoProvider,
        video_current_time: 0,
        video_percent: 0
    };

    const expectedEventProgress = {
        event: gaEventNames[1],
        visible: videoVisible,
        video_duration: videoDuration,
        video_title: videoTitle,
        video_url: videoUrl,
        video_provider: videoProvider,
        video_current_time: 10,
        video_percent: percentage10
    };

    const expectedEventComplete = {
        event: gaEventNames[2],
        visible: videoVisible,
        video_duration: videoDuration,
        video_title: videoTitle,
        video_url: videoUrl,
        video_provider: videoProvider,
        video_current_time: videoDuration,
        video_percent: percentage100
    };

    beforeEach(function () {
        window.dataLayer = [];
        VideoEngagement.duration = videoDuration;
    });

    afterEach(function () {
        delete window.dataLayer;
        VideoEngagement.duration = null;
    });

    it('calculates percentage completed correctly', function () {
        expect(
            VideoEngagement.getPercentageComplete(percentage10) ===
                VideoEngagement.progressThresholds[0]
        ).toBeTruthy();
        expect(
            VideoEngagement.getPercentageComplete(percentage25) ===
                VideoEngagement.progressThresholds[1]
        ).toBeTruthy();
        expect(
            VideoEngagement.getPercentageComplete(percentage50) ===
                VideoEngagement.progressThresholds[2]
        ).toBeTruthy();
        expect(
            VideoEngagement.getPercentageComplete(percentage75) ===
                VideoEngagement.progressThresholds[3]
        ).toBeTruthy();
        expect(
            VideoEngagement.getPercentageComplete(percentage100) === 100
        ).toBeTruthy();
    });

    it('correctly identifies when multiple progress thresholds have been passed', function () {
        spyOn(VideoEngagement, 'getPercentageComplete').and.returnValue(
            percentage50
        );
        const passedThresholds =
            VideoEngagement.getPassedThresholds(percentage50);
        expect(passedThresholds.length).toBe(3);
    });

    it('will append the start event to the dataLayer', function () {
        VideoEngagement.sendEvent(expectedEventStart);
        expect(window.dataLayer[0]['event'] === 'video_start').toBeTruthy();
    });

    it('will append the progress event to the dataLayer', function () {
        VideoEngagement.sendEvent(expectedEventProgress);
        expect(window.dataLayer[0]['event'] === 'video_progress').toBeTruthy();
    });

    it('will append the complete event to the dataLayer', function () {
        VideoEngagement.sendEvent(expectedEventComplete);
        expect(window.dataLayer[0]['event'] === 'video_complete').toBeTruthy();
    });

    describe('handleProgress', () => {
        let mockEvent, sendEventSpy;

        beforeEach(() => {
            mockEvent = {
                target: {
                    currentTime: 0,
                    hasAttribute: jasmine.createSpy('hasAttribute'),
                    getAttribute: jasmine.createSpy('getAttribute'),
                    setAttribute: jasmine.createSpy('setAttribute'),
                    removeEventListener: jasmine.createSpy(
                        'removeEventListener'
                    )
                }
            };

            sendEventSpy = spyOn(VideoEngagement, 'sendEvent');
        });

        it('should call sendEvent with "video_progress" when video is in progress', () => {
            mockEvent.target.currentTime = 50;
            mockEvent.target.hasAttribute.and.returnValue(true);
            mockEvent.target.getAttribute.and.returnValue('25');

            VideoEngagement.handleProgress(mockEvent);

            expect(sendEventSpy).toHaveBeenCalledWith({
                event: 'video_progress',
                currentTime: 50,
                percent: 50
            });
            expect(mockEvent.target.setAttribute).toHaveBeenCalledWith(
                'data-ga-threshold',
                50
            );
        });

        it('should call sendEvent with "video_complete" when video is complete', () => {
            mockEvent.target.currentTime = 100;
            mockEvent.target.hasAttribute.and.returnValue(true);
            mockEvent.target.getAttribute.and.returnValue('75');

            VideoEngagement.handleProgress(mockEvent);

            expect(sendEventSpy).toHaveBeenCalledWith({
                event: 'video_complete',
                currentTime: 100,
                percent: 100
            });
            expect(mockEvent.target.removeEventListener).toHaveBeenCalled();
        });

        it('should call sendEvent with "video_complete" when video has looped', () => {
            mockEvent.target.currentTime = 10;
            mockEvent.target.hasAttribute.and.returnValue(true);
            mockEvent.target.getAttribute.and.returnValue('75');

            VideoEngagement.handleProgress(mockEvent);

            expect(sendEventSpy).toHaveBeenCalledWith({
                event: 'video_complete',
                currentTime: 100,
                percent: 100
            });
            expect(mockEvent.target.removeEventListener).toHaveBeenCalled();
        });

        it('should not call sendEvent when no new threshold is passed', () => {
            mockEvent.target.currentTime = 30;
            mockEvent.target.hasAttribute.and.returnValue(true);
            mockEvent.target.getAttribute.and.returnValue('25');

            VideoEngagement.handleProgress(mockEvent);

            expect(sendEventSpy).not.toHaveBeenCalled();
        });
    });
});
