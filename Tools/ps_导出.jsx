var doc = app.activeDocument;
var file = new File(doc.path+"/"+doc.name.split(".")[0]+".jpg");

var opts = new ExportOptionsSaveForWeb();
opts.format = SaveDocumentType.JPEG;
opts.quality = 90;

doc.exportDocument(file, ExportType.SAVEFORWEB, opts);