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
    	id:'simpleImageDialog',
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
                        },
                    	setup:function(data) {
                    		this.setValue(data.url)
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
        	var dialog = this
            $('.cke_dialog_ui_input_file').load(function() {
                var bodyHTML = this.contentWindow.document.body.innerHTML
                if (bodyHTML.indexOf('<') < 0) {
                	var data = { url:bodyHTML }
                	dialog.setupContent(data)
                }
            })
        },
        onOk:function() {
            var dialog = this, data = {}, link = editor.document.createElement('img');
            this.commitContent(data);
            link.setAttribute('src', data.url);
            editor.insertElement(link)
        }
    };
});