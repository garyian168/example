var xmlhttp;
function showName(name)
{
    if (name.length==0)
    { 
        document.getElementById("nameResult").innerHTML="";
        return;
    }
    
    if (window.XMLHttpRequest)
    {
        xmlhttp=new XMLHttpRequest();
    }
    else
    {
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    
    xmlhttp.open("GET","getName.php?n="+name,true);
    xmlhttp.send();
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            document.getElementById("nameResult").innerHTML=xmlhttp.responseText;
        }
    }
    
}

