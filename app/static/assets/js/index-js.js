function add_item() {
    let input = document.getElementsByClassName('form-control')[0];
    let item = input.value;
    //document.write(item)
    let is_correct = validate_url(item);
    //document.write(is_correct)
    if (is_correct) {
        //document.write('Link poprawny')
        document.getElementById("validator").innerHTML = 'Link poprawny'
        // jezeli response bedzie zawieral OK to wtedy odswiezamy
        // NOK wywalamy komunikat
    } else {
        // dynamiczny komunikat o niepoprawnym url
        document.getElementById("validator").innerHTML = 'Link niepoprawny'
    }
}

function validate_url(url) {
    re = /^(http:\/\/|https:\/\/)?(www\.amazon\.|amazon\.).+\/dp\/[0-9A-Z]{10}/
    return url.match(re)
}

async function delete_item(product_id){
    //console.log(product_id);
    //product_id = product_id.replace('-delete','')
    tr_to_delete = product_id + "-tr"
    //console.log(tr_to_delete);
    delete_endpoint = 'http://10.1.1.11:5000/products/' + product_id
    //console.log(delete_endpoint);
    document.getElementById(tr_to_delete).remove()
    resp = await fetch(delete_endpoint, {method: 'DELETE'});
    if(resp.status == 200){
        document.getElementById("validator").innerHTML = 'Product was removed'
    }
    else {
        document.getElementById("validator").innerHTML = 'Internal error'
    }


}

