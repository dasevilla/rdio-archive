/*jshint curly: true, eqeqeq: true, forin: true, undef: true, jquery: true */

$(function () {

    var getAttr = function($elem, attrName) {
        var attr = $elem.attr(attrName);
        if (typeof (attr) !== 'undefined') {
            return attr;
        } else {
            return null;
        }
    };

    var durationToStr = function(duration) {
        var returnStr = "";

        var hours = Math.floor(duration / (60 * 60));
        if (hours > 0) {
            returnStr += hours + ":";
        }

        var divisor_for_minutes = duration % (60 * 60);
        var minutes = Math.floor(divisor_for_minutes / 60);
        if (minutes > 9) {
            returnStr += minutes + ":";
        } else {
            returnStr += "0" + minutes + ":";
        }

        var divisor_for_seconds = divisor_for_minutes % 60;
        var seconds = Math.ceil(divisor_for_seconds);
        if (seconds > 9) {
            returnStr += seconds;
        } else {
            returnStr += "0" + seconds;
        }

        return returnStr;
    };

    var popoverTitle = function() {
        var $this = $(this);
        var response = '<h3 class="title">';

        var titleAttr = getAttr($this, 'data-original-title');
        if (titleAttr) {
            response += titleAttr;
        }

        if (getAttr($this, 'data-clean')) {
            response += ' <span class="label success">Clean</span>';
        }

        if (getAttr($this, 'data-explicit')) {
            response += ' <span class="label important">Explicit</span>';
        }

        response += '</h3>';

        return response;
    };

    var popoverContent = function() {
        var $this = $(this);
        var response = "";

        var artistAttr = getAttr($this, 'data-artist');
        if (artistAttr) {
            response += '<p>By <em>' + artistAttr + '</em></p>';
        }

        var lengthAttr = getAttr($this, 'data-length');
        if (lengthAttr) {
            response += '<p>Songs: ' + lengthAttr + '</p>';
        }

        var durationAttr = getAttr($this, 'data-duration');
        if (durationAttr) {
            var durationStr = durationToStr(durationAttr);
            response += '<p>Duration: ' + durationStr + '</p>';
        }

        return response;
    };

    var popoverSettings = {
        html: true,
        offset: 0,
        placement: 'above',
        title: popoverTitle,
        content: popoverContent
    };

    $(".album-link").popover(popoverSettings).click(function(e) {
    });

});
