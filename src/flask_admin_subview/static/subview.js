(function ($) {
    var listeners = [];

    // Copy of admin/js/actions.js
    function adminModelActions($el) {
        var actionErrorMessage = "";
        var actionConfirmations = {};
        try {
            actionErrorMessage = JSON.parse($el.find('#message-data').text());
        } catch (e) {
        }
        try {
            actionConfirmations = JSON.parse($el.find('#actions-confirmation-data').text());
        } catch (e) {
        }

        // batch actions helpers
        function execute(name) {
            var selected = $el.find('input.action-checkbox:checked').length;

            if (selected === 0) {
                alert(actionErrorMessage);
                return false;
            }

            var msg = actionConfirmations[name];

            if (!!msg)
                if (!confirm(msg))
                    return false;

            // Update hidden form and submit it
            var form = $el.find('#action_form');
            $('#action', form).val(name);

            $('input.action-checkbox', form).remove();
            $el.find('input.action-checkbox:checked').each(function () {
                form.append($(this).clone());
            });

            form.submit();

            return false;
        }

        $el.find('.action-rowtoggle').change(function () {
            $el.find('input.action-checkbox').prop('checked', this.checked);
        });

        var inputs = $el.find('input.action-checkbox');
        inputs.change(function () {
            var allInputsChecked = true;
            for (var i = 0; i < inputs.length; i++) {
                if (!inputs[i].checked) {
                    allInputsChecked = false;
                    break;
                }
            }
            $el.find('.action-rowtoggle').attr('checked', allInputsChecked);
        });
        $el.find("[data-action]").click(function (e) {
            e.preventDefault();
            execute(e.currentTarget.dataset.action);
        });
        $el.find('[data-role=tooltip]').tooltip({
            html: true,
            placement: 'bottom'
        });
    }

    function showError(prefix, el, message, notify) {
        if (typeof message === "object") {
            if (typeof message['responseText'] !== "undefined") {
                var rtLower = message['responseText'].toLowerCase();
                if (rtLower.search("<" + "!doctype html") !== -1) {
                    injectSubview(el, message['responseText']);
                    if (notify) {
                        notifyListeners(window.Subview.ERROR, el);
                    }
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
        loadSubview(el, link.href, true);
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
        adminModelActions($el);
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
        if (typeof el.dataset.injectParam !== "undefined") {
            var names = el.dataset.injectParam.split(",").map(function (x) {
                return x.trim();
            }).filter(function (x) {
                return x.length > 0;
            });
            if (names.length > 0) {
                var nextSeparator;
                if (url.indexOf("?") < 0) {
                    nextSeparator = "?";
                } else {
                    nextSeparator = "&";
                }
                for (var idx in names) {
                    var name = names[idx];
                    if (url.indexOf("?" + name + "=") < 0 && url.indexOf("&" + name + "=") < 0) {
                        url += nextSeparator + name + "=" + getParameterByName(name);
                    }
                    nextSeparator = "&";
                }
            }
        }
        return url;
    }

    function notifyListeners(type, el) {
        for (var k in listeners) {
            listeners[k].call(el, type);
        }
    }

    function loadSubview(el, url, notify) {
        // TODO: messages customization/internationalization
        // TODO: preloader from template
        var node = $("<div class='flask-admin-subview-preloader'>...</div>");
        el.appendChild(node.get(0));
        $.ajax({
            type: "GET",
            url: expandUrl(url, el),
            success: function (data) {
                injectSubview(el, data, url);
                if (notify) {
                    notifyListeners(window.Subview.GET, el);
                }
            },
            error: function (message) {
                showError("Subview load failed: ", el, message, notify);
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
                    notifyListeners(window.Subview.POST, el);
                }
            },
            error: function (message) {
                showError("Form POST failed: ", el, message, true);
            }
        });
        return false;
    }

    function reloadSubview(i, el) {
        var url;
        if (typeof el.dataset.lastUrl !== "undefined") {
            url = el.dataset.lastUrl;
        } else {
            url = el.dataset.subview;
        }
        loadSubview(el, url);
    }

    const SUBVIEWS = $("[data-type=subview]").each(function (i, el) {
        loadSubview(el, el.dataset.subview);
    });
    window.Subview = {
        postForm: postForm,
        reload: function () {
            SUBVIEWS.each(reloadSubview);
        },
        reloadNode: function (el) {
            reloadSubview(null, el);
        },
        reloadExcept(exceptEl) {
            SUBVIEWS.each(function (i, el) {
                if (exceptEl !== el) {
                    reloadSubview(i, el);
                }
            });
        },
        addUpdateListener: function (fn) {
            if (listeners.indexOf(fn) < 0) {
                listeners.push(fn);
            }
        },
        removeUpdateListener: function (fn) {
            var idx = listeners.indexOf(fn);
            if (idx < 0) {
                return;
            }
            listeners.splice(idx, 1);
        },
        GET: "get",
        POST: "post",
        ERROR: "error"
    };
})(jQuery);

function safeConfirm(msg) {
    try {
        var isconfirmed = confirm(msg);
        if (isconfirmed == true) {
            return true;
        }
        else {
            return false;
        }
    }
    catch (err) {
        return false;
    }
}
