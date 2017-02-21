/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global L */

(function($) {
    'use strict';

    var wideMode = true;

    var map = null;
    var xhr = null;
    var initContentId = null;
    var initialTabStateId = null;
    var contentCache = []; // page content cache
    var titleCache = []; // page title cache

    // Community Layers
    var northAmerica;
    var latinAmerica;
    var europe;
    var asiaSouthPacific;
    var antarctica;
    var africaMiddleEast;
    var balkans;
    var hispano;
    var francophone;
    var arabic;
    var communityLayers;
    var layers = {};

    var mozMap = {
        /*
         * Initialize mapbox and set default control values.
         * This should only be called once on page load.
         */
        init: function () {
            var $main = $('#main-content');
            // get the mapbox map id.
            var mapId = $main.data('mapbox');
            // touch support detection.
            var hasTouch = L.Browser.touch || L.Browser.msTouch;
            // mapbox access token
            L.mapbox.accessToken = $main.data('token');
            // set page nav state.
            mozMap.setInitialPageNavState();
            // create mobile navigation
            mozMap.initMobileNav();
            // init screen resize handler
            mozMap.initResizeHandler();
            //initialize map and center.
            map = L.mapbox.map('map', mapId).setView([28, 0], 2);
            // disable map zoom on scroll.
            map.scrollWheelZoom.disable();
            // create spaces markers.
            mozMap.initSpacesMarkers();
            // create community layers.
            mozMap.initCommunityLayers();
            // set the map state (i.e. spaces or communities)
            mozMap.setMapState();
            // store reference to the initial map content
            mozMap.setInitialContentState();
            // bind events on tab navigation.
            mozMap.bindTabNavigation();
            // init history.js.
            mozMap.bindHistory();
            // disable dragging for touch devices.
            if (hasTouch) {
                // disable drag and zoom handlers.
                map.dragging.disable();
                map.touchZoom.disable();
                map.doubleClickZoom.disable();
                // disable tap handler, if present.
                if (map.tap) {
                    map.tap.disable();
                }
            }

            mozMap.checkForHash();

            // init photo galleries using event delegation
            $('#page-content').magnificPopup({
                delegate: '.gallery-list a',
                gallery: { enabled: true },
                type: 'image'
            });

            // init HTML5 video poster helper
            var video = new Mozilla.VideoPosterHelper('#page-content');
            video.init();
        },

        /*
         * Sets the initial active tab and nav items on page load
         * using the id and data-tab attribute of the entry section element
         */
        setInitialPageNavState: function () {
            var $entry = $('#entry-container .entry');
            var tab = $entry.data('tab');
            var id = $entry.prop('id');

            //set the current tab navigation item
            $('ul.category-tabs li[data-id="' + tab + '"]').addClass('current');
            $('.nav-category li[data-id="' + id + '"]').addClass('current');

            if (tab === 'communities') {
                // hide the community sub menu's
                $('#nav-communities .submenu').hide();
                mozMap.toggleCommunitySubMenu();
            }
        },

        /*
         * Initialize history.js for pushState support
         */
        bindHistory: function () {
            // Bind to statechange event. Note: We are using statechange instead of popstate
            History.Adapter.bind(window, 'statechange', function () {
                // Note: We are using History.getState() instead of event.state
                var state = History.getState();
                var current = mozMap.getMapState();

                // check if we need to change the map state
                if (state.data.tab && current !== state.data.tab) {
                    mozMap.updateTabState(state.data.tab);
                    mozMap.setMapState();
                }

                if (state.data.tab && state.data.tab === 'spaces') {
                    // Hide community nav+meta and show spaces nav+meta
                    mozMap.toggleNav('spaces');
                    mozMap.toggleMobileNav('spaces');
                    // Update current nav item to the active space
                    mozMap.updateSpaceNavItem(state.data.id);
                    // Show the space based on event state url
                    mozMap.showSpace(state.url, state.data.id);

                } else if (state.data.tab && state.data.tab === 'communities') {
                    // Hide spaces nav+meta and show community nav+meta
                    mozMap.toggleNav('communities');
                    mozMap.toggleMobileNav('communities');
                    // Update community region on the map
                    mozMap.updateCommunityNavItem(state.data.id);
                    mozMap.showCommunityContent(state.url, state.data.id);

                } else if (state.data.tab && state.data.tab === 'contact') {
                    // Hide spaces and community nav+meta
                    mozMap.toggleNav('contact');
                    mozMap.toggleMobileNav('contact');
                    mozMap.showContactUsContent(state.url, state.data.id);

                } else {
                    // if state.data.tab is undefined we must be on our
                    // first history item when the page loaded
                    if (initialTabStateId === 'contact') {
                        mozMap.updateTabState(initialTabStateId);
                        mozMap.setMapState();
                        mozMap.showContactUsContent(null, initContentId);

                    } else if (initialTabStateId === 'spaces') {
                        mozMap.toggleNav('spaces');
                        mozMap.updateSpaceNavItem(initContentId);
                        mozMap.showSpace(null, initContentId);

                    } else if (initialTabStateId === 'communities') {
                        mozMap.toggleNav('communities');
                        mozMap.updateCommunityNavItem(initContentId);
                        mozMap.showCommunityContent(null, initContentId);
                    }
                }

                // close any photo galleries that may have been open
                $.magnificPopup.close();
            });

            // If pushState is emulated (html4 browsers) and we have a hash (a '#' in the url)
            // trigger the statechange event
            if (History.emulated.pushState && History.getHash()) {
                $(document).ready(function() {
                    History.Adapter.trigger(window, 'statechange');
                });
            }
        },

        /*
         * Generate nav dropdown from list
         */
        initMobileNav: function () {
            var id = $('#entry-container .entry').prop('id');
            var utils = Mozilla.Utils;
            // Create select form inputs for primary mobile navigation
            $('.nav-category').each(function() {
                var $this = $(this);
                var tab = $this.find('ul').data('tab');
                var $select = $('<select class="nav-category-select">').prependTo('#page-content');
                $('<option value="" disabled selected>-- ' + utils.trans('nav-' + tab) + ' --</option>').prependTo($select);
                $this.find('li').each(function() {
                    var $li = $(this),
                        $a = $li.find('> a'),
                        $p = $li.parents('li'),
                        prefix = new Array($p.length + 1).join('-');

                    $('<option>').text(prefix + ' ' + $a.text())
                        .val($(this).data('id'))
                        .appendTo($select);
                });
                $select.prop('id', $(this).prop('id') + '-select');
            });

            // Set the selected item in the mobile nav option menu
            mozMap.setSelectedMobileNavItem(id);
        },

        /*
         * Bind the change event on mobile form navigation
         */
        bindMobileNavChange: function () {
            $('.nav-category-select').on('change', mozMap.onMobileNavChange);
        },

        /*
         * Unbind the change event on mobile form navigation
         */
        unBindMobileNavChange: function () {
            $('.nav-category-select').off('change', mozMap.onMobileNavChange);
        },

        /*
         * Called when mobile nav change event is fired
         * Here we just find the right item in the menu and trigger a click
         * which in turn handles all the push state itself
         */
        onMobileNavChange: function () {
            $('.nav-category li[data-id="' + $(this).val() + '"] > a').trigger('click');
        },

        /*
         * Initializes resize handler for browsers that support matchMedia
         */
        initResizeHandler: function () {
            var hasMediaQueries = (typeof matchMedia !== 'undefined');
            // If the browser supports media queries, check the width onload and onresize.
            if (hasMediaQueries) {
                mozMap.checkScreenSize();
                $(window).on('resize', function() {
                    clearTimeout(this.resizeTimeout);
                    this.resizeTimeout = setTimeout(mozMap.checkScreenSize, 200);
                });
            } else {
                // else just show the desktop nav
                $('.nav-category-select').hide();
                mozMap.toggleNav(mozMap.getMapState());
            }
        },

        /*
         * Sets the current mobile navigation option
         * Param: @id string space/community identifier
         */
        setSelectedMobileNavItem: function (id) {
            var state = mozMap.getMapState();
            // unbind change listener
            mozMap.unBindMobileNavChange();
            // update the selected item
            if (state === 'spaces' && id !== 'spaces') {
                $('#nav-spaces-select').find('option:selected').prop('selected', false);
                $('#nav-spaces-select option[value="' + id + '"]').prop('selected', 'selected');
            } else if (state === 'communities' && id !== 'communities') {
                $('#nav-communities-select').find('option:selected').prop('selected', false);
                $('#nav-communities-select option[value="' + id + '"]').prop('selected', 'selected');
            } else {
                $('#nav-communities-select').find('option:selected').prop('selected', false);
                $('#nav-spaces-select').find('option:selected').prop('selected', false);
                $('.nav-category-select option[disabled]').prop('selected', 'selected');
            }
            // rebind change listener
            mozMap.bindMobileNavChange();
        },

        /*
         * Checks the screen size and toggles navigation state
         * Called on window 'resize' event
         */
        checkScreenSize: function () {
            var state = mozMap.getMapState();
            if (window.matchMedia('screen and (min-width: 761px)').matches) {
                wideMode = true;
                $('.nav-category-select').hide();
                mozMap.toggleNav(state);
            } else {
                wideMode = false;
                $('.nav-category').hide();
                mozMap.toggleMobileNav(state);
            }
        },

        /*
         * Toggles the active tab nav menu visibility
         */
        toggleNav: function (tab) {
            if (tab === 'spaces' && wideMode) {
                $('#nav-communities, #meta-communities').fadeOut(100, function () {
                    $('#nav-spaces, #meta-spaces').show();
                });
            } else if (tab === 'communities' && wideMode) {
                $('#nav-spaces, #meta-spaces').fadeOut(100, function () {
                    $('#nav-communities, #meta-communities').show();
                });
            } else if (tab === 'contact' && wideMode) {
                $('#nav-spaces, #meta-spaces, #nav-communities, #meta-communities').fadeOut(100);
            }
        },

        toggleMobileNav: function (tab) {
            if (tab === 'spaces' && !wideMode) {
                $('#nav-spaces-select, #meta-spaces').show();
                $('#nav-communities-select, #meta-communities').hide();
            } else if (tab === 'communities' && !wideMode) {
                $('#nav-spaces-select, #meta-spaces').hide();
                $('#nav-communities-select, #meta-communities').show();
            } else if (tab === 'contact'&& !wideMode) {
                $('#nav-communities-select, #meta-communities, #nav-spaces-select, #meta-spaces').hide();
            }
        },

        /*
         * Toggles the active community submenu nav
         */
        toggleCommunitySubMenu: function () {
            var $current = $('#nav-communities li.current');
            var $parent = $current.parent();

            // if current item has a sub-menu which isn't open
            if ($current.hasClass('hasmenu') && !$current.hasClass('open')) {
                $('.accordion .submenu:visible').slideUp().parent().removeClass('open');
                $current.addClass('open');
                $current.find('.submenu').slideDown();
            }

            // if current item is within a sub-menu and it's parent is not open
            if ($parent.hasClass('submenu') && !$parent.is(':visible')) {
                $('.accordion .submenu:visible').slideUp().parent().removeClass('open');
                $parent.slideDown().parent().addClass('open');
            }

            // if neither current item or it's parent has no sub-menu
            if  (!$current.hasClass('hasmenu') && !$parent.hasClass('submenu')) {
                $('.accordion .submenu:visible').slideUp().parent().removeClass('open');
            }

            if (wideMode) {
                mozMap.scrollToContent();
            }
        },

        /*
         * if user has scrolled past the map, autoscroll to the top of the content
         */
        scrollToContent: function () {
            var contentOffset = $('#page-content').offset().top;
            if ($(window).scrollTop() > contentOffset) {
                $('html, body').animate({
                    scrollTop: contentOffset
                }, 500);
            }
        },

        /*
         * Bind the main tab navigation for toggling spaces
         * and communities. Only needs to be called once
         */
        bindTabNavigation: function () {
            $('.category-tabs li a').on('click', mozMap.onTabNavigationClick);
        },

        /*
         * When tab navigation is clicked we need to do push state
         */
        onTabNavigationClick: function (e) {
            e.preventDefault();
            var itemId = $(this).parent().data('id');
            var itemUrl = this.href;

            // Push the new url and update browser history
            History.pushState({
                id: itemId,
                tab: itemId
            }, document.title, itemUrl);
        },

        /*
         * Stores initial content id and tab id on page load
         */
        setInitialContentState: function () {
            // store initial content data id on page load
            var state = mozMap.getMapState();

            if (state === 'spaces') {
                initContentId = $('#nav-spaces li.current').data('id');

                // if we land directly on a specific space, like Mountain View,
                // pan the marker to that space.
                if (initContentId) {
                    mozMap.panToMarker(initContentId);
                }

                // Show spaces nav+meta
                if (wideMode) {
                    $('#nav-spaces, #meta-spaces').show();
                } else {
                    $('#nav-spaces-select, #meta-spaces').show();
                }
            } else if (state === 'communities') {
                initContentId = $('#nav-communities li.current').data('id');

                var region = initContentId ? initContentId : 'communities';
                mozMap.showCommunityRegion(region);

                // Show community nav+meta
                if (wideMode) {
                    $('#nav-communities, #meta-communities').show();
                } else {
                    $('#nav-communities-select, #meta-communities').show();
                }
            } else if (state === 'contact') {
                initContentId = $('.category-tabs li.current').data('id');
            }
            //store ref to initial tab state
            initialTabStateId = state;
        },

        /*
         * Get the current map state
         * Return values are either 'spaces' or 'communities'
         */
        getMapState: function () {
            return $('ul.category-tabs li.current').data('id');
        },

        /*
         * Sets the map state based on the active category tab.
         * Determined using data-id attribute and .current list item.
         */
        setMapState: function () {
            var state = mozMap.getMapState();
            if (state === 'spaces') {
                //clear commuity layers
                mozMap.clearCommunityLayers();
                // unbind click events on community nav
                mozMap.unbindCommunityNav();
                // add spaces marker layer.
                mozMap.addSpacesMarkers();
                // bind click events on spaces nav
                mozMap.bindSpacesNav();
                // hide community legend
                mozMap.hideMapLegend();
            } else if (state === 'communities') {
                // remove spaces markers
                mozMap.removeSpacesMarkers();
                // unbind click events on spaces nav
                mozMap.unbindSpacesNav();
                // bind click events on community nav
                mozMap.bindCommunityNav();
                // hide community legend
                mozMap.showMapLegend();
            } else if (state === 'contact') {
                //clear commuity layers
                mozMap.clearCommunityLayers();
                // unbind click events on community nav
                mozMap.unbindCommunityNav();
                // unbind click events on spaces nav
                mozMap.unbindSpacesNav();
                // add spaces marker layer.
                mozMap.addSpacesMarkers();
                // hide community legend
                mozMap.hideMapLegend();
            }
        },

        /*
         * Creates spaces markers and then hide them using setFilter()
         */
        initSpacesMarkers: function () {
            map.featureLayer.on('layeradd', function(e) {
                var marker = e.layer,
                    feature = marker.feature;

                marker.setIcon(L.icon(feature.properties.icon));
            });
            map.featureLayer.setGeoJSON(window.mozSpaces);
            map.featureLayer.setFilter(function () {
                return false;
            });
        },

        /*
         * Creates a marker layer for office spaces and binds events.
         * Sets an initial panned out view of the world map.
         */
        addSpacesMarkers: function () {
            map.featureLayer.setFilter(function () {
                return true;
            });
            map.featureLayer.on('click', mozMap.onMarkerClick);
            map.featureLayer.on('mouseover', mozMap.openMarkerPopup);
            map.featureLayer.on('mouseout', mozMap.closeMarkerPopup);
        },

        /*
         * Removes spaces markers from the map and unbinds events.
         */
        removeSpacesMarkers: function () {
            map.featureLayer.setFilter(function () {
                return false;
            });
            map.featureLayer.off('click', mozMap.onMarkerClick);
            map.featureLayer.off('mouseover', mozMap.openMarkerPopup);
            map.featureLayer.off('mouseout', mozMap.closeMarkerPopup);
            map.setView([28, 0], 2);
        },

        /*
         * Creates a custom marker popup with localized text from template nav
         */
        openMarkerPopup: function (e) {
            var id = e.layer.feature.properties.id;
            var $name = $('#nav-spaces li[data-id="' + id + '"]').text();

            e.layer.bindPopup($name, {
                closeButton: false,
                maxWidth: 300
            });

            e.layer.openPopup();
        },

        /*
         * Closes and unbinds the popup
         */
        closeMarkerPopup: function (e) {
            e.layer.closePopup();
            e.layer.unbindPopup();
        },

        /*
         * Programatically pan to a given marker
         * Param: @id marker string identifier
         */
        panToMarker: function (id) {
            // if we're on the landing page zoom out to show all markers.
            if (id === 'spaces' || id === 'contact') {
                map.setView([28, 0], 2);
                return;
            }
            // else find the right marker and fire a click.
            map.featureLayer.eachLayer(function (marker) {
                if (marker.feature.properties.id === id) {
                    map.setView(marker.getLatLng(), 12, {
                        animate: true
                    });
                    return;
                }
            });
        },

        /*
         * Bind click events on spaces navigation menu.
         */
        bindSpacesNav: function () {
            $('#nav-spaces li a').on('click', mozMap.onSpacesNavClick);
        },

        /*
         * Unbind click events on spaces navigation menu.
         */
        unbindSpacesNav: function () {
            $('#nav-spaces li a').off('click', mozMap.onSpacesNavClick);
        },

        /*
         * Bind events on top level community navigation menu
         */
        bindCommunityNav: function () {
            $('#nav-communities li > a').on('click', mozMap.onCommunityNavClick);
        },

        /*
         * Unbind events on top level community navigation menu
         */
        unbindCommunityNav: function () {
            $('#nav-communities li > a').off('click', mozMap.onCommunityNavClick);
        },

        /*
         * Update current spaces nav item and then show the space
         */
        onSpacesNavClick: function (e) {
            e.preventDefault();
            var itemId = $(this).parent().data('id');
            var tabId = 'spaces';
            History.pushState({
                id: itemId,
                tab: tabId
            }, document.title, this.href);
        },

        /*
         * Update top level community nav item and show the region layer
         */
        onCommunityNavClick: function (e) {
            e.preventDefault();
            var $current = $(this).parent();
            var itemId = $current.data('id');
            var tabId = 'communities';

            if (!$current.hasClass('current')) {
                History.pushState({
                    id: itemId,
                    tab: tabId
                }, document.title, this.href);
                return;
            }

            // allow the current selected nav to toggle when clicked
            if ($current.hasClass('hasmenu') && !$current.hasClass('open')) {
                $('.accordion .submenu:visible').slideUp().parent().removeClass('open');
                $current.addClass('open');
                $current.find('.submenu').slideDown();
            } else if ($current.hasClass('hasmenu') && $current.hasClass('open')) {
                $('.accordion .submenu:visible').slideUp().parent().removeClass('open');
                $current.removeClass('open');
            }
        },

        /*
         * Clears all community map layers
         */
        clearCommunityLayers: function () {
            communityLayers.clearLayers();
        },

        /*
         * Updates the spaces navigation current ite,
         * Param: @id space string identifier
         */
        updateSpaceNavItem: function (id) {
            // return if the tab navigation has been clicked,
            // as we just want to show the landing page
            if (id === 'spaces') {
                $('#nav-spaces li.current').removeClass('current');
                mozMap.setSelectedMobileNavItem(id);
                return;
            }

            $('#nav-spaces li.current').removeClass('current');
            $('#nav-spaces li[data-id="' + id + '"]').addClass('current');

            mozMap.setSelectedMobileNavItem(id);

            if (wideMode) {
                mozMap.scrollToContent();
            }
        },

        /*
         * Updates the spaces navigation current ite,
         * Param: @id space string identifier
         */
        updateCommunityNavItem: function (id) {
            // return if the tab navigation has been clicked,
            // as we just want to show the landing page
            if (id === 'communities') {
                $('#nav-communities li.current').removeClass('current');
                // hide the community sub menu's
                $('.accordion .submenu').hide();
                $('#nav-communities li.open').removeClass('open');
                mozMap.setSelectedMobileNavItem(id);
                return;
            }

            $('#nav-communities li.current').removeClass('current');
            $('#nav-communities li[data-id="' + id + '"]').addClass('current');

            mozMap.setSelectedMobileNavItem(id);
            mozMap.toggleCommunitySubMenu();
        },

        /*
         * Show all community layers on the map at once
         */
        showAllCommunityLayers: function () {
            mozMap.clearCommunityLayers();
            communityLayers.addLayer(northAmerica);
            communityLayers.addLayer(latinAmerica);
            communityLayers.addLayer(europe);
            communityLayers.addLayer(asiaSouthPacific);
            communityLayers.addLayer(antarctica);
            communityLayers.addLayer(africaMiddleEast);
            map.setView([28, 0], 2);
        },

        /*
         * Updates the current active tab and then updates the map state.
         * Param: @tab tab string identifier (e.g. 'spaces', 'communities' or 'contact').
         */
        updateTabState: function (tab) {
            $('ul.category-tabs li.current').removeClass('current');
            $('ul.category-tabs li[data-id="' + tab + '"]').addClass('current');
            //remove current sub menu class as we're going to a landing page
            $('.nav-category li.current').removeClass('current');
            // hide the community sub menu's
            $('.accordion .submenu').hide();
            $('.accordion .hasmenu').removeClass('open');
        },

        /*
         * Focuses map on the marker and shows a popup tooltip
         */
        onMarkerClick: function (e) {
            var $itemId = $('#nav-spaces li.current').data('id');
            var markerId = e.layer.feature.properties.id;

            // if the user clicks on a marker that is not related to the current space
            // we need to do push state to update the page content.
            if (markerId !== $itemId) {
                var url = $('#nav-spaces li[data-id="' + markerId + '"] a').prop('href');
                History.pushState({
                    id: markerId,
                    tab: 'spaces'
                }, document.title, url);
                return;
            }
        },

        /*
         * Show the current active space information.
         * Determined using data-id attribute and .current list item.
         */
        showSpace: function (url, cacheId) {
            var current = $('#nav-spaces li.current');
            // get the current space id and href based on the nav
            var id = current.data('id');
            var contentUrl = url || current.prop('href');

            // if the content is already cached display it
            if (contentCache.hasOwnProperty(cacheId)) {
                // abort any pending xhr if we're loading from cache
                mozMap.abortRequest();
                $('#entry-container').html(contentCache[cacheId]);
                // pan to the new marker
                mozMap.panToMarker(cacheId);
                // update the page title
                mozMap.setPageTitle(cacheId);
            } else if (id && id === $('section.entry').prop('id')) {
                // pan to the new marker
                mozMap.panToMarker(id);
            } else {
                $('#entry-container').empty();
                // request content via ajax
                mozMap.requestContent(contentUrl);
            }
        },

        /*
         * Toggles community layers on the map
         * Params: @id string region identifier
         */
        showCommunityRegion: function (id) {
            var region = id;
            var $nav = $('#nav-communities li.current').parent();

            if ($nav.hasClass('submenu')) {
                region = $nav.parent().data('id');
            }

            if (region === 'communities') {
                mozMap.showAllCommunityLayers();
                mozMap.highlightLegend();
                return;
            }

            // if the layer exists clear the map and add it.
            if (layers.hasOwnProperty(region)) {
                mozMap.clearCommunityLayers();
                mozMap.fitRegionToLayer(region);
                // mapbox needs a small timeout after zooming
                // the region before adding the community layer
                setTimeout(function () {
                    communityLayers.addLayer(layers[region]);
                }, 50);
            }

            mozMap.highlightLegend(region);
        },

        /*
         * Show the contact us page content.
         * Determined using data-id attribute and .current list item.
         */
        showContactUsContent: function(url, cacheId) {
            var $current = $('.category-tabs li.current');
            var contentUrl = url || $current.prop('href');
            var $entryContainer = $('#entry-container');

            $('#nav-spaces, #nav-communities, #meta-spaces, #meta-communities').hide();

            if (contentCache.hasOwnProperty(cacheId)) {
                // abort any pending xhr if we're loading from cache
                mozMap.abortRequest();
                // if the content is already cached display it
                $entryContainer.html(contentCache[cacheId]);
                // update the page title
                mozMap.setPageTitle(cacheId);
                // this reuses the spaces view
                mozMap.panToMarker('contact');
            } else {
                $entryContainer.empty();
                // request content via ajax
                mozMap.requestContent(contentUrl);
            }
        },

        /*
         * Show the current active community information.
         * Determined using data-id attribute and .current list item.
         */
        showCommunityContent: function (url, cacheId) {
            var current = $('#nav-communities li.current');
            // get the current space id and href based on the nav
            var id = current.data('id');
            var contentUrl = url || current.prop('href');

            if (contentCache.hasOwnProperty(cacheId)) {
                // abort any pending xhr if we're loading from cache
                mozMap.abortRequest();
                // if the content is already cached display it
                $('#entry-container').html(contentCache[cacheId]);
                mozMap.showCommunityRegion(cacheId);
                // update the page title
                mozMap.setPageTitle(cacheId);
            } else if (id && id === $('section.entry').prop('id')) {
                // if we're already on the right page,
                // just show the map layer
                mozMap.showCommunityRegion(id);
            } else {
                $('#entry-container').empty();
                // request content via ajax
                mozMap.requestContent(contentUrl);
            }
        },

        fitRegionToLayer: function (id) {
            switch(id) {
            case 'north-america':
                map.setView([65, -110], 2);
                break;
            case 'latin-america':
                map.setView([-20, -80], 2);
                break;
            case 'europe':
                map.setView([50, 20], 3);
                break;
            case 'asia':
                map.setView([25, 100], 2);
                break;
            case 'antarctica':
                map.setView([-40, 0], 1);
                break;
            case 'africa':
                map.setView([10, 10], 3);
                break;
            case 'francophone':
                map.setView([40, -20], 2);
                break;
            case 'hispano':
                map.setView([-10, -40], 2);
                break;
            case 'arabic':
                map.setView([20, 10], 2);
                break;
            case 'balkans':
                map.setView([50, 20], 3);
            }
        },

        highlightLegend: function (id) {
            var $current = $('#map .legend li[data-id="' + id + '"] a');
            $('.legend li a.active').removeClass('active');
            if ($current.length > 0) {
                $current.addClass('active');
            }
        },

        /*
         * Initializes geo-json community layers ready for drawing
         */
        initCommunityLayers: function () {

            // create each geoJson layer
            northAmerica = L.geoJson(window.mozNorthAmerica, {
                style: mozMap.styleLayer('#5cb6e0')
            });
            latinAmerica = L.geoJson(window.mozLatinAmerica, {
                style: mozMap.styleLayer('#f36261')
            });
            europe = L.geoJson(window.mozEurope, {
                style: mozMap.styleLayer('#7dc879')
            });
            asiaSouthPacific = L.geoJson(window.mozAsiaSouthPacific, {
                style: mozMap.styleLayer('#c883c5')
            });
            antarctica = L.geoJson(window.mozAntarctica, {
                style: mozMap.styleLayer('#a1b2b7')
            });
            africaMiddleEast = L.geoJson(window.mozAfricaMiddleEast, {
                style: mozMap.styleLayer('#eb936e')
            });
            hispano = L.geoJson(window.mozHispano, {
                style: mozMap.styleLayer('white', '#c71929', 0.1, 'none', 2)
            });
            francophone = L.geoJson(window.mozFrancophone, {
                style: mozMap.styleLayer('white', '#3b9bc5', 0.1, 'none', 2)
            });
            arabic = L.geoJson(window.mozArabic, {
                style: mozMap.styleLayer('white', '#f79937', 0.1, 'none', 2)
            });
            balkans = L.geoJson(window.mozBalkans, {
                style: mozMap.styleLayer('white', '#7022a8', 0.1, 'none', 2)
            });

            // create an empty layer group and add it to the map
            communityLayers = new L.FeatureGroup();
            communityLayers.addTo(map);

            // Store a lookup key for each layer object
            layers = {
                'north-america': northAmerica,
                'latin-america': latinAmerica,
                'europe': europe,
                'asia': asiaSouthPacific,
                'antarctica': antarctica,
                'africa': africaMiddleEast,
                'hispano': hispano,
                'francophone': francophone,
                'arabic': arabic,
                'balkans': balkans
            };
        },

        /*
         * Styles a geo-json community layer
         */
        styleLayer: function (fill, outline, opacity, dash, weight) {
            return {
                fillColor: fill,
                weight: weight || 1,
                opacity: 1,
                color: outline || 'white',
                fillOpacity: opacity || 0.7,
                dashArray: dash || 'none',
                clickable: false
            };
        },

        /*
         * Shows the community map legend and bind click events
         */
        showMapLegend: function () {
            var $legend = $('#map .legend');
            $legend.fadeIn('fast');
            $legend.on('click', 'li a', mozMap.onMapLegendClick);
        },

        /*
         * Hides the community map legend and unbind click events
         */
        hideMapLegend: function () {
            var $legend = $('#map .legend');
            $legend.fadeOut('fast');
            $legend.off('click', 'li a', mozMap.onMapLegendClick);
        },

        /*
         * Find the corresponding nav item based on data-id in the legend
         * and call push state to update the page content
         */
        onMapLegendClick: function (e) {
            e.preventDefault();
            var itemId = $(this).parent().data('id');
            var tabId = 'communities';

            History.pushState({
                id: itemId,
                tab: tabId
            }, document.title, this.href);
        },

        /*
         * Sets the page title from cache
         */
        setPageTitle: function (id) {
            if (titleCache.hasOwnProperty(id)) {
                document.title = titleCache[id];
            }
        },

        /*
         * Legacy support for the old contact page hash URL's
         */
        checkForHash: function () {
            var hashChange = ('onhashchange' in window);
            var itemId;

            if (hashChange && window.location.hash) {
                switch (window.location.hash) {
                case '#map-mountain_view':
                    itemId = 'mountain-view';
                    break;
                case '#map-new-zealand':
                    itemId = 'auckland';
                    break;
                case '#map-china':
                    itemId = 'beijing';
                    break;
                case '#map-europe-london':
                    itemId = 'london';
                    break;
                case '#map-europe-paris':
                    itemId = 'paris';
                    break;
                case '#map-portland':
                    itemId = 'portland';
                    break;
                case '#map-us-san-francisco':
                    itemId = 'san-francisco';
                    break;
                case '#map-taiwan-taipei':
                    itemId = 'taipei';
                    break;
                case '#map-japan':
                    itemId = 'tokyo';
                    break;
                case '#map-canada-toronto':
                    itemId = 'toronto';
                    break;
                case '#map-canada-vancouver':
                    itemId = 'vancouver';
                    break;
                }

                if (itemId) {
                    setTimeout(function () {
                        $('#nav-spaces li[data-id="' + itemId + '"] a').trigger('click');
                    }, 100);
                }
            }
        },

        abortRequest: function () {
            if (xhr && xhr.readystate !== 4) {
                xhr.abort();
            }
        },

        /*
         * Requests content for displaying current space information
         * Params: @id space identifier string, @url url to request
         */
        requestContent: function (url) {
            //abort previous request if one exists
            mozMap.abortRequest();

            //get the page content
            xhr = $.ajax({
                url: url,
                type: 'get',
                dataType: 'html',
                cache: 'false',
                success: function(data) {
                    // pull out data we need
                    var content = $($.parseHTML(data)).find('section.entry');
                    var title = data.match(/<title>(.*?)<\/title>/);
                    var id = content.prop('id');

                    // add content to the cache for future retrieval
                    contentCache[id] = content;
                    titleCache[id] = title[1];
                    // update content in the page
                    $('#entry-container').html(content);

                    // update the page title
                    mozMap.setPageTitle(id);
                    // pan to the new marker
                    mozMap.panToMarker(id);
                    // show the corresponding community region
                    mozMap.showCommunityRegion(id);
                }
            });
        }
    };

    //initialize mapbox
    mozMap.init();

})(jQuery);
