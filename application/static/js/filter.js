var all_movies = all_movies;
var reverse = false;
id_index = { id: [], index: [], title: [] };

screen.orientation.lock("landscape");

$("#reverse").click(function () {
  if (reverse == false) {
    $("body").css({
      "background-image": 'url("/static/images/bg12.gif")',
    });

    $("a").css({
      color: "black",
    });

    reverse = true;
  } else {
    $("body").css({
      "background-image": 'url("/static/images/bg8.gif")',
    });

    $("a").css({
      color: "white",
    });

    reverse = false;
  }
});

all_movies.forEach(function (row, index) {
  var option = document.createElement("option");
  title = row[0];
  movie_id = row[1].toString();

  option.setAttribute("data-tokens", movie_id);
  option.setAttribute("value", movie_id);
  movie = document.createTextNode(title);
  option.appendChild(movie);
  document.getElementById("filter").appendChild(option);

  id_index["id"].push(movie_id);
  id_index["index"].push(index);
  id_index["title"].push(title);
});

function random() {
  document.getElementsByTagName("option")[5].click();
}

$("#filter").on(
  "changed.bs.select",
  function (e, clickedIndex, isSelected, previousValue) {
    $('input[type="text"], textarea').val(""); // clears textbox area after selection

    id = id_index["id"][clickedIndex];
    title = id_index["title"][clickedIndex];
    var image1 = document.getElementById(`image1`).getAttribute("src");
    var image2 = document.getElementById(`image2`).getAttribute("src");
    var image3 = document.getElementById(`image3`).getAttribute("src");
    var movie_name1 = document.getElementById("movie_name1").innerHTML;
    var movie_name2 = document.getElementById("movie_name2").innerHTML;
    var movie_name3 = document.getElementById("movie_name3").innerHTML;
    var poster_present = false;
    var poster =
      "https://movie-posters-project3.s3.us-east-2.amazonaws.com/images/";
    poster = poster + id + ".jpg";

    // variables to determine empty spaces for posters
    var space1;
    var space2;
    var space3;
    var spaces = [space1, space2, space3];

    // Checks to see if the most recent selection has already been selected and therefore poster should be present
    for (i = 0; i < previousValue.length; i++) {
      if (previousValue[i] == id) {
        poster_present = true;
      }
    }

    // Checks if poster absent then sets space value to true
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
      if (space1) {
        const movieLink1 = document.getElementById("link1");

        document.getElementById("image1").setAttribute("src", poster);
        document.getElementById("movie_name1").innerHTML = title;

        movieLink1?.setAttribute("href", `/info/${id}`);
        movieLink1?.setAttribute("target", "_blank");
      } else if (space2) {
        const movieLink2 = document.getElementById("link2");

        document.getElementById("image2").setAttribute("src", poster);
        document.getElementById("movie_name2").innerHTML = title;

        movieLink2?.setAttribute("href", `/info/${id}`);
        movieLink2?.setAttribute("target", "_blank");
      } else if (space3) {
        const movieLink3 = document.getElementById("link3");

        document.getElementById("image3").setAttribute("src", poster);
        document.getElementById("movie_name3").innerHTML = title;

        movieLink3?.setAttribute("href", `/info/${id}`);
        movieLink3?.setAttribute("target", "_blank");
      }
    }

    if (poster_present) {
      if (image1.includes(`/${id}.jpg`) || movie_name1 == title) {
        const movieLink1 = document.getElementById("link1");

        document
          .getElementById("image1")
          .setAttribute("src", "static/images/random1.gif");

        movieLink1?.removeAttribute("href");
        movieLink1?.removeAttribute("target");
        document.getElementById("movie_name1").innerHTML = "Selection 1";
      } else if (image2.includes(`/${id}.jpg`) || movie_name2 == title) {
        const movieLink2 = document.getElementById("link2");

        document
          .getElementById("image2")
          .setAttribute("src", "static/images/random2.gif");
        document.getElementById("movie_name2").innerHTML = "Selection 2";

        movieLink2?.removeAttribute("href");
        movieLink2?.removeAttribute("target");
      } else if (image3.includes(`/${id}.jpg`) || movie_name3 == title) {
        const movieLink3 = document.getElementById("link3");

        document
          .getElementById("image3")
          .setAttribute("src", "static/images/random3.gif");
        document.getElementById("movie_name3").innerHTML = "Selection 3";

        movieLink3?.removeAttribute("href");
        movieLink3?.removeAttribute("target");
      }
    }

    var hey = "'#loading'";
    movies = document.getElementById("filter").selectedOptions;

    if (movies.length == 3) {
      document.getElementById(
        "button"
      ).innerHTML = `<button type="submit" class="btn btn-success" id="submit" onclick="$(${hey}).show();" >Submit</button>`;
      $("#submit").click(function () {
        var route;
        list = [];
        movies = document.getElementById("filter").selectedOptions;

        if (reverse == true) {
          route = "/worst";
        } else {
          route = "/choices";
        }
        for (var i = 0; i < movies.length; i++) {
          index = i + 1;
          movie = { movie_title: movies[i].text, movie_id: movies[i].value };
          list.push(movie);
          console.log(movie);
        }
        $.ajax({
          type: "POST",
          contentType: "application/json;charset=utf-8",
          url: route,
          traditional: "true",
          data: JSON.stringify(list),
          dataType: "json",
          success: function (res) {
            console.log(res);

            document.getElementById("page").innerHTML = res.data;
            var mix = mix;
            console.log(mix);
          },
          // res is the response from the server
          error: function (error) {
            console.log(error);
          },
        });
      });
    } else {
      document.getElementById("button").innerHTML = "";
    }
  }
);
