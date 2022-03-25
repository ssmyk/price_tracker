function add_item(user_id) {
    //let input = document.getElementsByClassName('form-control');
    let input = document.getElementById('link');

    let item = input.value;
    //document.write(item)
    let is_correct = validate_url(item);
    let asin = is_correct[0].substr(-10);

    check_product(asin)

    //document.write(is_correct)
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
}

function validate_url(url) {
    re = /^(http:\/\/|https:\/\/)?(www\.amazon\.|amazon\.).+\/dp\/[0-9A-Z]{10}/
    //asin = /[0-9A-Z]{10}/
    return url.match(re)
}

async function check_product(asin) {
    db_endpoint = window.location.protocol + '//' + window.location.hostname + ':5000/products';
    let resp = await fetch(db_endpoint, {method: 'GET'});
    let obj = await resp.json();
    //json = JSON.stringify(resp);
    console.log(obj);

    obj.forEach(function(item){
    console.log(item.product_asin);
    if (item.product_asin == asin) {
    document.getElementById("validator").innerHTML = 'BUMSZAKALKA!'
    }
    //document.getElementById("validator").innerHTML = item.product_asin;
    });
    }



async function delete_item(product_id){
    //console.log(product_id);
    //product_id = product_id.replace('-delete','')
    tr_to_delete = product_id + "-tr";
    //console.log(tr_to_delete);
    console.log(window.location.host)
    delete_endpoint = window.location.protocol + '//' + window.location.host + '/products/' + product_id;
    //delete_endpoint = 'http://172.18.0.3/products/' + product_id;
    //console.log(delete_endpoint);

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

