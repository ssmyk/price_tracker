function add_item(user_id) {
    //let input = document.getElementsByClassName('form-control');
    let input = document.getElementById('link');

    let item = input.value;
    //document.write(item)
    let is_correct = validate_url(item);
    let asin = is_correct[0].substr(-10);
    let product_exists = check_product(asin);
    console.log(product_exists);

    console.log(11+asin);
    if (check_product(asin)==asin){
        document.getElementById("validator").innerHTML = 'Produkt jest już śledzony';
        console.log(check_product(asin));
        return;
}
    //document.write(is_correct)
    if (is_correct) {
        //document.write('Link poprawny')
        document.getElementById("validator").innerHTML = 'Link poprawny, ASIN: '+ asin;
        scraper_endpoint = window.location.protocol + '//' + window.location.hostname + ':5500/api/';
        //scraper_endpoint = 'http://scraper_api:5500/api/';
        //console.log(scraper_endpoint);
        data = {'asin':asin,'user_id': user_id};
        //console.log(JSON.stringify(data));
        //console.log(data);
        //fetch(scraper_endpoint, {method: 'POST', body: JSON.stringify(data), headers: {"Content-type": "application/json"}});
        w = add_to_tack(data)
        //console.log(w+1);
        //console.log(w['task_id']+2);
        //console.log(w.body);
        // jezeli response bedzie zawieral OK to wtedy odswiezamy
        // NOK wywalamy komunikat
    } else {
        // dynamiczny komunikat o niepoprawnym url
        document.getElementById("validator").innerHTML = 'Link niepoprawny'
    }
}

async function add_to_tack(data){
    resp = await fetch(scraper_endpoint, {method: 'POST', body: JSON.stringify(data), headers: {"Content-type": "application/json"}});
    w = await resp.json();
    return w
}

function validate_url(url) {
    re = /^(http:\/\/|https:\/\/)?(www\.amazon\.|amazon\.).+\/dp\/[0-9A-Z]{10}/
    return url.match(re)
}

async function check_product(asin){
    products_endpoint = window.location.protocol + '//' + window.location.host + '/products/asin/' + asin;

    try{
        let resp = await fetch(products_endpoint, {method: 'GET'});
        let obj = await resp.json();
        //console.log(resp)
        //console.log(obj)
        //console.log(obj['product_asin']);
        return (obj['product_asin']==asin);
        //if (obj['product_asin']==asin){
        //console.log('jest w bazie')
        //return true;
        //}
        //else{
        //console.log('nie ma w bazie')
        //return false;
        }

     catch(e){
        document.getElementById("validator").innerHTML = 'Service unavailable';
        return
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

