
        var added=[];
        if(added.length==0){
            $('.list').append( '<h3> ENTERED SYMPTOMS APPEARS HERE </h3>');
            
        }
       function add(){
        var firstname = $('#city_autocomplete').val();
        if(firstname && !(IN(firstname))){
            rm=' <input type="Button"  value="remove" id="'+(add.Counter+"B")+'" onClick="remove('+add.Counter+');"> ';
            $('#top').append( '<li id="'+(add.Counter)+'"  >' + firstname + rm + '</li>');
            added.push(firstname);
            add.Counter++;
        }
        console.log(added);
       }
       add.Counter=0;

       function IN(ele){
           for(var i=0;i<added.length;i++){
               if(added[i]==ele){
                   return true;
               }
           }
           return false;
       }

       function remove(element_id){
            //    alert("func called");
            txt=document.getElementById(element_id).innerHTML;
            added = added.filter(function(item) {
                return item !== txt
            });
            // console.log(element_id);
            // console.log(txt);
            

            var element = document.getElementById(element_id);
            element.parentNode.removeChild(element);
            
            btn_id=element_id +'B';
            var element = document.getElementById(btn_id);
            console.log(btn_id+" "+element);
            element.parentNode.removeChild(element);

            console.log(added);
       }

       //sending the added[] to flask
       function send_data(){
        var input = document.createElement("input");

        input.setAttribute("type", "hidden");

        input.setAttribute("name", "length");

        input.setAttribute("value", added.length);

        //append to form element that you want .
        document.getElementById("invisible_form").appendChild(input);

        for(var i=0;i<=added.length;i++){
            var input = document.createElement("input");

                input.setAttribute("type", "hidden");

                input.setAttribute("name", "symptom"+i);

                

                input.setAttribute("value", added[i]);

                //append to form element that you want .
                document.getElementById("invisible_form").appendChild(input);
        }
                input.setAttribute("type", "submit");

                input.setAttribute("name", "submit");

                input.setAttribute("value", "confirm");

                //append to form element that you want .
                document.getElementById("invisible_form").appendChild(input);
                
       }
       
      
        
    