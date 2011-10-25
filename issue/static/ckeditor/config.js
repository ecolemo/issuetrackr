CKEDITOR.editorConfig = function( config ) {
	config.protectedSource.push()
	config.toolbar = 'Wiki'
	config.toolbar_Wiki =
	[
		{ name: 'colors', items : [ 'TextColor','BGColor' ] },
//		{ name: 'styles', items : [ 'Format','Font','FontSize' ] },
		{ name: 'basicstyles', items : [ 'Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat' ] },
		{ name: 'paragraph', items : [ 'Format', 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','CreateDiv','-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl' ] },
		'/',
		{ name: 'links', items : [ 'WikiLink', 'Link','Unlink','Anchor', 'WikiCodeBlock' ] },
		{ name: 'insert', items : [ 'Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak','Iframe' ] },
		{ name: 'editing', items : [ 'Find','Replace','-','SelectAll','-','SpellChecker', 'Scayt' ] },
		{ name: 'clipboard', items : [ 'Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ] },
//		{ name: 'tools', items : [ 'Maximize', 'ShowBlocks','-','About', '-', 'Source' ] },
//		{ name: 'forms', items : [ 'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField' ] },
	];
	config.keystrokes.push([CKEDITOR.CTRL + 32, 'WikiLink'])
	config.tabSpaces = 4;
	config.removePlugins = 'tab';
	config.filebrowserUploadUrl = '/attachments/_/create'
}
