var dropBox;
var imgHolder;
var reportImg;
var templateImg;
var tmplPath;
var rpFile;

$(document).ready(function() {
	reportImg = $('#report-img');
	templateImg = $('#template-img');
	imgHolder = $('#img-holder');
	dropBox = $('#drop-image');

	InitialDropBox();
	
	DrawStoredMark();
	
	imgHolder.children().on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
		e.preventDefault();
	});
	
	InitialControl();
});

function InitialDropBox() {
	dropBox.on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
		e.preventDefault();
		e.stopPropagation();
	})
	.on('dragover dragenter', function(e) {
		$(this).addClass('is-dragover');
	})
	.on('drop dragleave dragend', function(e) {
		$(this).removeClass('is-dragover');
	})
	.on('drop', function(e) {
		var image = e.originalEvent.dataTransfer.files[0];
		if (image.type.match(/image.*/)) {
			HandleFileUpload(image);
		}
		else {
			alert("無効画像です。");
		}
	});
	
	$('#file-input').on('change', function(e) {
		if ($('#file-input').val() != "")
			HandleFileUpload(this.files[0]);
	});

	function HandleFileUpload(file) {
		DisableDropBox();
		img = reportImg;
		
		var reader = new FileReader();
		reader.onload = (e) => {
			img.attr('src', e.target.result);
			rpFile = file;
			CreateReportContainer();
		};
		reader.onprogress = (data) => {
			if (data.lengthComputable) {
				var progress = parseInt((data.loaded / data.total) * 100, 10);
				console.log(progress);
			}
		};
		reader.onerror = (e) => {
			EnableDropBox();
		};
		reader.readAsDataURL(file);
	};

	function DisableDropBox() {
		dropBox.hide();
		imgHolder.show();
		$('#crt-rp-btn').show();
	};
	
	function EnableDropBox() {
		dropBox.show();
		imgHolder.hide();
		$('#crt-rp-btn').hide();
	};
	
	function CreateReportContainer() {
		var rpCntr = $('<div/>').addClass('info').addClass('RpCntr');
		var header = $('<p/>').append('帳票ファイル:');
		rpCntr.append(header);
	
		var content = $('<p/>').css('padding-left', '20px').append(`ファイル名: ${rpFile.name}`);
		rpCntr.append(content);
	
		var removeButton = $('<i/>').addClass('remove-btn glyphicon glyphicon-remove');
		removeButton.on('click', function(e) {
			rpFile = null;
			EnableDropBox();
			$(this).parent()[0].remove();
			$('#file-input').val("");
		});
		rpCntr.append(removeButton);
	
		$('.info-container').prepend(rpCntr);
	};
}

function InitialControl() {
	var SLIDER_INITIAL_VALUE = 100;
	$('#opacity-slider').slider({
		create: () => $('#custom-slider').text(`${SLIDER_INITIAL_VALUE}%`),
		value: SLIDER_INITIAL_VALUE,
		slide: (event, ui) => {
			$('#custom-slider').text(`${ui.value}%`);
			templateImg.css('opacity', ui.value / 100);
		}
	});
	
	$('#display-template').on('change', function(e) {
		if(this.checked) {
			$('#opacity-control').show('Slide');
			templateImg.show();
		} else {
			$('#opacity-control').hide('Slide');
			templateImg.hide();
		}
	});
	
	$('#display-marks').on('change', function(e) {
		if(this.checked) {
			$('.mark').each((idx, element) => $(element).show());
		} else {
			$('.mark').each((idx, element) => $(element).hide());
		}
	});
	
	$('#crt-rp-btn').on('click', function(e) {
		formdata = new FormData();
		formdata.append("template-name", tmplPath);
		formdata.append("report", rpFile);
		
		GetCorrectImage(formdata).then(data => {
			var url = window.URL || window.webkitURL;
			reportImg.attr('src',  url.createObjectURL(data));
			$('.RpCntr, #tmpl-select').remove();
		}).catch(msg => alert(msg.responseText));
	});
	
	$('#tmpl-lst').on('change', function(e) {
		GetTemplate($(this).val()).then(data => {
			tmplURL = data["tmpl-img"];
			lstMark = data["img-coords"];
			templateImg.attr('src',  tmplURL);
			tmplPath = $(this).val();
			DrawStoredMark();
		}).catch(msg => alert(msg.responseText));
	});
}

function Mark() {
	this.x1 = 0;
	this.y1 = 0;
	this.x2 = 0;
	this.y2 = 0;
}

var lstMark = []
	
function DrawStoredMark() {
	lstMark.forEach((mark) => {
		var element = $('<div/>').addClass('mark').css({
			'top': Math.min(mark.y1, mark.y2),
			'left': Math.min(mark.x1, mark.x2),
			'width': Math.abs(mark.x1 - mark.x2),
			'height': Math.abs(mark.y1 - mark.y2)
		});
		
		if ($('#display-marks').prop('checked')) {
			element.show();
		} else {
			element.hide();
		}
		
		imgHolder.append(element);
	});
}