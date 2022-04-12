async function add_item(user_id) {
	let input = document.getElementById('link');
	let link_to_product = input.value;
	let asin = validate_url(link_to_product);
	if(!asin) {
		document.getElementById("validator").innerHTML = 'Invalid URL';
		return;
	}
	task_id = await add_to_track(asin, user_id)
	get_status(task_id);
}
async function add_to_track(asin, user_id) {
	scraper_endpoint = window.location.protocol + '//' + window.location.hostname + ':5500/api/';
	let data = {
		'asin': asin,
		'user_id': user_id
	};
	let resp = await fetch(scraper_endpoint, {
		method: 'POST',
		body: JSON.stringify(data),
		headers: {
			"Content-type": "application/json"
		}
	});
	let json = await resp.json();
	let task_id = json['task_id'];
	return task_id
}

function get_status(task_id) {
	setTimeout(async function() {
		get_status_api = window.location.protocol + '//' + window.location.hostname + ':5500/status/' + task_id;
		let resp = await fetch(get_status_api);
		let status = await resp.json();
		console.log(status['task_status']);
		let loading = '<h4>Please wait...<div class="lds-facebook"><div></div><div></div><div></div></div></h4>'
		document.getElementById("validator").innerHTML = loading;
		let current_status = status['task_status']
		if(current_status == 'DUPLICATE') {
			document.getElementById("validator").innerHTML = 'Product is already tracked';
			wait_for_clear();
			return;
		}
		if(current_status == 'CREATED') {
			document.getElementById("validator").innerHTML = 'Product was added to track';
			page_reload();
			return;
		}
		if(current_status == 'ERROR') {
			document.getElementById("validator").innerHTML = 'Internal error';
			wait_for_clear();
			return;
		}
		get_status(task_id);
	}, 1000);
}

function page_reload() {
	setTimeout(function() {
		location.reload();
	}, 3000);
}

function wait_for_clear() {
	setTimeout(function() {
		document.getElementById("validator").innerHTML = '';
	}, 3000);
}

function refresh_all() {
	refresh_api = window.location.protocol + '//' + window.location.hostname + ':5500/api/';
	fetch(refresh_api, {
		method: 'PATCH'
	});
}

function validate_url(url) {
	re = /^(http:\/\/|https:\/\/)?(www\.amazon\.|amazon\.).+\/dp\/[0-9A-Z]{10}/
	try {
		let asin = url.match(re)[0].substr(-10);
		return asin;
	} catch(e) {
		return false;
	}
}
async function delete_item(product_id) {
	tr_to_delete = product_id + "-tr";
	delete_endpoint = window.location.protocol + '//' + window.location.host + '/products/' + product_id;
	try {
		resp = await fetch(delete_endpoint, {
			method: 'DELETE'
		});
	} catch(e) {
		document.getElementById("validator").innerHTML = 'Service unavailable';
		page_reload();
		return
	}
	if(resp.status == 200) {
		document.getElementById(tr_to_delete).remove();
		document.getElementById("validator").innerHTML = 'Product was removed';
		page_reload();
	} else {
		document.getElementById("validator").innerHTML = 'Internal error';
		page_reload();
	}
}