$(function(){
    
    var csrfToken = getCookie('csrftoken'),
        widget = $('.files-widget'),
        effectTime = 200,
        mediaURL = $('[data-media-url]').data('media-url'),
        staticURL = $('[data-static-url]').data('static-url'),
        template,
        deletedTemplate;

    template =
        '<div class="new preview">'+
            '<span class="image-holder">'+
                '<img class="thumbnail" />'+
                '<span class="buttons">'+
                    '<a href="javascript:void(0)" class="enlarge-button">'+
                        '<img src="'+ staticURL + 'files_widget/img/enlarge_button.png" />'+
                    '</a> '+
                    '<a href="javascript:void(0)" class="remove-button">'+
                        '<img src="'+ staticURL + 'files_widget/img/close_button.png" />'+
                    '</a>'+
                '</span>'+
            '</span>'+
            '<div class="progress-holder">'+
                '<div class="progress"></div>'+
            '</div>'+
        '</div>';

    deletedTemplate =
        '<div class="deleted-file">'+
            '<span class="image-holder">'+
                '<img class="icon" />'+
            '</span>'+
            '<span class="name"></span>'+
            '<span class="undo">'+
                '<a href="javascript:void(0);" class="undo-remove-button">'+
                    'Undo'+
                '</a>'+
            '</span>'+
        '</div>';

    function splitlines(str) {
        return str.match(/[^\r\n]+/g) || [];
    }

    function filenameFromPath(path) {
        return path.replace(/^.+\//);
    }

    function stripMediaURL(path) {
        if (path.indexOf(mediaURL) === 0) {
            return path.replace(mediaURL, '');
        }
        return path;
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function numberformat( number, decimals, dec_point, thousands_sep ) {
        // http://kevin.vanzonneveld.net
        // +   original by: Jonas Raoni Soares Silva (http://www.jsfromhell.com)
        // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)  
        // *     example 1: number_format(1234.5678, 2, '.', '');
        // *     returns 1: 1234.57     
     
        var n = number, c = isNaN(decimals = Math.abs(decimals)) ? 2 : decimals;
        var d = dec_point == undefined ? "," : dec_point;
        var t = thousands_sep == undefined ? "." : thousands_sep, s = n < 0 ? "-" : "";
        var i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", j = (j = i.length) > 3 ? j % 3 : 0;
        
        return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
    }

    function sizeformat(filesize) {
        // from http://snipplr.com/view/5945/javascript-numberformat--ported-from-php/
        if (filesize >= 1073741824) {
             filesize = numberformat(filesize / 1073741824, 2, '.', '') + ' GB';
        } else { 
            if (filesize >= 1048576) {
                filesize = numberformat(filesize / 1048576, 2, '.', '') + ' MB';
        } else { 
                if (filesize >= 1024) {
                filesize = numberformat(filesize / 1024, 0) + ' KB';
            } else {
                filesize = numberformat(filesize, 0) + 'B';
                };
            };
        };
        return filesize;
    };

    function fillIn(input, files) {
        var value = '';
        files.each(function() {
            var path = $(this).data('image-path');
            if (path) {
                value += path + '\n';
            }
        });
        input.val(value);
    }

    function fillInHiddenInputs(inputName, movedOutFile, movedInFile) {
        var input = $('input[name="' + inputName + '_0"]'),
            deletedInput = $('input[name="' + inputName + '_1"]'),
            movedInput = $('input[name="' + inputName + '_2"]'),
            widget = input.closest('.files-widget'),
            files = widget.find('.preview'),
            deletedFiles = widget.find('.deleted-file');

        fillIn(input, files.add(movedInFile));
        fillIn(deletedInput, deletedFiles);

        if (movedOutFile) {
            var movedInputValue = splitlines(movedInput.val()),
                filename = movedOutFile.data('image-path');
            //console.log(movedOutFile);
            movedInputValue.push(filename);
            movedInput.val(movedInputValue.join('\n'));
        }
        if (movedInFile) {
            var movedInputValue = splitlines(movedInput.val()),
                filename = movedInFile.data('image-path'),
                index = movedInputValue.indexOf(filename);

            if (index != -1) {
                movedInputValue.splice(index, 1);
                movedInput.val(movedInputValue);
            }
        }
    }

    $(document).bind('dragover', function (e) {
        e.preventDefault();
        $('.files-widget-dropbox').addClass('dragging-files');
    }).bind('drop', function (e) {
        e.preventDefault();
        $('.files-widget-dropbox').removeClass('dragging-files');
    }).bind('dragleave', function (e) {
        $('.files-widget-dropbox').removeClass('dragging-files');
    });

    widget.each(function() {
        var that = $(this),
            dropbox = $('.files-widget-dropbox', that),
            inputName = dropbox.data('input-name'),
            hiddenInput = $('input[name="' + inputName + '_0"]', that),
            filesInput = $('.files-input', that),
            deletedInput = $('input[name="' + inputName + '_1"]', that),
            message = $('.message', dropbox),
            uploadURL = dropbox.data('upload-url'),
            fallback_id = filesInput.attr('id'),
            initialFiles = $('.preview', dropbox),
            fileBrowserResultInput = $('.filebrowser-result', that),
            deletedContainer = $('.files-widget-deleted', that),
            deletedList = $('.deleted-list', deletedContainer),
            stats = $('.upload-progress-stats', that);

        if (initialFiles.length) {
            message.hide();
        }
        if (deletedList.find('.deleted-file').length) {
            deletedContainer.show();
        }

        dropbox.on('click', '.remove-button', function() {
            $(this).closest('.preview').fadeOut(effectTime, function() {
                var preview = $(this),
                    deletedPreview = $(deletedTemplate),
                    path = preview.data('image-path');

                $('.icon', deletedPreview).attr('src', preview.find('.thumbnail').attr('src'));
                $('.name', deletedPreview).text(filenameFromPath(path));
                deletedPreview.attr('data-image-path', path);
                deletedContainer.show();
                deletedPreview.hide().appendTo(deletedList).slideDown(effectTime);
                preview.remove();

                if (!dropbox.find('.preview').length) {
                    message.show();
                };
                fillInHiddenInputs(inputName);
            });
        });

        that.on('click', '.undo-remove-button', function() {
            var deletedPreview = $(this).closest('.deleted-file'),
                preview = $(template), 
                image = $('.thumbnail', preview),
                imagePath = deletedPreview.data('image-path');
            
            image.attr('src', $('.icon', deletedPreview).attr('src'));
            preview.removeClass('new');
            preview.attr('data-image-path', imagePath).find('.progress-holder').remove();
            message.hide();
            preview.hide().insertAfter(dropbox.children(':last-child')).fadeIn(effectTime);
            deletedPreview.slideUp(effectTime, function() {
                $(this).remove();
                if (!deletedList.find('.deleted-file').length) {
                    deletedContainer.hide();
                };
                fillInHiddenInputs(inputName);
            });
        });

        dropbox.on('click', '.enlarge-button', function() {
            window.open(mediaURL + $(this).closest('.preview').data('image-path'));
        });

        function onFileBrowserResult() {
            var preview = $(template), 
                image = $('.thumbnail', preview),
                imagePath = stripMediaURL(fileBrowserResultInput.val());

            $.get(dropbox.data('get-thumbnail-url'), 'img=' + imagePath, function(data) {
                image.attr('src', data);
                preview.removeClass('new');
            });
            preview.attr('data-image-path', imagePath).find('.progress-holder').remove();
            message.hide();
            fileBrowserResultInput.val('');
            preview.insertAfter(dropbox.children(':last-child'));
            fillInHiddenInputs(inputName);
        }

        function checkFileBrowserResult() {
            var oldVal = fileBrowserResultInput.val(),
                checkInterval;

            checkInterval = setInterval(function() {
                var newVal = fileBrowserResultInput.val();
                if (oldVal != newVal) {
                    clearInterval(checkInterval);
                    onFileBrowserResult();
                }
            }, 250);
        }

        $('.media-library-button', that).on('click', function() {
            var url = window.__filebrowser_url || '/admin/media-library/browse/'
            FileBrowser.show(fileBrowserResultInput.attr('id'), url + '?pop=1');
            checkFileBrowserResult();
        });

        dropbox.sortable({
            placeholder: 'sortable-placeholder',
            tolerance: 'pointer',
            connectWith: '.files-widget-dropbox',

            start: function(e, ui) {
                $('.sortable-placeholder').width(ui.item.width()).height(ui.item.height());
            },

            over: function() {
                message.hide();
            },

            beforeStop: function(e, ui) {
                var newInputName = ui.placeholder.parent().data('input-name');
                if (newInputName == inputName) {
                    fillInHiddenInputs(inputName);
                } else {
                    fillInHiddenInputs(inputName, ui.item, null);
                    fillInHiddenInputs(newInputName, null, ui.item);
                    if (!dropbox.find('.preview').length) {
                        message.show();
                    }
                }
            }
        });

        dropbox.disableSelection();
        dropbox.bind('dragover', function (e) {
            dropbox.addClass('dragover');
        }).bind('dragleave drop', function (e) {
            dropbox.removeClass('dragover');
        });

        filesInput.fileupload({
            url: uploadURL,
            type: 'POST',
            dataType: 'json',
            dropZone: dropbox,
            pasteZone: dropbox,
            paramName: 'files[]',
            limitConcurrentUploads: 3,
            formData: [
                {
                    name: 'csrf_token',
                    value: csrfToken
                },
            ],
            autoUpload: true,
            maxFileSize: 10000000,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
            maxNumberOfFiles: undefined,
            previewMaxWidth: 150,
            previewMaxHeight: 150,
            previewCrop: true,

            add: function(e, data) {
                var preview = $(template), 
                    image = $('.thumbnail', preview),
                    reader = new FileReader(),
                    file = data.files[0];
                //console.log('add', data);
                reader.onload = function(e){
                    image.attr('src', e.target.result);
                };
                
                if (file.size < 500000) {
                    reader.readAsDataURL(file);
                } else {
                    $('<span/>').addClass('filename').text(file.name)
                        .appendTo('.image-holder', preview);
                }
                
                message.hide();
                preview.insertAfter(dropbox.children(':last-child'));
                data.context = preview;
                data.submit();
            },

            submit: function(e, data) {
                // console.log('submit', data);
                // create thumbnail client side?
            },

            done: function(e, data) {
                var preview = data.context;

                //console.log('done', data);
                preview.removeClass('new').attr('data-image-path', data.result.imagePath);
                preview.find('.progress-holder, .filename').remove();
                preview.find('.thumbnail').attr('src', data.result.thumbnailPath);
                fillInHiddenInputs(inputName);
            },

            fail: function(e, data) {
                //console.log('failed', data);
                // display errors
            },

            always: function(e, data) {
                //console.log('always', data);
                stats.text('');
            },

            progress: function(e, data) {
                //console.log('progress', data);
                var progress = parseInt(data.loaded / data.total * 100, 10);
                data.context.find('.progress').css('width', progress + '%');
            },

            progressall: function(e, data) {
                //console.log('progressall', data);
                stats.text(sizeformat(data.loaded) +
                    ' of ' + sizeformat(data.total) +
                    ' (' + sizeformat(data.bitrate) + 'ps)');
            },
        });
    });
});
