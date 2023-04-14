const BASE_URL = "http://127.0.0.1:5000/api"

// Generate HTML of a single cupcake
function makeCupcakeHTML(cupcake){
  return `
  <div data-cupcake-id=${cupcake.id}>
    <li>
      ${cupcake.size} ${cupcake.flavor} [${cupcake.rating} / 10 rating] 
      <button class="delete-button">X</button>
    </li>
    <img class="cupcake-thumbnail" src=${cupcake.image} alt="(no image provided)">
  </div>
    `
}

// Generate list of cupcakes to display
async function listCupcakes(){
  const resp = await axios.get(`${BASE_URL}/cupcakes`)
  
  for (let cupcakeData of resp.data.cupcakes){
    let newCupcake = $(makeCupcakeHTML(cupcakeData))
    $(".cupcake-list").append(newCupcake)
  }
}

//Handle form submission
$("#new-cupcake-form").on("submit", async function (evt){
  evt.preventDefault();
  let flavor= $("#form-flavor").val();
  let rating= $("#form-rating").val();
  let size  = $("#form-size").val();
  let image = $("#form-image").val();

  const makeCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`,
    {flavor, rating, size, image});

  let newCupcake = makeCupcakeHTML(makeCupcakeResponse.data.cupcake)
  $(".cupcake-list").append(newCupcake)
  //Clear form data after submission
  $('#new-cupcake-form').trigger("reset")
})

//Handle cupcake deletion from list
$(".cupcake-list").on("click", ".delete-button", async function(evt){
  evt.preventDefault();
  let $cupcake = $(evt.target).closest("div")
  // Get the id  of the cupcake
  let $cupcakeID = $cupcake.attr("data-cupcake-id")

  // Delete cupcake from DB
  await axios.delete(`${BASE_URL}/cupcakes/${$cupcakeID}`)
  // Delete cupcake from DOM
  $cupcake.remove();
})

$(listCupcakes);
