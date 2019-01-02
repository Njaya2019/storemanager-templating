//Get modal element
var modal=document.getElementById('simplemodal');
//Get edit button
var modalbutton=document.querySelectorAll('.edit');
//Get close button
var closeBtn=document.getElementsByClassName('closebtn')[0];



//listen to close click modal

//listen to outside click and close


//function to open modal
[].forEach.call(modalbutton, function(el) {
    el.onclick = function() {
        modal.style.display = "block";
    }
  })



//function to close modal
closeBtn.onclick = function() {
    modal.style.display = "none";
}


window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    } 
}

//function to close if modal is clicked


 
