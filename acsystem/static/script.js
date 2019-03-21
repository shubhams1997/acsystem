// let arrofobj = [{ "id": 1, "name": "name1" }, { "id": 2, "name": "name2" }, { "id": 3, "name": "name3" }, { "id": 4, "name": "name4" }];
// /*initiate the autocomplete function on the "myInput" element, and pass along the countries array as possible autocomplete values:*/

// function autocomplete2(inp, arr) {
//   var currentFocus;
//   inp.addEventListener("input", function (e) {
//     var a, b, i, val = this.value;
//     /*close any already open lists of autocompleted values*/
//     closeAllLists();
//     if (!val) { return false; }
//     currentFocus = -1;
//     /*create a DIV element that will contain the items (values):*/
//     a = document.createElement("DIV");
//     a.setAttribute("id", this.id + "autocomplete-list");
//     a.setAttribute("class", "autocomplete-items");
//     /*append the DIV element as a child of the autocomplete container:*/
//     this.parentNode.appendChild(a);
//     /*for each item in the array...*/
//     for (i = 0; i < arr.length; i++) {
//       /*check if the item starts with the same letters as the text field value:*/
//       if (arr[i]["name"].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
//         /*create a DIV element for each matching element:*/
//         b = document.createElement("DIV");
//         /*make the matching letters bold:*/
//         b.innerHTML = "<strong>" + arr[i]["name"].substr(0, val.length) + "</strong>";
//         b.innerHTML += arr[i]["name"].substr(val.length);
//         /*insert a input field that will hold the current arr item's value:*/
//         b.innerHTML += "<input type='hidden' name='" + arr[i]["id"] + "' value='" + arr[i]["name"] + "'>";
//         /*execute a function when someone clicks on the item value (DIV element):*/
//         b.addEventListener("click", function (e) {
//           /*insert the value for the autocomplete text field:*/
//           inp.value = this.getElementsByTagName("input")[0].value;
//           console.log(this.getElementsByTagName("input")[0].name);
//           /*close the list of autocompleted values,
//           (or any other open lists of autocompleted values:*/
//           closeAllLists();
//         });
//         a.appendChild(b);
//       }
//     }
//   });
//   /*execute a function presses a key on the keyboard:*/
//   inp.addEventListener("keydown", function (e) {
//     var x = document.getElementById(this.id + "autocomplete-list");
//     if (x) x = x.getElementsByTagName("div");
//     if (e.keyCode == 40) {
//       /*If the arrow DOWN key is pressed,
//       increase the currentFocus variable:*/
//       currentFocus++;
//       /*and and make the current item more visible:*/
//       addActive(x);
//     } else if (e.keyCode == 38) { //up
//       /*If the arrow UP key is pressed,
//       decrease the currentFocus variable:*/
//       currentFocus--;
//       /*and and make the current item more visible:*/
//       addActive(x);
//     } else if (e.keyCode == 13) {
//       /*If the ENTER key is pressed, prevent the form from being submitted,*/
//       e.preventDefault();
//       if (currentFocus > -1) {
//         /*and simulate a click on the "active" item:*/
//         if (x) x[currentFocus].click();
//       }
//     }
//   });
//   function addActive(x) {
//     /*a function to classify an item as "active":*/
//     if (!x) return false;
//     /*start by removing the "active" class on all items:*/
//     removeActive(x);
//     if (currentFocus >= x.length) currentFocus = 0;
//     if (currentFocus < 0) currentFocus = (x.length - 1);
//     /*add class "autocomplete-active":*/
//     x[currentFocus].classList.add("autocomplete-active");
//   }
//   function removeActive(x) {
//     /*a function to remove the "active" class from all autocomplete items:*/
//     for (var i = 0; i < x.length; i++) {
//       x[i].classList.remove("autocomplete-active");
//     }
//   }
//   function closeAllLists(elmnt) {
//     /*close all autocomplete lists in the document,
//     except the one passed as an argument:*/
//     var x = document.getElementsByClassName("autocomplete-items");
//     for (var i = 0; i < x.length; i++) {
//       if (elmnt != x[i] && elmnt != inp) {
//         x[i].parentNode.removeChild(x[i]);
//       }
//     }
//   }
//   /*execute a function when someone clicks in the document:*/
//   document.addEventListener("click", function (e) {
//     closeAllLists(e.target);
//   });
// }

// autocomplete2(document.getElementById("myInput2"), arrofobj);

// var count = 1;
// $("#additeminlist").on("click", () => {
//   let arrofobj = [{ "id": 1, "name": "name1" }, { "id": 2, "name": "name2" }, { "id": 3, "name": "name3" }, { "id": 4, "name": "name4" }];
//   const data = `<tr class="row">
//   <td class="col-1"> <a class='btn btn-outline-dark'>delete</a></td>
//   <th class="col-6">
//   <div class="autocomplete" style="width:100%;">
//   <input autocomplete="off" id="`+count+`" class="form-control" type="text"
//   placeholder="Add an Item">
//   </div>
//   </th>
//   <td class="col-2"><input class="form-control" type="text"></td>
//   <td class="col-1"><input class="form-control" type="text"></td>
//   <td class="col-1">@9999</td>
//   </tr>`;
//   $("#itemslist").append(data);
//   autocomplete2(document.getElementById(count), arrofobj);
//   count++;
//   $("#itemslist tr td .btn").click(function (event) {
//     console.log("delete clicked");
//     event.preventDefault();
//     $(this).parents(".row").remove();
//   });
// });
