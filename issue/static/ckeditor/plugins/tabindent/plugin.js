CKEDITOR.plugins.add( 'tabindent', {
	init: function( editor ) {
		editor.on( 'key', function( ev ) {
			if (ev.data.keyCode == 9) {
				editor.execCommand('indent')
				ev.cancel()
			} else if (ev.data.keyCode == CKEDITOR.SHIFT + 9) {
				editor.execCommand('outdent')
				ev.cancel()
			}
		});
	}
});
