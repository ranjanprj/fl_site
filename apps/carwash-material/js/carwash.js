var apiURL = "http://ec2-52-90-180-17.compute-1.amazonaws.com:3000"
var contentRoot = "/static/www";
token = "";
emailAddr = "";
app_name = "carwash_app";
service_name = "carwash_service";

/*
 * 	Ajax Helpers
 */
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
            callback(d,status="ERROR");

        }
    }).done(function(data) {
        callback(data,status="SUCCESS");
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
            callback(d,status="ERROR");


        }
    }).done(function(data) {
    	callback(data,status="SUCCESS");
    });
}




/*
 * After login create a booking
 *
 */

function getServiceAssetDetails() {

    var url = `/service?app_name=eq.` + app_name + `&service_name=eq.` + service_name; //+ `&select=id,service_asset{*}`;
    ajaxCallWithAuth("GET", url, '', function(serviceAssetData) {
        

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

//        console.log('Your current position is:');
//        console.log(`Latitude : ${crd.latitude}`);
//        console.log(`Longitude: ${crd.longitude}`);
//        console.log(`More or less ${crd.accuracy} meters.`);
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
      
        // Now create booking details
        getServiceDetails(100, "initiated", bookingDetailsData);
    }, "return=representation");
}


/*
 * View Service and assets
 *
 */

var serviceDetails;
var bookDetailsData;
function getServiceDetails(dist_in_km, status, bookingDetailsData) {
    // /service_booking_view?dist_in_km=lt.1000000&status=eq.initiated&app_name=eq.carwash_app&service_name=eq.carwash_service&booking_id=eq.7
    var url = `/service_booking_view?dist_in_km=lt.` + dist_in_km + `&status=eq.` + status + `&app_name=eq.` + app_name + `&service_name=eq.` + service_name + `&booking_id=eq.` + bookingDetailsData.booking_id;
    console.log(url);

    ajaxCallWithAuth("GET", url, '', function(data) {
        
        serviceDetails = data;
        console.log("GET BOOKING  DETAILS");
        bookDetailsData = bookingDetailsData;
        console.log(bookingDetailsData);
        console.log("GET SERVICE DETAILS");
        serviceDetails = data;
        console.log(serviceDetails);
        
        initMap(serviceDetails,bookDetailsData);
    });


}



/*
 * 	Framework 7 Functions
 * 
 */
var crd;
function getCurrentPositionIn(callback) {
    var position;
    var options = {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
    };

    function success(pos) {
        crd = pos.coords;

        console.log('Your current position is:');
        console.log(`Latitude : ${crd.latitude}`);
        console.log(`Longitude: ${crd.longitude}`);
        console.log(`More or less ${crd.accuracy} meters.`);
        callback(crd)
    };

    function error(err) {
        console.warn(err);
    };

    navigator.geolocation.getCurrentPosition(success, error, options);

}

var map;
function initMap(servDetails,bookDetails) {
	console.log("INIT MAP");
	
	
    	  var mapDiv = document.getElementById("map");
    	    console.log(mapDiv);
    	    var uluru = {lat: bookDetails.booked_lat, lng: bookDetails.booked_lon};

    	    if(mapDiv){
    	    	map = new google.maps.Map(mapDiv, {
    	            zoom: 16,
    	            center: uluru
    	          });
    	          var marker = new google.maps.Marker({
    	            position: uluru,
    	            map: map
    	          });	
    	          
    	          var image = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
    	          for(var s in servDetails){
    	        	  console.log("---------------");
    	        	  var pos = {lat: servDetails[s].current_lat, lng: servDetails[s].current_lon};
    	        	  console.log("---------------" + pos);
    	        	  var marker = new google.maps.Marker({
    	    	            position: pos,
    	    	            map: map,
    	    	            label: servDetails[s].company_name,

    	    	            icon: image
    	    	          });	
    	          }
    	    }
    
    
  }



// Init App

var myApp = new Framework7({
    modalTitle: 'Framework7',
    // Enable Material theme
    material: true,
});

// Expose Internal DOM library
var $$ = Dom7;

// Add main view
var mainView = myApp.addView('.view-main', {
});
// Add another view, which is in right panel
var rightView = myApp.addView('.view-right', {
});


$$(document).on('page:init', function (e) {
	  // Do something here when page loaded and initialized
	console.log("Loading page");
	console.log(e);
	var page = e.detail.page;
	console.log(page);
	if(page.name === "second-screen"){
		if(document.getElementById("map")){
			getServiceAssetDetails(initMap);

		}
		
	}else if(page.name === "third-screen"){
		var bookingForm = $("form#booking-form");	  	

		var email =  bookingForm.find('input[name="email"]').val(emailAddr);
		var credit_card_email =  bookingForm.find('input[name="customer_payment_email"]').val(emailAddr);
		var amount =  bookingForm.find('input[name="amount"]').val(4000);
		
		
		
	
		
		$("a#confirm").on("click",function(e){

			
//			
//			var credit_card =  bookingForm.find('input[name="credit_card"]').val();
//			var cvv =  bookingForm.find('input[name="cvv"]');
//			var year =  bookingForm.find('input[name="year"]');
//			var month =  bookingForm.find('input[name="month"]');
//			
//			var booking_time =  bookingForm.find('input[name="booking_time"]').val();
			
			var formData = myApp.formToData("form#booking-form");
			console.log("BOOKING DETAILS");
			console.log(bookDetailsData);
			 var paymentData = {
					 "token"  : token,
					 "customer_payment_email" : formData.customer_payment_email,
					 "customer_app_email"  : emailAddr ,
					 "service_name" : service_name,
					 "payment_provider"  : "stripe",
					 "booking_id"  : bookDetailsData.booking_id,
					 "amount"  : formData.amount,
					 "currency" : "USD"
			 };
			 console.log("Charge Data");
			 console.log("STATUS " + paymentData);
			 ajaxCallWithAuth("POST", "/rpc/payment_stripe",paymentData , function(data,status) {
				 console.log("STATUS");
				 console.log(status);
			     if(status !== "ERROR"){
			    	 console.log("PAY MENT DONE")
			    	 console.log(data);
		
			    	        var url = "/booking_details?booking_id=eq." + bookDetailsData.booking_id; 
			    	        ajaxCallWithAuth("GET", url ,"" , function(booking_details) {			    	        	
			    	        	
								 booking_details[0].booking_time = formData.booking_time;
			    	        	 booking_details[0].status = "inprogress";
			    	        	 delete booking_details[0].updated_at;
			    	        	 console.log("BOOKING DETAILS");
			    	        	 console.log(booking_details);
			    	        	 ajaxCallWithAuth("POST", url , booking_details[0], function() {
			    	        		 		console.log("BOOKING IN PROGRESS");
			    	        		 		mainView.router.loadPage('fourth-screen.html');

					    	        });
			    	        });
				    	          
				
			     }   
				 
			 });
			
			// initialize the booking
			console.log(formData);

		});
	}else if(page.name === "fourth-screen"){
		 var url =`/booking_details?booking_id=eq.${bookDetailsData.booking_id}&order=updated_at.desc&limit=1`; 
			 
		   ajaxCallWithAuth("GET", url ,"" , function(booking_details) {		
			   
	        	$("div#order-number").html("Order No : " + bookDetailsData.booking_id);
	        	var orderDetails = `Order No : ${bookDetailsData.booking_id} , Booked At ${bookDetailsData.booking_time}`;
	        	$("div#order-details").html(orderDetails);
	        	var footerDetails = `Order Status : ${booking_details[0].status}`;
	        	$("div#order-footer").html(footerDetails);
				
	        });
	}else if(page.name === "stripe-payment"){
		document.getElementById('stripe-payment-button').addEventListener('click', function(e) {
			  // Open Checkout with further options:
			  handler.open({
			    name: 'Stripe.com',
			    description: '2 widgets',
			    zipCode: true,
			    amount: 2000
			  });
			  e.preventDefault();
		});
		
	}
});
	

$$('a#sign-in-btn').on('click', function(e){
	
	  var formData = myApp.formToData('form#sign-in-form');
	  ajaxCallWithAuth("POST","/rpc/login",formData,function(loginData,status){	  
		  
		  if(status && status === "ERROR"){
			  if(loginData.message = "invalid user or password"){
				  
				  
			  }
		  }else{
			  console.log("LOGGED IN ");
			  console.log(loginData);
			  token = loginData.token;
			  emailAddr = formData.email;
			  mainView.router.loadPage('second-screen.html');
		  }
		  
	  });
	  
}); 

$$('a#book-now').on('click', function(e){
	   
	  
	  
	  
}); 
$$('a#schedule-later').on('click', function(e){
	
	  var formData = myApp.formToData('form#sign-in-form');
	  ajaxCallWithAuth("POST","/rpc/login",formData,function(loginData,status){
		  
		
		  mainView.router.loadPage('third-screen.html');
		
		  
	  });
	  
});

$$('a#confirm').on('click', function(e){
	   alert("--------");
	  
	  
	  
}); 