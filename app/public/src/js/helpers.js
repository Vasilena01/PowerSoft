// document.querySelector wrapper
window.select = (selector) => {
	return document.querySelector(selector)
}

// document.querySelectorAll wrapper
window.select_all = (selector) => {
	return document.querySelectorAll(selector)
}

// post request function
window.post = async function (url='', data={}, cache='default', content_type='json') {
	let headers = {
		'X-CSRFToken': csrf_token,
    }

	if (content_type == 'json') {
		data = JSON.stringify(data)
		headers['Content-Type'] = 'application/json'
	}

	// Fetching
	const response = await fetch(url, {
		method: 'POST', // *GET, POST, PUT, DELETE, etc.
    	cache: cache, // *default, no-cache, reload, force-cache, only-if-cached
    	headers: headers,
    	body: data
	})

	const reponse_content_type = response.headers.get('content-type')
	if (reponse_content_type && reponse_content_type.indexOf('application/json') !== -1)
		return response.json()
	
	return response.text()
}

// get request function
window.get = async function (url='', data={}, cache='default') {
	// Construction the url
	let is_first = true
	for (const key in data) {
		if (is_first) {
			url += '?' + key + '=' + data[key]
			is_first = false
			continue
		}

		url += '&' + key + '=' + data[key]
	}


	// Fetching
	const response = await fetch(url, {
		method: 'GET',
    	cache: cache, // *default, no-cache, reload, force-cache, only-if-cached
    	//headers: headers,
    	//body: data
	})

	const reponse_content_type = response.headers.get('content-type')
	if (reponse_content_type && reponse_content_type.indexOf('application/json') !== -1)
		return response.json()
	
	return response.text()
}

// Adds a default option to a select element
window.insert_default_option = (selector, text) => {
	select(`${selector}`).insertAdjacentHTML('afterbegin', `<option hidden disabled selected value=""> -- Select ${text} -- </option>`)
}

// Makes a field required and adds an asterisk if needed
window.make_field_required = (element, add_asterisk) => {
	element.setAttribute('required', 'required')
	if (add_asterisk)
		element.parentElement.querySelector('label').insertAdjacentHTML('beforeend', '<span class="input-required-asterisk"> *</span>')
}

// Makes a field unrequired and removes the asterisk if present
window.make_field_unrequired = (element) => {
	element.removeAttribute('required')
	let asterisk = element.parentElement.querySelector('label .input-required-asterisk')
	if (asterisk)
		asterisk.remove()
}

// Open modal
window.open_modal = (id) => {
	select(`#${id}`).style.display = 'block'
	select('body').classList.add('no-scroll')
}

// Close modal
window.close_modal = (id, e) => {
	if (e && !e.target.classList.contains('btn-close') && !e.target.classList.contains('modal'))
		return

	select(`#${id}`).style.display = 'none'
	select('body').classList.remove('no-scroll')
}

// Toggle the navbar for mobile devices
window.toggle_navbar = () => {
	let navbar_toggler = select('#navbar-toggler')

	if (!navbar_toggler.classList.contains('navbar-expanded')) {
		select('body').classList.add('no-scroll')
		select('#main-navbar').classList.add('navbar-expanded')
		navbar_toggler.classList.add('navbar-expanded')
		return
	}

	select('body').classList.remove('no-scroll')
	select('#main-navbar').classList.remove('navbar-expanded')
	navbar_toggler.classList.remove('navbar-expanded')
}

// Creates a counter element
window.counter = (element_id, interval) => {
	let element = select(`#${element_id}`)

  	window[`interval_${element_id}`] = setInterval(() => {
		// Adding 1 to the current number of the element
		element.textContent = parseInt(element.textContent) + 1

		// If the counter is equal or greater than the endNumber set
  	  	if (parseInt(element.textContent) >= element.dataset.endNumber) {
			// Setting the number of the element to the endNumber
			element.textContent = element.dataset.endNumber
			// Clearing the interval
			clearInterval(window[`interval_${element_id}`])
		}
  	}, interval)
}

// Calling a function when the element given is visible on the screen
window.call_on_scroll_into_view = (element, callback, args) => {
	// Getting the bounding of the element
	let bounding = element.getBoundingClientRect()

	// Checker function for the position of the element in accordance to the screen
	const check_and_call = () => {
		if (bounding.top < (window.scrollY + window.innerHeight)){
	        callback(...args)
	        window.removeEventListener('scroll', check_and_call)
			return true
	    }
	}

	// Initial check
	if (check_and_call())
		return

	// If the element was not initally visible, asisgning a scroll listener
	window.addEventListener('scroll', check_and_call)
}


// Copy the string given to the clipboard (+ some tooltip & icons stuff)
window.copy2clipboard = (str) => {
    const el = document.createElement('textarea')
    el.value = str
    el.setAttribute('readonly', '')
    el.style.position = 'absolute'
    el.style.left = '-9999px'
    document.body.appendChild(el)
    const selected = 
        document.getSelection().rangeCount > 0
            ? document.getSelection().getRangeAt(0)
            : false
    el.select()
    document.execCommand('copy')
    document.body.removeChild(el)
    if (selected) {
        document.getSelection().removeAllRanges()
        document.getSelection().addRange(selected)
    }

	change_icon('.share-btns .url-btn .icon-link', 'check')
    //msg({status: 'success', msg: 'Линкът е копиран!'});

    setTimeout(() => {
		change_icon('.share-btns .url-btn .icon-check', 'link')
    }, 3000)
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
		block_formats: 'Paragraph=p; Header 2=h2; Header 3=h3; Blockquote=blockquote',
		image_title: true,
		image_class_list: [
			{title: 'Fluid', value: 'img-fluid'},
		],
		// Upload image handler
		images_upload_handler: (blob_info, success, failure) => {
    	    let data = new FormData()
    	    data.append('file', blob_info.blob(), blob_info.filename())
			post(img_upload_url, data, 'no-cache', 'form')
				.then(response => {
					if (response.status)
						success(response.data.url)
					else
						failure(response.msg)
				})
				.catch(error => {
					failure('Image upload failed')
				})
    	},
		setup: (editor) => {
			// Delete image handler
			editor.on('KeyDown', (e) => {
			    if ((e.keyCode == 8 || e.keyCode == 46) && editor.selection) { // delete & backspace keys
			        let node = editor.selection.getNode()
			        if (node && node.nodeName == 'IMG')
						post(img_del_url, {src: node.src}, 'no-cache')
			    }
			})
		},
	})
}
