function add_item(user_id) {

    let input = document.getElementById('link');

    let link_to_product = input.value;

    let asin = validate_url(link_to_product);
    if (!asin) {
        document.getElementById("validator").innerHTML = 'Link niepoprawny';
        return;
    }
    add_to_track(asin, user_id)


}

/*
if (is_correct) {
        //document.write('Link poprawny')
        document.getElementById("validator").innerHTML = 'Link poprawny, ASIN: '+ asin;
        scraper_endpoint = window.location.protocol + '//' + window.location.hostname + ':5500/api/';
        //scraper_endpoint = 'http://scraper_api:5500/api/';
        console.log(scraper_endpoint);
        data = {'asin':asin,'user_id': user_id};
        console.log(JSON.stringify(data));
        console.log(data);
        fetch(scraper_endpoint, {method: 'POST', body: JSON.stringify(data), headers: {"Content-type": "application/json"}});
        //fetch(scraper_endpoint, {method: 'POST', body: data, headers: {"Content-type": "application/json"}});
        // jezeli response bedzie zawieral OK to wtedy odswiezamy
        // NOK wywalamy komunikat
    } else {
        // dynamiczny komunikat o niepoprawnym url
        document.getElementById("validator").innerHTML = 'Link niepoprawny'
    }
*/
async function add_to_track(asin,user_id){
    scraper_endpoint = window.location.protocol + '//' + window.location.hostname + ':5500/api/';
    let data = {'asin':asin,'user_id': user_id};
    let resp = await fetch(scraper_endpoint, {method: 'POST', body: JSON.stringify(data), headers: {"Content-type": "application/json"}});
    let json = await resp.json();
    let task_id = json['task_id'];

    get_status(task_id);
    //console.log(status)
    //get_status_api = window.location.protocol + '//' + window.location.hostname + ':5500/status/' + task_id;
}

function get_status(task_id) {
    setTimeout(async function () {
    get_status_api = window.location.protocol + '//' + window.location.hostname + ':5500/status/' + task_id;
    let resp = await fetch(get_status_api);
    let status = await resp.json();
    console.log(status['task_status']);
    if (status['task_status'] == 'DUPLICATE'){
    location.reload();
    document.getElementById("validator").innerHTML = status['task_status'];
    return;
    }
    if (status['task_status'] == 'ADDED'){
    location.reload();
    document.getElementById("validator").innerHTML = status['task_status'];
    return;
    }
    if (status['task_status'] == 'ERROR'){
    location.reload();
    document.getElementById("validator").innerHTML = status['task_status'];
    return;
    }

    get_status(task_id);
    }, 1000);
}


function validate_url(url) {
    re = /^(http:\/\/|https:\/\/)?(www\.amazon\.|amazon\.).+\/dp\/[0-9A-Z]{10}/
    //return url.match(re);
    try{
        let asin = url.match(re)[0].substr(-10);
        return asin;
    } catch(e){
        return false;
    }

}


async function delete_item(product_id){
    tr_to_delete = product_id + "-tr";
    console.log(window.location.host)
    delete_endpoint = window.location.protocol + '//' + window.location.host + '/products/' + product_id;

    try{
        resp = await fetch(delete_endpoint, {method: 'DELETE'});
    } catch(e){
        document.getElementById("validator").innerHTML = 'Service unavailable';
        return
    }
    console.log(resp.status)
    if(resp.status == 200){
        document.getElementById(tr_to_delete).remove();
        document.getElementById("validator").innerHTML = 'Product was removed';
    }
    else {
        document.getElementById("validator").innerHTML = 'Internal error';
    }

}

