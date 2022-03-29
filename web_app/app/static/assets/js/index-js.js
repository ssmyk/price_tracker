function add_item(user_id) {

    let input = document.getElementById('link');

    let link_to_product = input.value;

    let asin = validate_url(link_to_product);
    if (!asin) {
        document.getElementById("validator").innerHTML = 'Link niepoprawny';
        return;
    }

    let product_exists = check_asin_in_db(asin);
    //document.getElementById("validator").innerHTML = product_exists;
    if (product_exists==true) {
        document.getElementById("validator").innerHTML = 'Produkt jest już śledzony';
        return;
    }


}

async function add_to_track(data){
    resp = await fetch(scraper_endpoint, {method: 'POST', body: JSON.stringify(data), headers: {"Content-type": "application/json"}});
    w = await resp.json();
    return w
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

function check_asin_in_db(asin){
    products_endpoint = window.location.protocol + '//' + window.location.host + '/products/asin/' + asin;

    try{
        fetch(products_endpoint, {method: 'GET'})
        .then(resp => resp.json())
        .then(resp => console.log(resp))
        return resp
        //console.log(obj['product_asin']==asin);
        //return (obj['product_asin']==asin);
        //return obj['product_asin']==asin;
        }
     catch(e){
        document.getElementById("validator").innerHTML = 'Service unavailable';
        return;
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

