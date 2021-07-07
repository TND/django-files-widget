$(function () {

    let csrfToken = getCookie('csrftoken'),
        widgets = $('.files-widget'),
        effectTime = 200;

    function splitlines(str) {
        return str.match(/[^\r\n]+/g) || [];
    }

    function filenameFromPath(path) {
        return path.replace(/^.+\//, '');
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function numberformat(number, decimals, dec_point, thousands_sep) {
        // http://kevin.vanzonneveld.net
        // +   original by: Jonas Raoni Soares Silva (http://www.jsfromhell.com)
        // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)  
        // *     example 1: number_format(1234.5678, 2, '.', '');
        // *     returns 1: 1234.57     

        var n = number, c = isNaN(decimals = Math.abs(decimals)) ? 2 : decimals;
        var d = dec_point === undefined ? "," : dec_point;
        var t = thousands_sep === undefined ? "." : thousands_sep, s = n < 0 ? "-" : "";
        var i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", j = (j = i.length) > 3 ? j % 3 : 0;

        return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
    }

    function sizeformat(filesize, bits) {
        var b = 'B';
        if (bits) {
            b = 'b';
        }

        // from http://snipplr.com/view/5945/javascript-numberformat--ported-from-php/
        if (filesize >= 1073741824) {
            filesize = numberformat(filesize / 1073741824, 2, '.', '') + 'G' + b;
        } else {
            if (filesize >= 1048576) {
                filesize = numberformat(filesize / 1048576, 2, '.', '') + 'M' + b;
            } else {
                if (filesize >= 1024) {
                    filesize = numberformat(filesize / 1024, 0) + 'k' + b;
                } else {
                    filesize = numberformat(filesize, 0) + b;
                }
            }
        }
        return filesize;
    }

    function isInputDisabled(input) {
        return input.is(":disabled") || input.is('[readonly="readonly"]');
    }

    widgets.each(function () {
        var that = $(this),
            dropbox = $('.files-widget-dropbox', that);
        if (!dropbox.length) return;

        var hiddenInput = $('input[name="' + dropbox.data('input-name') + '_0"]', that),
            inputDisabled = isInputDisabled(hiddenInput),
            initialFileNames = splitlines(hiddenInput.val()),
            mediaURL = dropbox.data('media-url'),
            staticURL = dropbox.data('static-url'),
            thumbnailURL = dropbox.data('get-thumbnail-url'),
            initialFiles = $('.preview', dropbox),
            previewSize = dropbox.data('preview-size'),
            message = $('.message', dropbox),
            removeButtonHtml="",
            previewTemplate;

        if(!inputDisabled)
            removeButtonHtml =
                '<a href="javascript:void(0)" class="remove-button">' +
                '<img src="' + staticURL + 'files_widget/img/close_button.png" />' +
                '</a>';

        previewTemplate =
            '<div class="new preview">' +
                '<span class="image-holder">' +
                    '<img class="thumbnail" />' +
                    '<span class="buttons">' +
                        '<a href="javascript:void(0)" class="enlarge-button">' +
                            '<img src="' + staticURL + 'files_widget/img/enlarge_button.png" />' +
                        '</a> ' + removeButtonHtml +
                    '</span>' +
                '</span>' +
                '<div class="progress-holder"><div class="progress"></div></div>' +
            '</div>';

        dropbox.on('click', '.enlarge-button', function () {
            window.open(mediaURL + $(this).closest('.preview').data('image-path'));
        });

        if (!inputDisabled) {
            dropbox.bind('drag dragover', function (e) {
                e.preventDefault();
                dropbox.addClass('dragging-files');
            }).bind('drop', function (e) {
                e.preventDefault();
                dropbox.removeClass('dragging-files');
            }).bind('dragleave', function (e) {
                dropbox.removeClass('dragging-files');
            });
        }

        for (var name in initialFileNames) {
            if (!initialFiles.filter('[data-image-path="' + initialFileNames[name] + '"]').length) {
                addPreview(initialFileNames[name], null, null, true);
            }
        }

        initialFiles = $('.preview', dropbox);
        if (initialFiles.length) {
            message.hide();
        }

        if (inputDisabled) return;

        // The following will be proceeded only when inputDisabled is false

        var filesInput = $('.files-input', that),
            uploadURL = dropbox.data('upload-url'),
            multiple = dropbox.data('multiple') === 1,
            fileBrowserResultInput = $('.filebrowser-result', that),
            deletedContainer = $('.files-widget-deleted', that),
            deletedList = $('.deleted-list', deletedContainer),
            stats = $('.upload-progress-stats', that),
            undoText = $('[data-undo-text]', that).data('undo-text'),

            deletedTemplate;

        deletedTemplate =
            '<div class="deleted-file">' +
                '<span class="image-holder">' +
                    '<img class="icon" />' +
                '</span>' +
                '<span class="name"></span>' +
                '<span class="undo">' +
                    '<a href="javascript:void(0);" class="undo-remove-button">' +
                    undoText +
                    '</a>' +
                '</span>' +
            '</div>';

        if (deletedList.find('.deleted-file').length) {
            deletedContainer.show();
        }

        dropbox.on('click', '.remove-button', function () {
            if (inputDisabled) return;
            var preview = $(this).closest('.preview');
            deletePreview(preview);
        });

        that.on('click', '.undo-remove-button', function () {
            if (inputDisabled) return;
            var deletedPreview = $(this).closest('.deleted-file');
            undoDeletePreview(deletedPreview);
        });

        function onFileBrowserResult() {
            var imagePath = stripMediaURL(fileBrowserResultInput.val()),
                preview = addPreview(imagePath);
            fileBrowserResultInput.val('');
        }

        function checkFileBrowserResult() {
            var oldVal = fileBrowserResultInput.val(),
                checkInterval;

            checkInterval = setInterval(function () {
                var newVal = fileBrowserResultInput.val();
                if (oldVal !== newVal) {
                    clearInterval(checkInterval);
                    onFileBrowserResult();
                }
            }, 250);
        }

        $('.media-library-button', that).on('click', function () {
            var url = window.__filebrowser_url || '/admin/media-library/browse/';
            FileBrowser.show(fileBrowserResultInput.attr('id'), url + '?pop=1');
            checkFileBrowserResult();
        });

        $('.add-by-url-button', that).on('click', function () {
            $('.add-by-url-container', that).show();
            $(this).hide();
            $('.add-by-url', that).trigger('focus');
        });

        $('.add-by-url', that).on('focusout', function () {
            $('.add-by-url-button', that).show();
            $('.add-by-url-container', that).hide();
        }).on('keypress', function (e) {
            var urlInput = $(this),
                val = urlInput.val();

            if (e.which === 13) {
                e.stopPropagation();
                e.preventDefault();

                $('.add-by-url-button', that).show();
                $('.add-by-url-container', that).hide();
                urlInput.val('');

                if (val.length) {
                    addPreview(val);
                }
                return false;
            }
        });

        dropbox.disableSelection();
        dropbox.bind('dragover', function (e) {
            if (inputDisabled) return;
            dropbox.addClass('dragover');
        }).bind('dragleave drop', function (e) {
            if (inputDisabled) return;
            dropbox.removeClass('dragover');
        });

        dropbox.sortable({
            placeholder: 'sortable-placeholder',
            //tolerance: 'pointer',
            connectWith: '.files-widget-dropbox',
            //cursorAt: { top: 0, left: 0 },
            //items: '.preview:not(.controls-preview)',
            revert: effectTime,
            start: function (e, ui) {
                $('.sortable-placeholder').width(ui.item.width()).height(ui.item.height());
            },
            over: function () {
                message.hide();
            },
            beforeStop: function (e, ui) {
                var newDropbox = ui.placeholder.closest('.files-widget-dropbox');
                onPreviewMove(ui.item, dropbox, newDropbox);
            }
        });

        function stripMediaURL(path) {
            if (path.indexOf(mediaURL) === 0) {
                return path.replace(mediaURL, '');
            }
            return path;
        }

        function fillIn(input, files) {
            var value = '';
            files.each(function () {
                var path = $(this).data('image-path');
                if (path) {
                    value += path + '\n';
                }
            });
            input.val(value);
        }

        function fillInHiddenInputs(dropbox, movedOutFile, movedInFile) {
            var input = $('input[name="' + dropbox.data('input-name') + '_0"]'),
                deletedInput = $('input[name="' + dropbox.data('input-name') + '_1"]'),
                movedInput = $('input[name="' + dropbox.data('input-name') + '_2"]'),
                files = that.find('.preview'),
                deletedFiles = that.find('.deleted-file'),
                movedInputValue,
                filename;

            fillIn(input, files.add(movedInFile));
            fillIn(deletedInput, deletedFiles);

            if (movedOutFile) {
                movedInputValue = splitlines(movedInput.val());
                filename = movedOutFile.data('image-path');

                movedInputValue.push(filename);
                movedInput.val(movedInputValue.join('\n'));
            }
            if (movedInFile) {
                movedInputValue = splitlines(movedInput.val());
                filename = movedInFile.data('image-path');
                var index = movedInputValue.indexOf(filename);

                if (index !== -1) {
                    movedInputValue.splice(index, 1);
                    movedInput.val(movedInputValue);
                }
            }
        }

        function downloadThumbnail(preview) {
            var imagePath = stripMediaURL(preview.data('image-path')),
                previewSize = dropbox.data('preview-size');

            $.get(thumbnailURL,
                'img=' + encodeURIComponent(imagePath) + '&preview_size=' + previewSize,
                function (data) {
                    preview.find('.thumbnail')
                        .css({'width': '', 'height': ''}).attr('src', data);
                    ;
                    preview.removeClass('new');
                });
        }

        function generateThumbnail(preview, file) {
            var image = $('.thumbnail', preview),
                reader = new FileReader(),
                previewSize = dropbox.data('preview-size'),
                defaultSize = parseInt(+previewSize * 2 / 3, 10);

            reader.onload = function (e) {
                image.attr('src', e.target.result);
                image.css({'width': '', 'height': ''});
            };

            image.css({
                'max-width': previewSize, 'max-height': previewSize,
                'width': defaultSize, 'height': defaultSize
            });

            if (file.size < 500000) {
                reader.readAsDataURL(file);
            } else {
                $('<span/>').addClass('filename').text(file.name)
                    .appendTo(preview.find('.image-holder'));
            }
        }

        function addPreview(imagePath, thumbnailPath, file, fromHiddenInput) {
            var preview = $(previewTemplate);

            if (dropbox.data('multiple') !== 1) {
                dropbox.find('.preview').each(function () {
                    deletePreview($(this), true);
                });
            }

            dropbox.find('.message').hide();
            preview.hide().insertAfter(dropbox.children(':last-child')).fadeIn(effectTime);
            if (imagePath) {
                completePreview(preview, imagePath, thumbnailPath, fromHiddenInput);
            } else if (file) {
                generateThumbnail(preview, file);
            }

            return preview;
        }

        function completePreview(preview, imagePath, thumbnailPath, fromHiddenInput) {
            preview.removeClass('new').attr('data-image-path', imagePath);
            preview.find('.progress-holder, .filename').remove();

            if (thumbnailPath) {
                preview.find('.thumbnail')
                    .css({'width': '', 'height': ''}).attr('src', thumbnailPath);
            } else {
                downloadThumbnail(preview);
            }
            if (!fromHiddenInput) {
                fillInHiddenInputs(dropbox);
            }
        }

        function onPreviewMove(preview, oldDropbox, newDropbox) {
            if (oldDropbox.is(newDropbox)) {
                fillInHiddenInputs(oldDropbox);
            } else {
                if (newDropbox.data('multiple') !== 1) {
                    newDropbox.find('.preview').not(preview).each(function () {
                        deletePreview($(this), true);
                    });
                }
                fillInHiddenInputs(oldDropbox, preview, null);
                fillInHiddenInputs(newDropbox, null, preview);
                if (!oldDropbox.find('.preview').length) {
                    oldDropbox.find('.message').show();
                }
                if (oldDropbox.data('preview-size') !== newDropbox.data('preview-size')) {
                    downloadThumbnail(preview);
                }
            }
        }

        function deletePreview(preview, changingToNewPreview) {
            var deletedPreview = $(deletedTemplate),
                deletedContainer = $('.files-widget-deleted', that),
                deletedList = $('.deleted-list', deletedContainer),
                path = preview.data('image-path');

            function doDelete() {
                $('.icon', deletedPreview).attr('src', preview.find('.thumbnail').attr('src'));
                $('.name', deletedPreview).text(filenameFromPath(path));
                deletedPreview.attr('data-image-path', path);
                deletedContainer.show();
                deletedPreview.hide().appendTo(deletedList);
                deletedPreview.slideDown(effectTime);
                preview.remove();

                if (!dropbox.find('.preview').length && !changingToNewPreview) {
                    dropbox.find('.message').show();
                }
                fillInHiddenInputs(dropbox);
            }

            if (changingToNewPreview) {
                doDelete();
            } else {
                preview.fadeOut(effectTime, doDelete);
            }
        }

        function undoDeletePreview(deletedPreview) {
            var imagePath = deletedPreview.data('image-path'),
                thumbnailPath = $('.icon', deletedPreview).attr('src'),
                deletedContainer = $('.files-widget-deleted', that),
                deletedList = $('.deleted-list', deletedContainer),
                preview = addPreview(imagePath, thumbnailPath);

            deletedPreview.slideUp(effectTime, function () {
                $(this).remove();
                if (!deletedList.find('.deleted-file').length) {
                    deletedContainer.hide();
                }
                fillInHiddenInputs(dropbox);
            });
        }
        filesInput.fileupload({
            url: uploadURL,
            type: 'POST',
            dataType: 'json',
            dropZone: dropbox,
            pasteZone: dropbox,
            paramName: 'files[]',
            limitConcurrentUploads: 3,
            formData: [
                {name: 'csrfmiddlewaretoken', value: csrfToken},
                {name: 'preview_size', value: previewSize}
            ],
            autoUpload: true,
            maxFileSize: 10000000,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
            maxNumberOfFiles: undefined,
            previewMaxWidth: 150,
            previewMaxHeight: 150,
            previewCrop: true,
            add: function (e, data) {
                var preview = addPreview(undefined, undefined, data.files[0]);
                data.context = preview;
                data.submit();
            },
            submit: function (e, data) {
                // console.log('submit', data);
                // create thumbnail client side?
            },
            done: function (e, data) {
                completePreview(data.context,
                    data.result.imagePath, data.result.thumbnailPath);
            },
            fail: function (e, data) {
                //console.log('failed', data);
                // display errors
            },
            always: function (e, data) {
                //console.log('always', data);
                stats.text('');
            },
            progress: function (e, data) {
                //console.log('progress', data);
                var progress = parseInt(data.loaded / data.total * 100, 10);
                data.context.find('.progress').css('width', progress + '%');
            },
            progressall: function (e, data) {
                //console.log('progressall', data);
                stats.text(sizeformat(data.loaded) +
                    ' of ' + sizeformat(data.total) +
                    ' (' + sizeformat(data.bitrate, true) + 'ps)');
            },
        });
    });
});
