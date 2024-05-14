let reverse = false;
let id_index = { id: [], index: [], title: [] };

const setMovieLinkAttributes = (linkElement, id, title) => {
  linkElement?.setAttribute("href", `/info/${id}`);
  linkElement?.setAttribute("target", "_blank");
  linkElement?.setAttribute("title", title);
  linkElement?.setAttribute("data-selected", "true");
};

const removeMovieLinkAttributes = (linkElement) => {
  linkElement?.removeAttribute("href");
  linkElement?.removeAttribute("target");
  linkElement?.setAttribute(
    "title",
    "Select one of your favorite movies via dropdown menu below."
  );
  linkElement?.setAttribute("data-selected", "false");
};

$("#reverse").click(() => {
  if (reverse == false) {
    $("#fixed-background").css({
      "background-image": 'url("/static/images/bg12.gif")',
    });

    $("a").css({
      color: "black",
    });

    $("#reverse-label").css({
      color: "black",
    });

    $("#reverse-label").html(
      'Basis for <strong style="color: red;">negative</strong> recommendations &#128530;'
    );

    reverse = true;
  } else {
    $("#fixed-background").css({
      "background-image": 'url("/static/images/bg8.gif")',
    });

    $("a").css({
      color: "white",
    });

    $("#reverse-label").css({
      color: "white",
    });

    $("#reverse-label").html(
      'Basis for <strong style="color: green;">positive</strong> recommendations &#128525;'
    );

    reverse = false;
  }
});

Object.entries(all_movies)
  .sort(([_a, movie_id_a], [_b, movie_id_b]) => movie_id_a - movie_id_b)
  .forEach((row, index) => {
    let option = document.createElement("option");
    let title = row[0];
    let movie_id = row[1].toString();

    movie = document.createTextNode(title);

    option.setAttribute("data-tokens", movie_id);
    option.setAttribute("value", movie_id);
    option.appendChild(movie);

    document.getElementById("filter").appendChild(option);

    id_index["id"].push(movie_id);
    id_index["index"].push(index);
    id_index["title"].push(title);
  });

$("#filter").on(
  "changed.bs.select",
  function (e, clickedIndex, isSelected, previousValue) {
    $('input[type="text"], textarea').val(""); // Clears textbox area after selection.

    let id = id_index["id"][clickedIndex];
    let title = id_index["title"][clickedIndex];
    let image1 = document.getElementById(`image1`).getAttribute("src");
    let image2 = document.getElementById(`image2`).getAttribute("src");
    let image3 = document.getElementById(`image3`).getAttribute("src");
    let movie_name1 = document.getElementById("movie_name1").innerHTML;
    let movie_name2 = document.getElementById("movie_name2").innerHTML;
    let movie_name3 = document.getElementById("movie_name3").innerHTML;
    let isPosterPresent = false;
    let poster = "https://d2cltuy1xv6n7i.cloudfront.net/images/";
    poster = poster + id + ".jpg";

    // Variables to determine empty spaces for posters.
    let space1;
    let space2;
    let space3;

    // Checks to see if the most recent selection has already been selected and therefore poster should be present.
    for (let i = 0; i < previousValue.length; i++) {
      if (previousValue[i] == id) {
        isPosterPresent = true;
      }
    }

    // Checks if poster absent then sets space value to true.
    if (image1.includes("random")) {
      space1 = true;
    }

    if (image2.includes("random")) {
      space2 = true;
    }

    if (image3.includes("random")) {
      space3 = true;
    }

    if (!isPosterPresent) {
      if (space1) {
        const movieLink1 = document.getElementById("link1");

        document.getElementById("image1").setAttribute("src", poster);
        document.getElementById("movie_name1").innerHTML = title;

        setMovieLinkAttributes(movieLink1, id, title);
      } else if (space2) {
        const movieLink2 = document.getElementById("link2");

        document.getElementById("image2").setAttribute("src", poster);
        document.getElementById("movie_name2").innerHTML = title;

        setMovieLinkAttributes(movieLink2, id, title);
      } else if (space3) {
        const movieLink3 = document.getElementById("link3");

        document.getElementById("image3").setAttribute("src", poster);
        document.getElementById("movie_name3").innerHTML = title;

        setMovieLinkAttributes(movieLink3, id, title);
      }
    }

    if (isPosterPresent) {
      if (image1.includes(`/${id}.jpg`) || movie_name1 == title) {
        const movieLink1 = document.getElementById("link1");

        document
          .getElementById("image1")
          .setAttribute("src", "static/images/random1.gif");
        document.getElementById("movie_name1").innerHTML = "Selection 1";

        removeMovieLinkAttributes(movieLink1);
      } else if (image2.includes(`/${id}.jpg`) || movie_name2 == title) {
        const movieLink2 = document.getElementById("link2");

        document
          .getElementById("image2")
          .setAttribute("src", "static/images/random2.gif");
        document.getElementById("movie_name2").innerHTML = "Selection 2";

        removeMovieLinkAttributes(movieLink2);
      } else if (image3.includes(`/${id}.jpg`) || movie_name3 == title) {
        const movieLink3 = document.getElementById("link3");

        document
          .getElementById("image3")
          .setAttribute("src", "static/images/random3.gif");
        document.getElementById("movie_name3").innerHTML = "Selection 3";

        removeMovieLinkAttributes(movieLink3);
      }
    }

    let loadingContainerId = "'#loading'";
    let movies = document.getElementById("filter").selectedOptions;

    if (movies.length == 3) {
      document.getElementById(
        "button"
      ).innerHTML = `<button type="submit" class="btn btn-success" id="submit" onclick="$(${loadingContainerId}).show();" >Submit</button>`;

      $("#submit").click(function () {
        let route;
        let list = [];
        let movies = document.getElementById("filter").selectedOptions;

        if (reverse === true) {
          route = "/worst";
        } else {
          route = "/best";
        }

        for (let i = 0; i < movies.length; i++) {
          index = i + 1;
          let movie = {
            movie_title: movies[i].text,
            movie_id: movies[i].value,
          };

          list.push(movie);
        }

        $.ajax({
          type: "POST",
          contentType: "application/json;charset=utf-8",
          url: route,
          traditional: "true",
          data: JSON.stringify(list),
          dataType: "json",
          success: (res) => {
            document.getElementById("page").innerHTML = res.data;
          },
          // res is the response from the server
          error: (error) => {
            console.error(error);
          },
        });
      });
    } else {
      document.getElementById("button").innerHTML = "";
    }
  }
);
