function get_users(){
    var users=new XMLHttpRequest();
    users.open('GET', "/api/v1/admin/users");
    users.onload=function() {
    if (this.readyState == 4 && this.status == 200) {
        usersData=users.responseText
        //window.onload=renderHtml();
        //d=JSON.parse(usersData);
        
        emps=JSON.parse(usersData);
        //alert(u[0].fullname);
        document.getElementById('user-data').innerHTML=`
        ${emps.map(function(emp){
           return `
           <tr>
            <td>
                <a href="/api/v1/admin/users/${emp.user_id}" id="edit" class="edit">&#9998; Edit</a>
                <button type="buttton" id="del" onclick="del()" class="delete" value=${emp.user_id}>&#10005; Delete</button>
            </td>
            <td>${emp.fullname}</td>
            <td>${emp.email}</td>
            <td>Oct 9, 2018 9:42 A.M</td>
            <td>Oct 10, 2018 5:30 P.M</td>
            <td>${emp.role}</td>
            </tr>
           
           `
           
           //emp.fullname
        }).join('')}
        `
        //window.onload =document.getElementById('allusers').innerHTML=usersData
    }
};
users.send();
}
get_users();

// Ajax request to delete a user



function del(){
    var deleteBtnValue=document.getElementById('del').value;
    var delRequest=new XMLHttpRequest();
    delRequest.open('DELETE', "/api/v1/admin/users/"+deleteBtnValue);
    delRequest.onload=function() {
        if (delRequest.readyState == 4 && delRequest.status == 200) {
           // deleteResponse=users.responseText
            alert('User deleted');
            get_users();

        }
    }
    delRequest.send();
    
}
   





