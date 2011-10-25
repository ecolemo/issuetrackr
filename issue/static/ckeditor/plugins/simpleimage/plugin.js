CKEDITOR.plugins.add('simpleimage',
    {
        init:function(editor) {
            // Plugin logic goes here...

            editor.addCommand('insertSimpleImage', {
                exec:function(editor) {
                    // TODO

                }
            })
            editor.addCommand('simpleImageDialog', new CKEDITOR.dialogCommand('simpleImageDialog'));
            editor.ui.addButton('SimpleImage', {
                label:'Insert Image',
                command:'simpleImageDialog',
                icon:this.path + 'simpleimage.png'
            })
        }
    });

CKEDITOR.dialog.add('simpleImageDialog', function(editor) {
    return {
        title:'Insert Image',
        minWidth:400,
        minHeight:200,
        contents:[
            {
                id:'Upload',
                hidden:true,
                filebrowser:'uploadButton',
                label:editor.lang.image.upload,
                elements:[
                    {
                        type:'text',
                        id:'url',
                        label:'이미지 URL',
                        required:true,
                        commit:function(data) {
                            data.url = this.getValue();
                        }
                    },
                    {
                        type:'file',
                        id:'upload',
                        label:'이미지 올리기',
                        style:'height:40px',
                        size:38
                    },
                    {
                        type:'fileButton',
                        id:'uploadButton',
                        filebrowser:'info:txtUrl',
                        label:editor.lang.image.btnUpload,
                        'for':[ 'Upload', 'upload' ]
                    }
                ]
            }
        ],
        onLoad:function() {
            $('.cke_dialog_ui_input_file').load(function() {
                bodyHTML = this.contentWindow.document.body.innerHTML
                if (bodyHTML.indexOf('<') < 0) {
                    alert($('.url_input'))
                    $('.').val(bodyHTML);
                }
            })
        },
        onOk:function() {
            var dialog = this, data = {}, link = editor.document.createElement('a');
            this.commitContent(data);
            link.setAttribute('href', '/' + data.page_title);
            link.setHtml(data.page_title)
            editor.insertElement(link)
        }
    };
});