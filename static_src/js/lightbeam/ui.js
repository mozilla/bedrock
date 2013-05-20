// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

(function() {
    "use strict";

    // not sure what's the best way to include the URL
    var DATABASE_URL = "//collusiondb.mofoprod.net";
    var ROWS_PER_TABLE_PAGE = 20;
    var AJAX_JSONP_TIMEOUT = 30 * 1000; // in millinseconds
    var currentPage;
    var allSites;
    var errorNotice = function jsonpErrorHandling(){
        addClass(document.querySelector("#loading img"),"hidden");
        document.querySelector("#loading span").innerHTML = "This is taking longer than expected. <br/>Please reload the page or check back later. <br/>Thanks!";
    };
    
    function checkClassExist(elem,theClass){
        return elem.className.split(" ").indexOf(theClass) > -1;
    };

    function addClass(elem,theClass){
        if ( !checkClassExist(elem,theClass) ){
            elem.className += " " + theClass; 
        }
    };

    function removeClass(elem,theClass){
        if ( checkClassExist(elem,theClass) ){
            var classes = elem.className.split(" ");
            classes.splice(classes.indexOf(theClass),1);
            elem.className = classes.join(" ");
        }
    };

    document.addEventListener("DOMContentLoaded", function(event) {
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
        removeClass(document.querySelector("#loading"),"hidden");
    }

    function hideLoading() {
        addClass(document.querySelector("#loading"),"hidden");
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

    if (document.querySelector(".top-trackers-table")) {
        document.querySelector(".top-trackers-table").addEventListener("click", siteTableClickHandler);
    }


    /********************************************************************************
    *   Database Page
    */

    function loadContentDatabase() {
        showLoading();
        // jQuery does not handle cross-domain jsonp request. Set a timer as a workaround.
        var timeoutTimer = setTimeout(errorNotice, AJAX_JSONP_TIMEOUT);
        $.ajax( {
            url: DATABASE_URL + "/databaseSiteList",
            dataType: 'jsonp',
            success: function(data) {
                var top10Trackers = data[1];
                var total;
                allSites = data[0];
                showAllSitesTable();
                showPotentialTracker(top10Trackers);
                total = currentPage.querySelectorAll(".num-sites");
                for (var i=0; i<total.length; i++) {
                    total[i].textContent = addCommasToNumber(Object.keys(data[0]).length);
                }
                hideLoading();
                clearTimeout(timeoutTimer);
            }
        });
    }


    /****************************************
    *   Table Sorting
    */

    function showPotentialTracker(top10Trackers) {
        var html = currentPage.querySelector(".top-trackers-table").innerHTML;
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
        $(".top-trackers-table").html(html);
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
        if ( site.numConnectedSites ) { 
            html += "<td>" + addCommasToNumber(site.numConnectedSites) + "</td>"; 
        }
        if ( site.numConnections ) { 
            html += "<td>" + addCommasToNumber(site.numConnections) + "</td>"; 
        }
        return html + "</tr>";
    }

    var paginationForSiteTables = function paginationHandler(event) {
        var selectedIdx = document.querySelector(".pagination select").selectedIndex; // starts from 0
        showAllSitesTable( (selectedIdx+1));
    };

    var sortingForSiteTables = function sortingHandler(event) {
        var sortBy = event.target.getAttribute("data-sort");
        if (sortBy) {
            var sortByFunction;
            var sortByConnectedSites = function(a,b) { return b.numConnectedSites - a.numConnectedSites; };
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

            document.querySelector(".sorting-options a[data-selected]").removeAttribute("data-selected");
            event.target.setAttribute("data-selected","true");

            sortSiteList(sortByFunction);
        }
    };

    if ( document.querySelector(".database") ) {
        document.querySelector(".sorting-options").addEventListener("click",sortingForSiteTables);
        document.querySelector(".pagination").addEventListener("click",paginationForSiteTables);
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
                // generate d3 graph
                lightbeam.loadData(data); 
                // other UI content
                var siteData = data[siteName];
                addConnnectionBar(siteData.howManyFirstParty, siteData.howMany);
                currentPage.querySelector(".num-total-connection b").innerHTML = siteData.howMany;
                currentPage.querySelector(".num-first b").innerHTML = siteData.howManyFirstParty;
                currentPage.querySelector(".num-third b").innerHTML = siteData.howMany - siteData.howManyFirstParty;
                // connected sites table
                delete data[siteName];
                allSites = turnMapIntoArray(data);
                document.querySelector(".profile .sorting-options a[data-selected]").click();
                var total = currentPage.querySelectorAll(".num-sites");
                for (var i=0; i<total.length; i++) {
                    total[i].textContent = addCommasToNumber(Object.keys(data).length);
                }
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
        $.ajax( {
            url: "//freegeoip.net/json/" + siteName,
            dataType: 'json',
            success: function(data) {
                var countryName = data.country_name;
                var countryCode = data.country_code.toLowerCase();
                if ( data === false || countryName === "Reserved" ) {
                    document.querySelector("#country").innerHTML = "(Unable to find server location)";
                } else {
                    document.querySelector("#country").innerHTML = data.country_name;
                }
            },
            error: function(){
                document.querySelector("#country").innerHTML = "(Unable to find server location)";
            }
        });

    }

    function addConnnectionBar(numFirstParty,numTotal) {
        // calculate connections percentage bar
        try{
            var totalWidth = currentPage.querySelector(".percent-bar").parentElement.getBoundingClientRect().width;
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
        document.querySelector(".profile .pagination").addEventListener("click",paginationForSiteTables);
        document.querySelector(".profile .sorting-options").addEventListener("click",sortingForSiteTables);
    }

})();
