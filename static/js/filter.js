var all_movies = all_movies;
id_index = {"id": [], "index": [], "title": []};


// console.log(all_movies);

all_movies.forEach(function(row, index) {
    title = row[0];
    movie_id = row[1].toString();
    var option = document.createElement('option');
    option.setAttribute("data-tokens", movie_id);
    option.setAttribute("value", movie_id);
    movie = document.createTextNode(title);
    option.appendChild(movie);
    document.getElementById("filter").appendChild(option);
    id_index["id"].push(movie_id);
    id_index["index"].push(index);
    id_index["title"].push(title);
});


    
    $('#filter').on('changed.bs.select', (function (e, clickedIndex, isSelected, previousValue) {
        // do something...
        

        id = id_index["id"][clickedIndex];
        title = id_index["title"][clickedIndex];
        var image1 = document.getElementById(`image1`).getAttribute("src");
        var image2 = document.getElementById(`image2`).getAttribute("src");
        var image3 = document.getElementById(`image3`).getAttribute("src");
        var poster_present = false;
        var poster = "https://movie-posters-project3.s3.us-east-2.amazonaws.com/images/";
        poster = poster + id + ".jpg";
        console.log(clickedIndex, id, title, previousValue);
        console.log(poster);

        var space1;
        var space2;
        var space3;
        var spaces = [space1, space2, space3];

        // Checks for poster present then removes
        for (i = 0; i < previousValue.length; i++) { 
            if (previousValue[i] == id) {
                poster_present = true;
            }
        }
        
        // Checks if poster absent then adds
        if (image1.includes("random")) {
            space1 = true;
        }

        if (image2.includes("random")) {
            space2 = true;
        }

         if (image3.includes("random")) {
            space3 = true;
        }

        if (!poster_present) {
            console.log("poster not present");

            if(space1) {
            document.getElementById("image1").setAttribute("src", poster);
            document.getElementById("movie_name1").innerHTML = title;
            }
 
             else if (space2) {
                 document.getElementById("image2").setAttribute("src", poster);
                 document.getElementById("movie_name2").innerHTML = title;
             }
 
             else if (space3) {
                 document.getElementById("image3").setAttribute("src", poster);
                 document.getElementById("movie_name3").innerHTML = title;
             }
         };


        
       if (poster_present) {
           console.log("poster is present");
            if (image1.includes(`/${id}.jpg`)) {
                document.getElementById("image1").setAttribute("src", "static/images/random1.gif");
                document.getElementById("movie_name1").innerHTML = "Selection 1";
            }

            else if (image2.includes(`/${id}.jpg`)) {
                document.getElementById("image2").setAttribute("src", "static/images/random2.gif");
                document.getElementById("movie_name2").innerHTML = "Selection 2";
            }

            else if (image3.includes(`/${id}.jpg`)) {
                document.getElementById("image3").setAttribute("src", "static/images/random3.gif");
                document.getElementById("movie_name3").innerHTML = "Selection 3";
            }
        };

}));

$('#submit').click(function() {
    movies = document.getElementById("filter").selectedOptions;
    console.log(movies);
    list = [];

    for (var i = 0; i < movies.length; i++) {
        index = i + 1;
        movie = movies[i].text
        list.push(movie)
        console.log(movie);
    }
    $.ajax({
      type: "POST",
      contentType: "application/json;charset=utf-8",
      url: "/choices",
      traditional: "true",
      data: JSON.stringify(list),
      dataType: "json",
      success: function (res) { console.log(res) 
    
      document.getElementById("page").innerHTML = res.data;
      var mix = mix;
      console.log(mix);
    
    
    }, 
      // res is the response from the server 
      // (from return request.data)
    error: function (error) { console.log(error) }
    });

    
});