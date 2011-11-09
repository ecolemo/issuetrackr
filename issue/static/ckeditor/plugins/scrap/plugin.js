/*
 * @example An iframe-based dialog with custom button handling logics.
 */
( function() {
    CKEDITOR.plugins.add('scrap',
        {
            requires:[ 'iframedialog' ],
            init:function(editor) {
                var me = this;
                CKEDITOR.dialog.add('ScrapDialog', function() {
                    return {
                        title:'Scrap',
                        minWidth:550,
                        minHeight:200,
                        contents:[
                            {
                                id:'iframeScrap',
                                label:'Scrap',
                                expand:true,
                                elements:[
                                    {
                                        type:'html',
                                        id:'pageScrap',
                                        label:'Scrap',
                                        style:'width : 100%;',
                                        html:'<iframe src="' + me.path + '/dialogs/scrap.html" frameborder="0" name="iframeScrap" id="iframeScrap" allowtransparency="1" style="width:100%;margin:0;padding:0;"></iframe>'
                                    }
                                ]
                            }
                        ],
                        onOk:function() {
                            for (var i = 0; i < window.frames.length; i++) {
                                if (window.frames[i].name == 'iframeScrap') {
                                    var content = window.frames[i].document.getElementById("embed").value;
                                }
                            }
                            var final_html = '<div class="add_scrap">' + content + '</div>';
                            editor.insertHtml(final_html);
                            var updated_editor_data = editor.getData();
                            editor.setData(updated_editor_data);
                        }
                    };
                });

                editor.addCommand('Scrap', new CKEDITOR.dialogCommand('ScrapDialog'));

                editor.ui.addButton('Scrap',
                    {
                        label:'Scrap',
                        command:'Scrap',
                        icon:this.path + 'images/icon.gif'
                    });
            }
        });
} )();
