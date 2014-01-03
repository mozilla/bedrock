// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

(function() {
    "use strict";

    var DATABASE_URL = "//lightbeamdb.org";
    var ROWS_PER_TABLE_PAGE = 10;
    var AJAX_JSONP_TIMEOUT = 30 * 1000; // 30 sec in millinseconds
    var currentPage;
    var allSites;
    var errorNotice = function jsonpErrorHandling(){
        addClass(document.querySelector("#loading img"),"hidden");
        var loadingMsg = document.querySelector("#loading span");
        loadingMsg.innerHTML = loadingMsg.getAttribute("data-message");
    };
    
    function checkClassExist(elem,theClass){
        return elem.className.split(" ").indexOf(theClass) > -1;
    }

    function addClass(elem,theClass){
        if ( !checkClassExist(elem,theClass) ){
            elem.className += " " + theClass; 
        }
    }

    function removeClass(elem,theClass){
        if ( checkClassExist(elem,theClass) ){
            var classes = elem.className.split(" ");
            classes.splice(classes.indexOf(theClass),1);
            elem.className = classes.join(" ");
        }
    }

    document.addEventListener("DOMContentLoaded", function() {
        currentPage = document.querySelector("body");

        if (checkClassExist(currentPage,"database")) {
            loadContentDatabase();
        } else if (checkClassExist(currentPage,"profile")) {
            var hrefArray = window.location.href.split('?');
            var site = hrefArray[hrefArray.length-1].substr(5);
            loadContentProfile(site);
        } else {
        }
    });

    function showLoading() {
        removeClass(document.getElementById("loading"),"hidden");
    }

    function hideLoading() {
        addClass(document.getElementById("loading"),"hidden");
    }

    function addCommasToNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    var siteTableClickHandler = function(event) {
        var row = event.target;
        var profileURL = "";
        if (!row.getAttribute("data-url")) {
            row = row.parentElement;
        }
        profileURL = row.getAttribute("data-url"); 
        if (!profileURL) {
            return;
        }
        window.location = profileURL;
    };

    if (document.querySelector(".website-list-table")) {
        document.querySelector(".website-list-table").addEventListener("click", siteTableClickHandler);
    }

    if (document.querySelector(".top-sites-table")) {
        document.querySelector(".top-sites-table").addEventListener("click", siteTableClickHandler);
    }


    /********************************************************************************
    *   Database Page
    */

    // jQuery does not handle cross-domain jsonp request. Set a timer as a workaround.
    var timeoutTimer = setTimeout(errorNotice, AJAX_JSONP_TIMEOUT);
    var dbPageTimeoutCleared = false;
    function loadContentDatabase(){
        showLoading();
        $.ajax({
            url: DATABASE_URL + "/databaseSiteList",
            dataType: 'jsonp',
            success: function(data){
                allSites = data.siteData;
                showAllSitesTable();
                var total = currentPage.querySelectorAll(".num-sites");
                for (var i=0; i<total.length; i++){
                    total[i].textContent = addCommasToNumber(Object.keys(allSites).length);
                }
                document.getElementById("website-list-time-range").innerHTML = data.timeRange;
                hideLoading();
                if ( !dbPageTimeoutCleared ){
                    dbPageTimeoutCleared = true;
                    clearTimeout(timeoutTimer);
                }
            }
        });

        // top 10
        $.ajax({
            url: DATABASE_URL + "/dashboardDataTop10",
            dataType: 'jsonp',
            success: function(data){
                showPotentialTracker(data.topTenSites);
                document.getElementById("top-list-time-range").innerHTML = data.timeRange;
                hideLoading();
                if ( !dbPageTimeoutCleared ){
                    dbPageTimeoutCleared = true;
                    clearTimeout(timeoutTimer);
                }
            }
        });

    }


    /****************************************
    *   Table Sorting
    */

    function showPotentialTracker(top10Trackers) {
        var html = "";
        var siteArray = Object.keys(top10Trackers);
        var site;
        var row;
        for ( var i=0; i<siteArray.length; i++ ) {
            site = top10Trackers[siteArray[i]];
            row = "<tr data-url='/lightbeam/profile?site="+ site.site + "'>" +
                    "<td>" + (i+1) + "</td>" +
                    "<td>" + site.site + "</td>" +
                "</tr>";
            html += row;
        }
        $(".top-sites-table tbody").html(html);
    }

    function showAllSitesTable(pageIndex) {
        if (!pageIndex) { 
            pageIndex = 1; 
        }
        var numTotalPages = Math.ceil(allSites.length/ROWS_PER_TABLE_PAGE);
        var start = (pageIndex-1) * ROWS_PER_TABLE_PAGE;
        var end = (pageIndex * ROWS_PER_TABLE_PAGE);
        var tbody = "";
        allSites.slice(start,end).forEach(function(site) {
            tbody += addTableRow(site);
        });
        $(".website-list-table tbody").html(tbody);
        addPageSelection(pageIndex,numTotalPages);
    }

    function addPageSelection(current,total) {
        currentPage.querySelector(".row-start").textContent = (current-1) * ROWS_PER_TABLE_PAGE + 1;
        currentPage.querySelector(".row-end").textContent = (current-1) * ROWS_PER_TABLE_PAGE + currentPage.querySelectorAll(".website-list-table tbody tr[data-url]").length;
        
        if ( !document.querySelector(".pagination select") ) {
            var html = "Page: <select>";
            for (var i=1; i<=total; i++) {
                html = html + "<option>" + i + "</option>";
            }
            html += "</select>";
            currentPage.querySelector(".pagination").innerHTML = html;
        }
    }

    function sortSiteList(sortByFunction) {
        if (sortByFunction) {
            allSites.sort(sortByFunction);
        }
        showAllSitesTable();
        document.querySelector(".pagination select").selectedIndex = 0;
    }

    function addTableRow(site) {
        var html = "<tr data-url='/lightbeam/profile?site="+ site.site + "'>" +
                        "<td>" + site.site + "</td>";
        if ( site.numSources ) { 
            html += "<td>" + addCommasToNumber(site.numSources) + "</td>"; 
        }
        if ( site.numConnections ) { 
            html += "<td>" + addCommasToNumber(site.numConnections) + "</td>"; 
        }
        return html + "</tr>";
    }

    var paginationForSiteTables = function paginationHandler() {
        var selectedIdx = document.querySelector(".pagination select").selectedIndex; // starts from 0
        showAllSitesTable( (selectedIdx+1));
    };

    var sortingForSiteTables = function sortingHandler(event) {
        var sortBy = event.target.getAttribute("data-sort");
        if (sortBy) {
            var sortByFunction;
            var sortByConnectedSites = function(a,b) { return b.numSources - a.numSources; };
            var sortByConnections = function(a,b) { return b.numConnections - a.numConnections; };
            var sortByAlpha = function(a,b) {
                                if (a.site.toLowerCase() < b.site.toLowerCase()) { 
                                    return -1; 
                                }
                                if (a.site.toLowerCase() > b.site.toLowerCase()) { 
                                    return 1;
                                }
                                return 0; 
                            };
            if (sortBy === "siteConnected") {
                sortByFunction = sortByConnectedSites;
            } else if (sortBy === "connections") {
                sortByFunction = sortByConnections;
            } else {
                sortByFunction = sortByAlpha;
            }

            document.querySelector(".sorting-options button[data-selected]").removeAttribute("data-selected");
            event.target.setAttribute("data-selected","true");

            sortSiteList(sortByFunction);
        }
    };

    if ( document.querySelector(".database") ) {
        $(".sorting-options button").click(sortingForSiteTables);
        document.querySelector(".pagination").addEventListener("change",paginationForSiteTables);
    }


    /********************************************************************************
    *   Profile Page
    */

    function turnMapIntoArray(nodemap) {
        var node;
        var arr = Object.keys(nodemap).map(function(nodeName) {
            node = nodemap[nodeName];
            return { site: node.name, numConnections: node.howMany };
        });
        return arr;
    }

    function loadContentProfile(siteName) {
        showLoading();
        var sites = currentPage.querySelectorAll(".site");
        for (var i=0; i<sites.length; i++) {
            sites[i].textContent = siteName;
        }
        // jQuery does not handle cross-domain jsonp request. Set a timer as a workaround.
        var timeoutTimer = setTimeout(errorNotice, AJAX_JSONP_TIMEOUT);
        $.ajax( {
            url: DATABASE_URL+"/getSiteProfileNew?name=" + siteName,
            dataType: 'jsonp',
            success: function(data) {
                var siteData = data.siteData;
                if ( Object.keys(siteData).length < 1 ){
                    hideLoading();
                    clearTimeout(timeoutTimer);
                    return;
                }
                // generate d3 graph
                lightbeam.loadData(siteData);
                // other UI content
                var siteProfile = siteData[siteName];
                var howMany = siteProfile.howMany;
                var numFirstParty = siteProfile.howManyFirstParty;
                addConnnectionBar(numFirstParty, howMany);
                currentPage.querySelector(".num-total-connection b").innerHTML = addCommasToNumber(howMany);
                currentPage.querySelector(".num-first b").innerHTML = addCommasToNumber(numFirstParty);
                currentPage.querySelector(".num-third b").innerHTML = addCommasToNumber(howMany-numFirstParty);
                // connected sites table
                delete siteData[siteName];
                allSites = turnMapIntoArray(siteData);
                document.querySelector(".sorting-options button[data-selected]").click();
                var total = currentPage.querySelectorAll(".num-sites");
                for (var i=0; i<total.length; i++) {
                    total[i].textContent = addCommasToNumber(Object.keys(siteData).length);
                }
                document.getElementById("website-list-time-range").innerHTML = data.timeRange;
                hideLoading();
                clearTimeout(timeoutTimer);
            }
        });

        /***************************************************
        *   Find out where the server of the site locates
        *
        *   Based on https://github.com/toolness/url-demystifier
        *   and uses Steven Levithan's parseUri 1.2.2
        */
        var countryElem = document.getElementById("country");
        $.ajax( {
            url: "//freegeoip.net/json/" + siteName,
            dataType: 'json',
            success: function(data) {
                var countryName = data.country_name;
                if ( data === false || countryName === "Reserved" ) {
                    countryElem.innerHTML = countryElem.getAttribute("data-message");
                } else {
                    countryElem.innerHTML = data.country_name;
                }
            },
            error: function(){
                countryElem.innerHTML = countryElem.getAttribute("data-message");
            }
        });

        // squareify canvas size - cross broswer fix
        var canvasContainer = document.querySelector(".vizcanvas-container");
        var canvas = canvasContainer.querySelector("svg");
        canvas.setAttribute("height",canvasContainer.getBoundingClientRect().width);
    }

    function addConnnectionBar(numFirstParty,numTotal) {
        // calculate connections percentage bar
        var totalWidth;
        try{
            totalWidth = currentPage.querySelector(".percent-bar").parentElement.getBoundingClientRect().width;
        }catch(e){  // getBoundingClientRect() might not work in older IE
            totalWidth = currentPage.querySelector(".percent-bar").clientWidth;
        }
        var firstPartyRatio = numFirstParty / numTotal;
        var firstBar = currentPage.querySelector(".first-bar");
        var thirdBar = currentPage.querySelector(".third-bar");
        var firstBarLabel = currentPage.querySelector(".first-bar + text");
        var thirdBarLabel = currentPage.querySelector(".third-bar + text");
        firstBar.setAttribute("width", totalWidth*firstPartyRatio);
        firstBarLabel.innerHTML = Math.round(firstPartyRatio*100) + "%";
        thirdBar.setAttribute("x", totalWidth*firstPartyRatio);
        thirdBar.setAttribute("width", totalWidth*(1-firstPartyRatio));
        thirdBarLabel.setAttribute("x", totalWidth*firstPartyRatio + 5);
        thirdBarLabel.innerHTML = Math.round((1-firstPartyRatio)*100) + "%";
    }


    if ( document.querySelector(".profile") ) {
        document.querySelector(".profile .pagination").addEventListener("change",paginationForSiteTables);
        $(".profile .sorting-options button").click(sortingForSiteTables);
    }

})();
