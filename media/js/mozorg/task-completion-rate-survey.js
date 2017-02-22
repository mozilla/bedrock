/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function () {
    var COOKIE_INTERACTION_ID = 'moz-task-completion-survey-interaction';
    var COOKIE_SHOWN_ID = 'moz-task-completion-survey-shown';
    var $survey = $('#survey-message');

    function showSurvey() {
        $survey.removeClass('hidden');
        setTimeout(function() {
            $survey.addClass('animate');
        }, 500);

        // Once survey is shown don't show it again for another 3 days.
        setCookie(COOKIE_SHOWN_ID, 3);
    }

    function hideSurvey(e) {
        e.preventDefault();
        $survey.addClass('hidden');
        onSurveyInteraction();
    }

    function getExpiryDate(days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        return date.toUTCString();
    }

    function setCookie(id, days) {
        Mozilla.Cookies.setItem(id, 'true', getExpiryDate(days));
    }

    function onSurveyInteraction() {
        // If visitor interacts with survey, don't show it again.
        // Assuming the survey will be taken down within 30 days.
        setCookie(COOKIE_INTERACTION_ID, 30);
    }

    function onSurveyClick(e) {
        if (e.metaKey || e.ctrlKey) {
            $survey.addClass('hidden');
            onSurveyInteraction();
        } else {
            e.preventDefault();
            onSurveyInteraction();
            window.location = e.target.href;
        }
    }

    function bindEvents() {
        $survey.find('.survey-button').one('click', onSurveyClick);
        $survey.find('.survey-button-close').one('click', hideSurvey);
    }

    function setParams() {
        var $surveyButton = $survey.find('.survey-button');
        var surveyURL = $surveyButton.attr('href');
        var path = encodeURIComponent(window.location.pathname);
        var surveyLink = surveyURL + '?' + '&p=' + path;
        $surveyButton.attr('href', surveyLink);
    }

    /**
     * Task completion rate surevey (bug 1341425).
     */
    if ($survey.length) {

        if (typeof Mozilla.Cookies === 'undefined' || !Mozilla.Cookies.enabled()) {
            return;
        }

        if (Mozilla.Cookies.getItem(COOKIE_INTERACTION_ID) === 'true' || Mozilla.Cookies.getItem(COOKIE_SHOWN_ID) === 'true') {
            return;
        }

        setParams();
        showSurvey();
        bindEvents();
    }
});
