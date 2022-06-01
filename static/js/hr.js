var elem="";
function show(id){
    elem = document.getElementById("show");
    elem.setAttribute("class", "d-block");
    id.setAttribute("class", "d-none");
}
function hide(){
    elem = document.getElementById("show");
    elem.setAttribute("class", "d-none");
    document.getElementById("shm").setAttribute("class", "d-inline");
}