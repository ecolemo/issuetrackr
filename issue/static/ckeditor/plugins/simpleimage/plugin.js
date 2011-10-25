CKEDITOR.plugins.add( 'simpleimage',
{
	init: function( editor )
	{
		// Plugin logic goes here...

		editor.addCommand('insertSimpleImage', {
			exec : function( editor )
			{
                // TODO

			}
		})
		editor.addCommand( 'simpleImageDialog', new CKEDITOR.dialogCommand( 'simpleImageDialog' ) );
		editor.ui.addButton('SimpleImage', {
			label: 'Insert Image',
			command: 'simpleImageDialog',
			icon: this.path + 'simpleimage.png'
		})
	}
} );

CKEDITOR.dialog.add( 'simpleImageDialog', function( editor )
		{
			return {
				title : 'Insert Image',
				minWidth : 400,
				minHeight : 200,
				contents : [
					{
						id : 'general',
						label : 'Settings',
						elements :
						[
							{
								type : 'text',
								id : 'url',
								label : '이미지 URL',
								required : true,
								commit : function( data ) {
									data.url = this.getValue();
								}
							},
                            {
                      			type : 'file',
                      			id : 'upload',
                      			label : '이미지 올리기',
                      			style: 'height:40px',
                      			size : 38
                      		},
                            {
                                type : 'button',
                                id : 'uploadButton',
                                label : editor.lang.image.btnUpload
                            }
						]
					}
				],
				onOk : function() {
					var dialog = this,
					data = {},
					link = editor.document.createElement( 'a' );
					this.commitContent( data );
					link.setAttribute( 'href', '/' + data.page_title );
					link.setHtml(data.page_title)
					editor.insertElement(link)
				}
			};
		});