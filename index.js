function validateForm()                                    
{ 
    var title = document.forms["myForm"]["title"];               
    var experation = document.forms["myForm"]["experation"];    
    var contenue = document.forms["myForm"]["desc"];   
   
    if (title.value == "")                                  
    { 
        document.getElementById('errorTitle').innerHTML="Veuillez entrez un titre valide";  
        title.focus(); 
        return false; 
    }else{
        document.getElementById('errorTitle').innerHTML="";  
    }
       
    if (experation.value == "")                                   
    { 
        document.getElementById('errorExperation').innerHTML="Veuillez entrez un créneau valide"; 
        experation.focus(); 
        return false; 
    }else{
        document.getElementById('errorExperation').innerHTML="";  
    }
   
    if (contenue.value == "")                           
    {
        document.getElementById('errorDesc').innerHTML="Veuillez entrez un contenue valide"; 
        contenue.focus(); 
        return false; 
    }else{
        document.getElementById('errorDesc').innerHTML="";  
    }
   
    return true; 
}