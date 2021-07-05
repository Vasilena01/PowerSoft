// document.querySelector wrapper
window.select = (selector) => {
	return document.querySelector(selector);
}

// document.querySelectorAll wrapper
window.select_all = (selector) => {
	return document.querySelectorAll(selector);
}

// post request function
window.post = async function (url='', data={}, cache='default', content_type='json') {
	let headers = {
		'X-CSRFToken': csrf_token,
    };

	if (content_type == 'json') {
		data = JSON.stringify(data);
		headers['Content-Type'] = 'application/json';
	}

	// Fetching
	const response = await fetch(url, {
		method: 'POST', // *GET, POST, PUT, DELETE, etc.
    	cache: cache, // *default, no-cache, reload, force-cache, only-if-cached
    	headers: headers,
    	body: data
	});

	const reponse_content_type = response.headers.get('content-type');
	if (reponse_content_type && reponse_content_type.indexOf('application/json') !== -1)
		return response.json();
	
	return response.text();
}

// get request function
window.get = async function (url='', data={}, cache='default') {
	// Construction the url
	let is_first = true;
	for (const key in data) {
		if (is_first) {
			url += '?' + key + '=' + data[key];
			is_first = false;
			continue;
		}

		url += '&' + key + '=' + data[key];
	}


	// Fetching
	const response = await fetch(url, {
		method: 'GET',
    	cache: cache, // *default, no-cache, reload, force-cache, only-if-cached
    	//headers: headers,
    	//body: data
	});

	const reponse_content_type = response.headers.get('content-type');
	if (reponse_content_type && reponse_content_type.indexOf('application/json') !== -1)
		return response.json();
	
	return response.text();
}

// Adds a default option to a select element
window.insert_default_option = (selector, text) => {
	select(`${selector}`).insertAdjacentHTML('afterbegin', `<option hidden disabled selected value=""> -- Select ${text} -- </option>`);
}

// Makes a field required and adds an asterisk if needed
window.make_field_required = (element, add_asterisk) => {
	element.setAttribute('required', 'required');
	if (add_asterisk)
		element.parentElement.querySelector('label').insertAdjacentHTML('beforeend', '<span class="input-required-asterisk"> *</span>');
}

// Makes a field unrequired and removes the asterisk if present
window.make_field_unrequired = (element) => {
	element.removeAttribute('required');
	let asterisk = element.parentElement.querySelector('label .input-required-asterisk');
	if (asterisk)
		asterisk.remove();
}

// Copy the string given to the clipboard (+ some tooltip & icons stuff)
window.copy2clipboard = (str) => {
    const el = document.createElement('textarea');
    el.value = str;
    el.setAttribute('readonly', '');
    el.style.position = 'absolute';
    el.style.left = '-9999px';
    document.body.appendChild(el);
    const selected = 
        document.getSelection().rangeCount > 0
            ? document.getSelection().getRangeAt(0)
            : false;
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    if (selected) {
        document.getSelection().removeAllRanges();
        document.getSelection().addRange(selected);
    }

    let btn = select('.share-btns .url-btn');
    let icon = btn.querySelector('svg.fa-link')
	icon.classList.remove('fa-link')
	icon.classList.add('fa-check');
    btn.setAttribute('data-bs-original-title', 'Линкът е копиран!');
	let tooltip = new Tooltip(btn);
	tooltip.show();

    setTimeout(() => {
        let icon = btn.querySelector('svg.fa-check');
		icon.classList.remove('fa-check');
		icon.classList.add('fa-link');
        btn.setAttribute('data-bs-original-title', 'Копирай Линка');
		tooltip.hide();
    }, 3000);
}

// TinyMCE initialization function
window.tinymce_init = (img_upload_url, img_del_url, selector='.tinymce', height=500) => {
	tinymce.init({
		selector: selector,
		height: height,
		menubar: false,
		plugins: [
			'code link image media preview anchor fullscreen lists'
		],
		toolbar: [
			'undo redo | formatselect | bold italic strikethrough superscript subscript | numlist bullist | anchor link image media | preview code fullscreen'
		],
		block_formats: 'Paragraph=p; Header 1=h1; Header 2=h2; Header 3=h3; Blockquote=blockquote',
		image_title: true,
		image_class_list: [
			{title: 'Fluid', value: 'img-fluid rounded'},
		],
		// Upload image handler
		images_upload_handler: (blob_info, success, failure) => {
    	    let data = new FormData();
    	    data.append('file', blob_info.blob(), blob_info.filename());
			post(img_upload_url, data, 'no-cache', 'form')
				.then(response => {
					if (response.status)
						success(response.data.url);
					else
						failure(response.msg);
				})
				.catch(error => {
					failure('Image upload failed');
				});
    	},
		setup: (editor) => {
			// Delete image handler
			editor.on('KeyDown', (e) => {
			    if ((e.keyCode == 8 || e.keyCode == 46) && editor.selection) { // delete & backspace keys
			        let node = editor.selection.getNode();
			        if (node && node.nodeName == 'IMG')
						post(img_del_url, {src: node.src}, 'no-cache');
			    }
			});
		},
	});
};
