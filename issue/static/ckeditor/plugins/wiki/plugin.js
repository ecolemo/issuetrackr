CKEDITOR.plugins.add( 'wiki',
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
		editor.addCommand('wikiLink', {
			exec : function( editor )
			{    
				editor.insertHtml( '<pre class="wikicode">% </pre>' );
			}
		})
		editor.addCommand( 'wikiLinkDialog', new CKEDITOR.dialogCommand( 'wikiLinkDialog' ) );
		editor.ui.addButton('WikiCodeBlock', {
			label: 'Insert Code Block snippet',
			command: 'insertCodeBlock',
			icon: this.path + 'codeblock.png'
		})
		editor.ui.addButton('WikiLink', {
			label: 'Wiki Link',
			command: 'wikiLinkDialog',
			icon: this.path + 'wikilink_icon.png'
		})
	}
} );

CKEDITOR.dialog.add( 'wikiLinkDialog', function( editor )
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