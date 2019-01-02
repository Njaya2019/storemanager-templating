var tokenButton=document.getElementById('login');

tokenButton.addEventListener("submit", function(event){

    //var email=document.getElementById('email');
    //var passwd=document.getElementById('password');
    //var params=("email=email&password=passwd");
   //console.log('BUTTON CLICKED');
   var tokenRequest=new XMLHttpRequest();
   tokenRequest.open('POST', "/api/v1/admin/login");
   tokenRequest.onreadystatechange=function() {
    if (this.readyState == 4 && this.status == 200) {
        //var ourdata=tokenRequest.responseText;
        //var getpage=new XMLHttpRequest();
        //getpage.open('GET', "/api/v1/admin/signup",true);
        //getpage.setRequestHeader('Authorization', 'Bearer '+ourdata);
        //getpage.setRequestHeader('Content-Type', 'application/xml');
        //window.location = "http://127.0.0.1:5000/api/v1/admin/signup";
        res=tokenRequest.responseURL
        window.location.href = res;
        //getpage.onreadystatechange=function() {
           // if (this.readyState == 4 && this.status == 200) {
                
            //}};getpage.send();
        //console.log(ourdata);
        //alert(ourdata)
            //const myHeaders = new Headers();
            //myHeaders.append('X-AUTH-TOKEN', ourdata);
    
            //return fetch('/api/v1/admin/signup', {
            //method: 'GET',
            //headers: myHeaders
            //})
      }
      else{
        var err=tokenRequest.responseText;
        newErr=JSON.parse(err);
        document.getElementById('error').innerHTML=newErr.error
        //alert(newErr.error);
      }
   };
    const formData = new FormData( tokenButton );
    tokenRequest.send(formData);
    event.preventDefault();
});

