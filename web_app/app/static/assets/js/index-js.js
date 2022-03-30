function add_item(user_id) {

    let input = document.getElementById('link');

    let link_to_product = input.value;

    let asin = validate_url(link_to_product);
    if (!asin) {
        document.getElementById("validator").innerHTML = 'Link niepoprawny';
        return;
    }
    add_to_track(asin,user_id)
/*

    let product_exists = check_asin_in_db(asin);
    console.log(product_exists.json())
    //let product_exists = check_asin_in_db(asin).then(value => console.log(value));

    //document.getElementById("validator").innerHTML = product_exists;
    if (product_exists) {
        document.getElementById("validator").innerHTML = 'Produkt jest już śledzony';
        return;
    }

*/
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
    data = {'asin':asin,'user_id': user_id};
    resp = await fetch(scraper_endpoint, {method: 'POST', body: JSON.stringify(data), headers: {"Content-type": "application/json"}});
    task_id = await resp.json();
    //get_status(task_id);
    console.log(task_id)

}


function get_status(task_id){
    get_status_api = window.location.protocol + '//' + window.location.hostname + ':5500/status/' + task_id;


    fetch(get_status_api)
        .then(res => {
            // console.log(res)
            const task_status = res.task_status;

            // console.log(taskResult)
            if (taskStatus === 'FAILURE') {
                console.log('error');
                return false
            }else if(taskStatus === 'SUCCESS'){
                console.log(taskResult);
                return true
            }
            setTimeout(function (){
                // console.log(taskStatus);
                getStatus(res.task_id);
            }, 1000)
        })
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
/*
function check_asin_in_db(asin){
    products_endpoint = window.location.protocol + '//' + window.location.host + '/products/asin/' + asin;

    let resp = fetch(products_endpoint, {method: 'GET'})
    .then(resp => resp.json())
    .then(data => console.log(data));
    return data

    }

*/

async function check_asin_in_db(asin){
    products_endpoint = window.location.protocol + '//' + window.location.host + '/products/asin/' + asin;

    let resp = await fetch(products_endpoint, {method: 'GET'});
    let obj = await resp.json();
    return obj;

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

