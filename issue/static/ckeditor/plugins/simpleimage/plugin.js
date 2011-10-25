CKEDITOR.plugins.add( 'simpleimage',
{
	init: function( editor )
	{
		// Plugin logic goes here...
		
		editor.addCommand('insertCodeBlock', {
			exec : function( editor )
			{    
				editor.insertHtml( '<pre class="wikicode">&lt;%  %&gt;</pre>' );
			}
		})
		editor.addCommand( 'simpleImageDialog', new CKEDITOR.dialogCommand( 'simpleImageDialog' ) );
		editor.ui.addButton('SimpleImage', {
			label: 'Wiki Link',
			command: 'simpleImageDialog',
			icon: this.path + 'wikilink_icon.png'
		})
	}
} );

CKEDITOR.dialog.add( 'simpleImageDialog', function( editor )
		{
			return {
				title : 'Wiki Link',
				minWidth : 400,
				minHeight : 200,
				contents : [
					{
						id : 'general',
						label : 'Settings',
						elements :
						[
							{
								type : 'html',
								html : 'Wiki Link'		
							},
							{
								type : 'text',
								id : 'page_title',
								label : 'Page Title',
								required : true,
								commit : function( data ) {
									data.page_title = this.getValue();
								}
							}						 	// UI elements of the Settings tab.
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