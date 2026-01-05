/*basic function in js :
     functions are the main building block of a program they allow to call a single code many times 
     without repeatation 

     declaration :

     function-keyword  function-name (parameters){
     // body
     }
     to call a function simply write function name 
    
*/
function showmessage(){
  console.log("hello all");  
}
showmessage()

/*a function can call both local variables (means the variable that is inside the function and only visible 
inside a function) or an outer variable function has full acess to outside variable 
it can modify it as well  

parameters:
we can pass arbitriary data to function using parameters

if only a single argument is given then it just shows undefined instead of error 
*/
function showMessage(from, text) { // parameters: from, text
  console.log(from + ': ' + text);
}

showMessage('Ann', 'Hello!'); // Ann: Hello! (*)
showMessage('Ann', "What's up?"); // Ann: What's up? (**)

/*
creating a function in some other way :

const function-name = () => {
    return value 
    }
export const instead of export default function name 

this is done to some scenarios to reduce line of code as we can directly call the function 
for anonymous function 
example:
 */
<button onClick={() => console.log("hello duniya")}> click here    
</button>






 
