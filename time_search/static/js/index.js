var getPushButtonValue = function(id_str, btn_str) {
  document.getElementById(id_str).innerHTML = btn_str;
}

function check() {
  console.log('check');

  if (document.getElementById('dep_stop').innerHTML == "出発地のバス停名" && document.getElementById('arr_stop').innerHTML == "到着地のバス停名") {
    alert("出発地と到着地が未選択です。");
    return false;
  }
  else if (document.getElementById('dep_stop').innerHTML == "出発地のバス停名") {
    alert("出発地が未選択です。");
    return false;
  }
  else if (document.getElementById('arr_stop').innerHTML == "到着地のバス停名") {
    alert("到着地が未選択です。");
    return false;
  }
  else if (document.getElementById('dep_stop').innerHTML == document.getElementById('arr_stop').innerHTML) {
    alert("出発地と到着地が同じです。")
    return false;
  }
  else {
    return true;
  }
}

window.onload = function() {
  console.log('window.onload');

  var depStopBtns = document.getElementsByClassName("dep_stop_btn");
  var arrStopBtns = document.getElementsByClassName("arr_stop_btn");

  for(var i=0; i<depStopBtns.length; i++) {
    depStopBtns[i].onclick = function() {
      document.getElementById("dep_stop").innerHTML = this.innerHTML;
      document.getElementsByClassName("selected-dep-stop")[0].value = this.innerHTML
      for(var j=0; j<depStopBtns.length; j++) {
        depStopBtns[j].style.backgroundColor = "#ECECEC";
        depStopBtns[j].style.color = "#A5A5A5";
      }
      this.style.backgroundColor = "#EC544E";
      this.style.color = "#FFFFFF";
    }
  }

  for(var i=0; i<arrStopBtns.length; i++) {
    arrStopBtns[i].onclick = function() {
      document.getElementById("arr_stop").innerHTML = this.innerHTML;
      document.getElementsByClassName("selected-arr-stop")[0].value = this.innerHTML
      for(var j=0; j<arrStopBtns.length; j++) {
        arrStopBtns[j].style.backgroundColor = "#ECECEC";
        arrStopBtns[j].style.color = "#A5A5A5";
      }
      this.style.backgroundColor = "#EC544E";
      this.style.color = "#FFFFFF";
    }
  }

};
