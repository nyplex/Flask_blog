CKEDITOR.config.allowedContent = true;
CKEDITOR.config.removeFormatAttributes = '';
CKEDITOR.config.toolbarGroups =  [
    { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
    { name: 'editing', groups: [ 'find', 'selection', 'spellchecker', 'editing' ] },
    { name: 'document', groups: [ 'mode', 'document', 'doctools' ] },
    { name: 'forms', groups: [ 'forms' ] },
    { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
    { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
    { name: 'links', groups: [ 'links' ] },
    { name: 'insert', groups: [ 'insert' ] },
    { name: 'styles', groups: [ 'styles' ] },
    { name: 'colors', groups: [ 'colors' ] },
    { name: 'tools', groups: [ 'tools' ] },
    { name: 'others', groups: [ 'others' ] },
    { name: 'about', groups: [ 'about' ] }
];
CKEDITOR.config.editorplaceholder = "Let's get started"
CKEDITOR.config.removeButtons = 'Source,Save,NewPage,ExportPdf,Preview,Print,Templates,Cut,Paste,PasteText,PasteFromWord,Find,Replace,SelectAll,Scayt,Form,Checkbox,Radio,TextField,Textarea,Select,Button,ImageButton,HiddenField,Subscript,Superscript,RemoveFormat,CopyFormatting,Blockquote,CreateDiv,Indent,Outdent,BidiLtr,BidiRtl,Language,Unlink,Image,Table,SpecialChar,PageBreak,Iframe,Styles,Format,Maximize,ShowBlocks,About';