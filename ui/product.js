$(document).ready(function () {
    loadProducts();

    $("#saveProductBtn").click(function () {
        addProduct();
    });
});

function loadProducts() {
    $.get(API_URL + "/getProducts", function (data) {
        let rows = "";
        data.forEach(p => {
            rows += `
              <tr>
                <td>${p.name}</td>
                <td>${p.uom_name}</td>
                <td>${p.price}</td>
                <td>
                  <button class="btn btn-danger btn-sm"
                          onclick="deleteProduct(${p.product_id})">
                    Delete
                  </button>
                </td>
              </tr>
            `;
        });
        $("#productTableBody").html(rows);
    });
}


function addProduct() {
    let product = {
        name: $("#productName").val(),
        uom_id: $("#productUnit").val(),
        price: $("#productPrice").val()
    };

    $.ajax({
        url: API_URL + "/insertProduct",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(product),
        success: function () {
            alert("Product Added");
            location.reload();
        }
    });
}


function deleteProduct(productId) {
    if (!confirm("Are you sure you want to delete this product?")) return;

    $.ajax({
        url: API_URL + "/deleteProduct/" + productId,
        type: "DELETE",
        success: function (res) {
            alert(res.message);
            loadProducts();
        },
        error: function (err) {
            alert(err.responseJSON.message);
        }
    });
}



