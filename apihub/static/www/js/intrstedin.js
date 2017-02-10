var apiURL = "http://ec2-52-90-180-17.compute-1.amazonaws.com:3000"
var contentRoot = "/static/www";
token = "";
emailAddr = "";
app_name = "carwash_app";
service_name = "carwash_service";


$(document).ready(function(e) {
    init();
  
 


});

function init() {
    get_stripe_pubkey();
}

function ajaxCall(method, url, data, callback) {
    var dat;
    if (!data) {
        dat = "";
    } else {
        dat = JSON.stringify(data);
    }
    $.ajax({
        method: method,
        url: apiURL + url,
        data: dat,
        contentType: "application/json",
        dataType: "json",
        success: function(data) {

        },
        error: function(d) {
            //displayError(url, data);
            console.log("There was ERROR in ajaxCall");
            console.log(d);

        }
    }).done(function(data) {
        callback(data);
    });
}

function ajaxCallWithAuth(method, url, data, callback, prefer) {
    var dat;
    if (!data) {
        dat = "";
    } else {
        dat = JSON.stringify(data);
    }
    var bearer = " Bearer " + token;
    $.ajax({
        method: method,
        url: apiURL + url,
        data: dat,
        contentType: "application/json",
        dataType: "json",
        headers: {
            "Content-Type": "application/json",
            "Authorization": bearer,
            "Prefer": prefer
        },
        success: function(data) {

        },
        error: function(d) {
            // displayError(url, data);
            console.log("There was ERROR in ajaxCallWithAuth");
            console.log(d);


        }
    }).done(function(data) {
        callback(data);
    });
}

/*
 * Signup function
 */

$("form#signup_form").submit(function(e) {
    var name = $(this).find('input[name="name"]').val();
    var email = $(this).find('input[name="email"]').val();
    var pass = $(this).find('input[name="pass"]').val();
    var repeat_pass = $(this).find('input[name="repeat_pass"]').val();
    var appname = $(this).find('input[name="app_name"]').val();

    if (pass != repeat_pass) {
        alert("password does not match");
    }

    var data = {
        "email": email,
        "pass": pass

    };
    console.log(data);
    ajaxCall("POST", "/rpc/signup", data, function(data) {
        console.log("SIGNUP DONE");
        console.log(data);


    });

    e.preventDefault();

});



/*
 *  function
 */

$("form#signup_form").submit(function(e) {
    var name = $(this).find('input[name="name"]').val();
    var email = $(this).find('input[name="email"]').val();
    var pass = $(this).find('input[name="pass"]').val();
    var repeat_pass = $(this).find('input[name="repeat_pass"]').val();
    var appname = $(this).find('input[name="app_name"]').val();

    if (pass != repeat_pass) {
        alert("password does not match");
    }

    var data = {
        "email": email,
        "pass": pass

    };
    console.log(data);
    ajaxCall("POST", "/rpc/signup", data, function(data) {
        console.log("SIGNUP DONE");
        console.log(data);


    });

    e.preventDefault();

});


/*
 *  Login function
 */

$("form#login_form").submit(function(e) {

    var email = $(this).find('input[name="email"]').val();
    var pass = $(this).find('input[name="pass"]').val();


    var data = {
        "email": email,
        "pass": pass

    };
    emailAddr = data.email;
    console.log(data);
    ajaxCall("POST", "/rpc/login", data, function(data) {
        console.log("LOGIN DONE");
        console.log(data);
        token = data.token;


    });

    e.preventDefault();

});


/*
 *  Reset function
 */

$("form#reset_form").submit(function(e) {

    var email = $(this).find('input[name="email"]').val();

    var data = {
        "email": email

    };
    console.log(data);
    ajaxCall("POST", "/rpc/request_password_reset", data, function(data) {
        console.log("RESET DONE");
        console.log(data);
        console.log("check your email");

    });


    e.preventDefault();
});



/*
 *  Reset FORM Password function
 */

$("form#reset_pass_form").submit(function(e) {


    var pass = $(this).find('input[name="pass"]').val();
    var email = $(this).find('input[name="email"]').val();
    var token = $(this).find('input[name="token"]').val();

    var data = {
        "email": email,
        "token": token,
        "pass": pass


    };
    console.log(data);
    ajaxCall("POST", "/rpc/reset_password", data, function(data) {
        console.log("RESET  DONE");
        console.log(data);
        window.location.assign("http://ec2-52-90-180-17.compute-1.amazonaws.com:8080/static/www/index.html");

    });

    e.preventDefault();

});





/*
 * After login create a booking
 *
 */

function getServiceAssetDetails() {

    var url = `/service?app_name=eq.` + app_name + `&service_name=eq.` + service_name; //+ `&select=id,service_asset{*}`;
    ajaxCallWithAuth("GET", url, '', function(serviceAssetData) {
        console.log("getServiceAssetDetails");

        // Now create booking details
        createBooking(serviceAssetData);
    });

}

/*
 * After login create a booking
 *
 */

function createBooking(serviceAssetData) {
    // first create a booking
    var url = "/booking";
    var data = {
        booked_by: emailAddr
    };
    ajaxCallWithAuth("POST", url, data, function(bookingData) {
        console.log("GET _SERVICE");
        console.log(data);

        // Now create booking details
        getCurrentPosition(bookingData, serviceAssetData);
    }, "return=representation");


}

function getCurrentPosition(bookingData, serviceAssetData) {
    var position;
    var options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
    };

    function success(pos) {
        var crd = pos.coords;

        console.log('Your current position is:');
        console.log(`Latitude : ${crd.latitude}`);
        console.log(`Longitude: ${crd.longitude}`);
        console.log(`More or less ${crd.accuracy} meters.`);
        createBookingDetails(bookingData, serviceAssetData, crd)
    };

    function error(err) {
        console.warn(`ERROR(${err.code}): ${err.message}`);
    };

    navigator.geolocation.getCurrentPosition(success, error, options);

}


function createBookingDetails(bookingData, serviceAssetData, position) {


    var data = {
        "status": "initiated",
        "booking_id": bookingData.id,
        "booked_by": emailAddr,
        "service_id": serviceAssetData[0].id,
        "booked_lat": position.latitude,
        "booked_lon": position.longitude

    };

    var url = `/booking_details`;
    ajaxCallWithAuth("POST", url, data, function(bookingDetailsData) {
        console.log("getServiceAssetDetails");
        console.log("bookingDetailsData");
        // Now create booking details
        getServiceDetails(100, "initiated", bookingDetailsData);
    }, "return=representation");
}


/*
 * View Service and assets
 *
 */

function getServiceDetails(dist_in_km, status, bookingDetailsData) {
    // /service_booking_view?dist_in_km=lt.1000000&status=eq.initiated&app_name=eq.carwash_app&service_name=eq.carwash_service&booking_id=eq.7
    var url = `/service_booking_view?dist_in_km=lt.` + dist_in_km + `&status=eq.` + status + `&app_name=eq.` + app_name + `&service_name=eq.` + service_name + `&booking_id=eq.` + bookingDetailsData.booking_id;
    console.log(url);

    ajaxCallWithAuth("GET", url, '', function(data) {
        console.log("GET _SERVICE");
        console.log(data);
    });


}


/*******************************************
 *              PAYMENT
 *
 ********************************************/

function get_stripe_pubkey() {
    prep_stripe_payment_form('pk_test_JbTi6Lps8rteWNYYzMWd6A4l');
}

function stripeResponseHandler(status, response) {
    // Grab the form:
    var $form = $('#payment-form');

    if (response.error) { // Problem!

        // Show the errors on the form:
        $form.find('.payment-errors').text(response.error.message);
        $form.find('.submit').prop('disabled', false); // Re-enable submission

    } else { // Token was created!

        // Get the token ID:
        var token = response.id;

        // Insert the token ID into the form so it gets submitted to the server:
        $form.append($('<input type="hidden" name="stripeToken">').val(token));

        // Submit the form:
        $form.get(0).submit();
    }
};

function prep_stripe_payment_form(pubkey) {
    Stripe.setPublishableKey(pubkey);
    var $form = $('#payment-form');
    $form.submit(function(event) {
        // Disable the submit button to prevent repeated clicks:
        $form.find('.submit').prop('disabled', true);

        // Request a token from Stripe:
        Stripe.card.createToken($form, stripeResponseHandler);

        // Prevent the form from being submitted:
        return false;
    });
}

function show_stripe_payment_report() {

}
