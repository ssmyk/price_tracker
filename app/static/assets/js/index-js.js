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

function delete_item(product_id){
    console.log(product_id);
    product_id = product_id.replace('-delete','')
    console.log(product_id);
    tr_to_delete = product_id + "-tr"

    // find tr with such tr_to_delete in
    // delete
    // send request to api
}
