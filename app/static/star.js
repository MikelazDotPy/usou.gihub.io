var count, r1, r2, r3;
document.getElementById("rating").classList.add('active');
function starmark(item)
{
if (item.id[1] + item.id[2] + item.id[3] == "one")
{
r1 = item.id[0]
}
if (item.id[1] + item.id[2] + item.id[3] == "two")
{
r2 = item.id[0]
}
if (item.id[1] + item.id[2] + item.id[3] == "thr")
{
r3 = item.id[0]
}
count=item.id[0];
sessionStorage.starRating = count;
var subid= item.id.substring(1);
for(var i=0;i<5;i++)
{
if(i<count)
{
document.getElementById((i+1)+subid).style.color="orange";
}
else
{
document.getElementById((i+1)+subid).style.color="black";
}


}

}

function result()
{
//Rating : Count
//Review : Comment(id)
if(r1 == undefined)
{
r1 = 1;
}
if(r2 == undefined)
{
r2 = 1;
}
if(r3 == undefined)
{
r3 = 1;
}
alert("Спасибо за отзыв")
 let xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://127.0.0.1:5000/star');
    var a = {
        "r1":r1,
        "r2":r2,
        "r3":r3,
        "com":document.getElementById("comment").value
    }
    var c = JSON.stringify(a)
    xhr.send(c)
}

