function add_item(user_id) {
    //let input = document.getElementsByClassName('form-control');
    let input = document.getElementById('link');
    //console.log(input);
    let item = input.value;
    //document.write(item)
    let is_correct = validate_url(item);

    //document.write(is_correct)
    if (is_correct) {
        //document.write('Link poprawny')
        let asin = is_correct[0].substr(-10);
        document.getElementById("validator").innerHTML = 'Link poprawny, ASIN: '+ asin;
        scraper_endpoint = window.location.protocol + '//' + window.location.hostname + ':5500/';
        console.log(scraper_endpoint);
        data = {'asin':asin,'user_id': user_id}
        console.log(JSON.stringify(data));
        console.log(data);
        fetch(scraper_endpoint, {method: 'POST', body: JSON.stringify(data), headers: {"Content-type": "application/json"}});
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

