function setupVersion() {
        var versionBox = document.getElementById("version-box");
        var downloadBox = document.getElementById("download-link");

        var req = new XMLHttpRequest();
        //req.open('GET', 'https://services.addons.mozilla.org/en-US/thunderbird/api/1.5/addon/lightning', false);
        //document.domain = "kewis.ch";
        req.open('GET', 'http://mozilla.kewis.ch/mozilla.org/lightning.xml', true);
        req.onreadystatechange = function() {
            if (req.readyState == 4) {
                var doc = req.responseXML;
                var xp = doc.evaluate("//addon/version/text()", doc, null, XPathResult.STRING_TYPE, null);
                versionBox.textContent = "Lightning " + xp.stringValue;
                downloadBox.className = downloadBox.className.replace("loading", "");

                var downloadLink = downloadBox.getAttribute("href");;
                if (navigator.platform.match(/Win/)) {
                    downloadLink = doc.evaluate("//addon/install[@os='WINNT']/text()", doc, null, XPathResult.STRING_TYPE, null).stringValue;
                } else if (navigator.platform.match(/Mac/)) {
                    downloadLink = doc.evaluate("//addon/install[@os='Darwin']/text()", doc, null, XPathResult.STRING_TYPE, null).stringValue;
                } else if (navigator.platform.match(/Linux/)) {
                    downloadLink = doc.evaluate("//addon/install[@os='Linux']/text()", doc, null, XPathResult.STRING_TYPE, null).stringValue;
                }
                downloadBox.setAttribute("href", downloadLink);
            }
        };

        req.send(null);
      }

      window.addEventListener("DOMContentLoaded", setupVersion, false);