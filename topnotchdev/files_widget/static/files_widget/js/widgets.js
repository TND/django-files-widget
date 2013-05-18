$(function(){
    
    var csrfToken = getCookie('csrftoken'),
        widget = $('.files-widget'),
        effectTime = 200,
        mediaURL = $('[data-media-url]').data('media-url'),
        staticURL = $('[data-static-url]').data('static-url');

    function splitlines(str) {
        return str.match(/[^\r\n]+/g) || [];
    }

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
            console.log(movedOutFile);
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

    function filenameFromPath(path) {
        return path.replace(/^.+\//);
    }

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
            deletedList = $('.deleted-list', deletedContainer);

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
            preview.hide().appendTo(dropbox).fadeIn(effectTime);
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
                imagePath = fileBrowserResultInput.val();

            $.get(dropbox.data('get-thumbnail-url'), 'img=' + imagePath, function(data) {
                image.attr('src', data);
                preview.removeClass('new');
            });
            preview.attr('data-image-path', imagePath).find('.progress-holder').remove();
            message.hide();
            fileBrowserResultInput.val('');
            preview.appendTo(dropbox);
            fillInHiddenInputs(inputName);
        }

        function checkFileBrowserResult() {
            var oldVal = fileBrowserResultInput.val(),
                checkInterval;

            checkInterval = setInterval(function() {
                var newVal = fileBrowserResultInput.val();
                if (oldVal != newVal) {
                    onFileBrowserResult();
                    clearInterval(checkInterval);
                }
            }, 250);
        }

        $('.media-library-button', that).on('click', function() {
            var url = window.__filebrowser_url || '/admin/media-library/browse/'
            FileBrowser.show(fileBrowserResultInput.attr('id'), url + '?pop=1');
            checkFileBrowserResult();
        });

        dropbox.disableSelection();

        dropbox.sortable({
            start: function(e, ui) {
                $('.sortable-placeholder').width(ui.item.width()).height(ui.item.height());
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
            },
            over: function() {
                message.hide();
            },
            placeholder: 'sortable-placeholder',
            tolerance: 'pointer',
            connectWith: '.files-widget-dropbox',
        });
        
        dropbox.filedrop({
            // The name of the $_FILES entry:
            paramname: 'file',
            fallback_id: fallback_id,
            queuefiles: 2,
            maxfilesize: 10,
            url: uploadURL,

            headers: {
                'X-CSRFToken': csrfToken
            },

            docEnter: function(e) { dropbox.addClass('dragging-files'); },
            docLeave: function(e) { dropbox.removeClass('dragging-files'); },
            docDrop: function(e) { dropbox.removeClass('dragging-files'); },
            drop: function(e) { dropbox.removeClass('dragging-files'); },
            afterAll: function(e) { dropbox.removeClass('dragging-files'); },
            
            uploadFinished: function(i, file, response) {
                $.data(file).removeClass('new').find('.progress-holder, .filename').remove();
                // response is the JSON object that post_file.php returns
                $.data(file).attr('data-image-path', response.imagePath);
                $.data(file).find('.thumbnail').attr('src', response.thumbnailPath);
                fillInHiddenInputs(inputName);
            },
            
            error: function(err, file) {
                switch(err) {
                    case 'BrowserNotSupported':
                        showMessage('Your browser does not support HTML5 file uploads!');
                        break;
                    case 'TooManyFiles':
                        alert('Too many files! Please select 5 at most! (configurable)');
                        break;
                    case 'FileTooLarge':
                        alert(file.name+' is too large! Please upload files up to 2mb (configurable).');
                        break;
                    default:
                        alert('Sorry, an error occurred while uploading file. Please contact your system administrator.')
                        break;
                }
            },
            
            // Called before each upload is started
            beforeEach: function(file){
                if(!file.type.match(/^image\//)){
                    alert('Only images are allowed!');
                    
                    // Returning false will cause the
                    // file to be rejected
                    return false;
                }
            },
            
            uploadStarted:function(i, file, len){
                createImage(file);
            },
            
            progressUpdated: function(i, file, progress) {
                $.data(file).find('.progress').css('width', progress + '%');
            }
             
        });
        
        var template =
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

        var deletedTemplate =
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

        
        function createImage(file) {

            var preview = $(template), 
                image = $('.thumbnail', preview);
                
            var reader = new FileReader();
            
            //image.width = 100;
            //image.height = 100;
            
            reader.onload = function(e){
                
                // e.target.result holds the DataURL which
                // can be used as a source of the image:
                
                image.attr('src', e.target.result);
            };
            
            // Reading the file as a DataURL. When finished,
            // this will trigger the onload function above:
            if (file.size < 500000) {
                reader.readAsDataURL(file);
            } else {
                preview.find('.image-holder').append('<span class="filename">' + file.name + '</span>');
            }
            
            message.hide();
            preview.appendTo(dropbox);
            
            // Associating a preview container
            // with the file, using jQuery's $.data():
            
            $.data(file,preview);
        }

        function showMessage(msg){
            message.html(msg);
        }

    });

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

});
