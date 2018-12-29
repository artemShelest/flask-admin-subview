(function ($) {
    function showError(prefix, el, message) {
        if (typeof message === "object") {
            if (typeof message['responseText'] !== "undefined") {
                var rtLower = message['responseText'].toLowerCase();
                if (rtLower.search("<" + "!doctype html") !== -1) {
                    injectSubview(el, message['responseText']);
                    return;
                }
            }
            message = JSON.stringify(message);
        }
        return alert(prefix + message);
    }

    function expandedHref(el, link, e) {
        var current = el.dataset.lastUrl.split("?")[0];
        var newUrl = link.href.split("?")[0];
        if (!newUrl.endsWith(current)) {
            return;
        }
        e.preventDefault();
        e.stopPropagation();
        loadSubview(el, link.href);
    }

    function injectSubview(el, data, url) {
        var $el = $(el);
        $el.html(data);
        if (typeof url !== "undefined") {
            el.dataset.lastUrl = url;
        }
        $el.find("a[href^='/']").each(function (i, link) {
            link.addEventListener("click", expandedHref.bind(null, el, link));
        });
    }

    function getParameterByName(name) {
        var url = window.location.href;
        name = name.replace(/[\[\]]/g, '\\$&');
        var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'), results = regex.exec(url);
        if (!results) {
            return null;
        }
        if (!results[2]) {
            return '';
        }
        return decodeURIComponent(results[2].replace(/\+/g, ' '));
    }

    function expandUrl(url, el) {
        if (typeof el.dataset.subviewParam !== "undefined") {
            var name = el.dataset.subviewParam;
            if (url.indexOf("?" + name + "=") < 0 && url.indexOf("&" + name + "=") < 0) {
                url += "?" + name + "=" + getParameterByName(name);
            }
        }
        return url;
    }

    function loadSubview(el, url) {
        // TODO: loading message customization/internationalization
        var node = $("<div class='flask-admin-subview-preloader'>...</div>");
        el.appendChild(node.get(0));
        $.ajax({
            type: "GET",
            url: expandUrl(url, el),
            success: function (data) {
                injectSubview(el, data, url);
            },
            error: function (message) {
                showError("Subview load failed: ", el, message);
            }
        });
    }

    function postForm(form) {
        var $form = $(form).closest("form");
        var el = $form.closest("[data-type=subview]").get(0);
        $.ajax({
            type: "POST",
            url: expandUrl($form.attr('action'), el),
            traditional: true,
            data: $form.find("input").get().reduce(function (o, el) {
                var t = typeof o[el.name];
                if (t !== "undefined") {
                    if (t !== "object") {
                        o[el.name] = [o[el.name]];
                    }
                    o[el.name].push(el.value);
                } else {
                    o[el.name] = el.value;
                }
                return o;
            }, {}),
            success: function (data, status, xhr) {
                if (typeof xhr.responseJSON !== "undefined") {
                    var json = xhr.responseJSON;
                    if (typeof json.redirect !== "undefined") {
                        window.location = json.redirect;
                    }
                } else {
                    injectSubview(el, data);
                }
            },
            error: function (message) {
                showError("Form POST failed: ", el, message);
            }
        });
        return false;
    }

    const SUBVIEWS = $("[data-type=subview]").each(function (i, el) {
        loadSubview(el, el.dataset.subview);
    });
    window.Subview = {
        postForm: postForm,
        reload: function () {
            SUBVIEWS.each(function (i, el) {
                var url;
                if (typeof el.dataset.lastUrl !== "undefined") {
                    url = el.dataset.lastUrl;
                } else {
                    url = el.dataset.subview;
                }
                loadSubview(el, url);
            });
        }
    };
})(jQuery);
