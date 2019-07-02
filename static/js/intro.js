var toggleButton = document.getElementById('toggleSlider'),
    slide = document.querySelector('.slide');

toggleButton.addEventListener('click', toggleSlider, false);

function toggleSlider() {
  if (slide.classList.contains('slide-up')) {
    slide.classList.remove('slide-up');
  } else {
    slide.classList.add('slide-up');
  }
}

setTimeout(trans, 5000);

function trans() {
    toggleButton.click();
    var style = document.createElement('link');
    style.src= "https://code.jquery.com/jquery-3.4.1.js";
    style.setAttribute("rel", "stylesheet");
    style.setAttribute("href", "https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.9/dist/css/bootstrap-select.min.css");
    page.appendChild(style);
    document.getElementById("place").innerHTML = `<!-- Tiles -->
    <div class="container">
      <div class="row justify-content-center" >
        <!-- Tile 1 -->
        <div class="col-xl-3 col-sm-12 mb-4">
          <div class="card border-0 shadow" id="tile1">
            <img id="image1" src="static/images/random1.gif" class="img-fluid" alt="Image not found">
            <div class="card-body text-center">
              <h5 class="card-title mb-0" id="movie_name1">Selection 1</h5>
            </div>
          </div>
        </div>
        <!-- Tile 2 -->
        <div class="col-xl-3 col-sm-12 mb-4">
          <div class="card border-0 shadow" id="tile2">
            <img id="image2" src="static/images/random2.gif" class="img-fluid" alt="Image not found">
            <div class="card-body text-center">
              <h5 class="card-title mb-0" id="movie_name2">Selection 2</h5>
            </div>
          </div>
        </div>
        <!-- Tile 3 -->
        <div class="col-xl-3 col-sm-12 mb-4">
          <div class="card border-0 shadow" id="tile3">
            <img id="image3" src="static/images/random3.gif" class="img-fluid" alt="Image not found" onClick="random()">
            <div class="card-body text-center">
              <h5 class="card-title mb-0" id="movie_name3">Selection 3</h5>
            </div>
          </div>
        </div>
      </div>
      <!-- /.row -->
    
    <div class="d-flex flex-row-reverse" style="width: 87%;" id="button">
      <!-- <button type="submit" class="btn btn-success" id="submit" >Submit</button> -->
    </div>
  
    <div class="row justify-content-center" style="margin-bottom: 250px;">
      <div class="col-xl-9 col-sm-12 mb-5 mt-0">
        <select id="filter"
           class="selectpicker"
           data-width="100%" 
           data-live-search="true"
           multiple data-max-options="3" 
           data-dropup-auto="false" 
           multiple title="Click here to choose 3 movies..."
           virtualScroll="200"
           >
        </select>
      </div>
    </div>
  
  </div>
  <!-- /.container -->`

  // var filter = document.getElementById('filter');

  var style = document.createElement('link');
  style.src= "https://code.jquery.com/jquery-3.4.1.js";
  style.setAttribute("rel", "stylesheet");
  style.setAttribute("href", "https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.9/dist/css/bootstrap-select.min.css");
  page.appendChild(style);


  var script3 = document.createElement('script');
  script3.src= "https://code.jquery.com/jquery-3.4.1.js";
  script3.setAttribute("integrity", "sha256-WpOohJOqMqqyKL9FccASB9O0KwACQJpFTUBLTYOVvVU=");
  script3.setAttribute("crossorigin", "anonymous");
  place2.appendChild(script3);

  var script4 = document.createElement('script');
  script4.src= "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js";
  script4.setAttribute("integrity", "sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q");
  script4.setAttribute("crossorigin", "anonymous");
  place2.appendChild(script4);

  var script5 = document.createElement('script');
  script5.src= "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js";
  script5.setAttribute("integrity", "sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl");
  script5.setAttribute("crossorigin", "anonymous");
  place2.appendChild(script5);

  var script2 = document.createElement('script');
  script2.src= "https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.9/dist/js/bootstrap-select.min.js";
  place2.appendChild(script2);

//   <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.9/dist/css/bootstrap-select.min.css"
//   <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
//   <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
//   <script src="https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.9/dist/js/bootstrap-select.min.js"></script>


  var script= document.createElement('script');
  script.setAttribute("type", "text/javascript");
  script.src= "static/js/filter.js";
  place2.appendChild(script);
}
