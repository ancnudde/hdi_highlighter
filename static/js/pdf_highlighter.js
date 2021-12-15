let current_page = 0;
let selection = 0;

function matches_switch(area) {
	// Hide or reveal list of matches.
	var matches_box = document.getElementById(area);
	if (matches_box.style.height != '0px') {
		matches_box.style.height = '0px';
	} else {
		matches_box.style.height = '70%';
		matches_box.style.border = '3pt solid #646D7E';
	}
}

function change_page(dir) {
	// Changes current page to previous/next one.
	let text_area = document.getElementById('extracted_pdf');
	if (dir == -1 && current_page < 1) {
		return null;
	}
	if (dir == 1 && current_page >= $('[id^="page"]').length - 1) {
		return null;
	}
	$(`#page-${current_page}`).css('display', 'none');
	current_page += parseInt(dir);
	$(`#page-${current_page}`).css('display', 'flex');
	$('#current_page').html(current_page + 1);
	text_area.scrollTo(text_area.offsetWidth / 2, 0);
}

function scroll_to_block(idx, category) {
	// Scroll to block of text corresponding to match.
	let focused_element = document.getElementById(`${category}-${idx}`);
	let page = focused_element.parentElement.parentElement.parentElement.id;
	$(`#page-${current_page}`).css('display', 'none');
	current_page = parseInt(page.slice(5));
	$(`#page-${current_page}`).css('display', 'flex');
	$('#current_page').html(current_page + 1);
	document.getElementById(`${category}-${idx}`).scrollIntoView();
}

function hover_nav(e, indices, category, step) {
	let counter = document.getElementById(e).parentElement.children[1];
	let max_count = indices.length;
	let count = parseInt(counter.innerHTML);
	if (step == -1 && count <= 1) {
		return null;
	}
	if (step == 1 && count >= max_count) {
		return null;
	}
	counter.innerHTML = count + parseInt(step);
	let current = indices[count + parseInt(step) - 1];
	scroll_to_block(current, category);
};

function go_to_current(e, indices, category) {
	// Goes to current occurence of the clicked term.
	let current = parseInt(document.getElementById(e).children[1].children[1].innerHTML);
	scroll_to_block(indices[current - 1], category);
}

function switch_highlight(match) {
	// Hides/highlights matches of a given grammar.
	let matched = $(`.${match}`);
	if ($(matched[0]).attr('disabled') == 'disabled') {
		$(`.highlight.${match}`).attr("disabled", false);
	} else {
		$(`.highlight.${match}`).attr("disabled", true);
	}
	// Makes selector opaque when hidden.
	let highlight_switch = document.getElementsByName(match)[0];
	if (highlight_switch.style.opacity == 1) {
		highlight_switch.style.opacity = 0.3;
	} else {
		highlight_switch.style.opacity = 1;
	}
}

function open_tab(evt, category) {
	var i, tabcontent, tablinks;
	// Get all elements with class="tabcontent" and hide them
	tabcontent = document.getElementsByClassName("tabcontent");
	for (i = 0; i < tabcontent.length; i++) {
		tabcontent[i].style.display = "none";
	}
	// Get all elements with class="tablinks" and remove the class "active"
	tablinks = document.getElementsByClassName("tablinks");
	for (i = 0; i < tablinks.length; i++) {
		tablinks[i].className = tablinks[i].className.replace(" active", "");
	}
	// Show current tab, and add "active" class to button that opened tab
	document.getElementById(`current_${category}`).style.display = "block";
	evt.currentTarget.className += " active";
}

function fit_text_area() {
	// Fit extracted text to text area.
	let text_area = document.getElementById('extracted_pdf');
	let page = document.getElementById(`page-${current_page}`);
	let target_width = text_area.offsetWidth;
	let origin_width = page.offsetWidth;
	let scale_factor = target_width / origin_width;
	page.style.transform = `scale(${scale_factor}, ${scale_factor})`;
	text_area.scrollTo(target_width / 2, 0);
}

function toogle_selection() {
	// Activate/deactivate scrolling by mouse.
	var down = false;
	var scrollLeft = 0;
	var x = 0;
	var scrollTop = 0;
	var y = 0;
	var timer = 0;
	var delay = 200;
	var prevent = false;
	$('#extracted_pdf').mousedown(function(e) {
		e.preventDefault();
		down = true;
		scrollLeft = this.scrollLeft;
		x = e.clientX;
		scrollTop = this.scrollTop;
		y = e.clientY;
	}).mouseup(function() {
		down = false;
	}).mousemove(function(e) {
		if (down) {
			this.scrollLeft = scrollLeft + x - e.clientX;
			this.scrollTop = scrollTop + y - e.clientY;
		}
	}).mouseleave(function() {
		down = false;
	});
}


window.onload = function() {
	// Moves click action from form to button for better visual.
	$('#upload').click(function() {
		$('#file').click();
	});
	$('#process').click(function() {
		let filename = $('#filename').html();
		$('#pdf_view').attr('src', 'static/uploads/' + filename);
		$('#apply').click();
	});
	// Make legend items clickable for highlight switching.
	let legends = document.getElementsByClassName('legend__box');
	Array.from(legends).forEach(element => {
		element.addEventListener('click', function() {
			let val = $(element).attr('name');
			switch_highlight(val);
		});
	});
	document.getElementById('terms_switch').addEventListener('click', () => {
		matches_switch('terms');
	});
	var terms = document.getElementById('terms');
	terms.ontransitionend = () => {
		if (terms.style.border && terms.style.height == '0px') {
			terms.style.border = null;
		}
	};
	// File upload listener to show uploaded file name.
	$("#file").change(function() {
		$("#filename").text(this.files[0].name);
		$('#original_pdf').attr('src', this.files[0].name);
	});
	// Click listener to switch original/extracted PDF.
	$("#to_original").click(function() {
		$("#original_pdf").css('display', 'block');
		$("#extracted_pdf").css('display', 'none');
	});
	$("#to_extracted").click(function() {
		$("#extracted_pdf").css('display', 'flex');
		$("#original_pdf").css('display', 'none');
	});
	$('[id^="page"]').css({
		'display': 'none',
		'background-color': 'transparent',
		'transform-origin': '0 0'
	});
	$('#page-0').css('display', 'flex');
	$('#zoom').val(10);
	$('#zoom').on('input', function() {
		let stretch_val = parseInt($('#zoom').val()) / 10;
		$(`[id^="page"]`).css('transform',
			`scale(${stretch_val}, ${stretch_val})`);
	});
	$('#zoom_in').click(function() {
		$('#zoom').val(parseInt($('#zoom').val()) + 5);
		let stretch_val = parseInt($('#zoom').val()) / 10;
		$(`[id^="page"]`).css('transform',
			`scale(${stretch_val}, ${stretch_val})`);
	});
	$('#zoom_out').click(function() {
		$('#zoom').val(parseInt($('#zoom').val()) - 5);
		let stretch_val = parseInt($('#zoom').val()) / 10;
		$(`[id^="page"]`).css('transform',
			`scale(${stretch_val}, ${stretch_val})`);
	});
	toogle_selection();
	$("#selection_tool").on("click", function() {
		if (selection == 0) {
			$('#extracted_pdf').off('mousedown');
			selection = 1;
			$("#extracted_pdf").css('cursor', 'text');
		} else {
			toogle_selection();
			selection = 0;
			$("#extracted_pdf").css('cursor', 'grab');
		}
	});
	$('#total_pages').html(`/ ${$('[id^="page"]').length}`);
	$('#current_page').html(current_page + 1);
	$('#fit_page').click(function() {
		fit_text_area();
	});
	const source = document.querySelector('#extracted_pdf');
	source.addEventListener('copy', (event) => {
		const selection = document.getSelection();
		event.clipboardData.setData(
			'text/plain', selection.toString().replace(/\r?\n|\r/g, ""));
		event.preventDefault();
	});

};


